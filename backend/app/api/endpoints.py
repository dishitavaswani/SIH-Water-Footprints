"""Footprint and scan endpoint definitions."""

import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, HTTPException, UploadFile, File, Query, status
from fastapi.responses import JSONResponse

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from database.lookup import get_footprint_data, get_water_footprint, get_comparison, get_tip, get_connection
from backend.app.services.translation_service import translate_text
from multilingual.registry import (
    get_supported_languages,
    get_supported_codes,
    normalize_language_code,
)

# Optional import of ML prediction
try:
    from ml_model.predict import predict_label
except Exception:
    predict_label = None

router = APIRouter()


@router.get("/health", tags=["System"])
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "SIH-Water-Footprint-API"}


@router.get("/languages", tags=["Languages"])
def list_languages() -> Dict[str, Any]:
    """Returns list of supported languages from the centralized language registry."""
    languages = get_supported_languages()
    return {
        "count": len(languages),
        "languages": languages,
    }


@router.get("/items", tags=["Footprint"])
def list_items() -> Dict[str, Any]:
    """Returns a list of all available food items in the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, green_wf, blue_wf, grey_wf, unit FROM water_footprint ORDER BY item_name ASC;")
        rows = cursor.fetchall()
        conn.close()
        items = [
            {
                "item": row[0],
                "green_wf": row[1],
                "blue_wf": row[2],
                "grey_wf": row[3],
                "total_litres_per_kg": round(row[1] + row[2] + row[3], 2),
                "unit": row[4],
            }
            for row in rows
        ]
        return {"count": len(items), "items": items}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query database items: {exc}",
        )


@router.get("/footprint", tags=["Footprint"])
def get_footprint(
    item: str = Query(..., description="Food or crop item name (e.g. rice, apple, chicken)"),
    lang: str = Query("en", description="Target response language code (e.g. 'en', 'hi', 'mr', 'gu', 'bn', 'ta', 'te', 'kn', 'ml', 'pa')"),
) -> Dict[str, Any]:
    """Retrieves water footprint data for a specific product."""
    clean_item = item.strip().lower()
    if not clean_item:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Item query parameter cannot be empty.",
        )

    # Validate language code against registry
    canonical_lang = normalize_language_code(lang)
    if not canonical_lang:
        supported = ", ".join(get_supported_codes())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language '{lang}'. Supported languages: {supported}",
        )

    data = get_footprint_data(clean_item)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item '{item}' not found in water footprint database.",
        )

    green = float(data["green_wf"])
    blue = float(data["blue_wf"])
    grey = float(data["grey_wf"])
    total = round(green + blue + grey, 2)
    comparison = data["comparison"]
    tip = data["tip"]
    item_name = data["item_name"]

    # Translation if non-English language requested
    if canonical_lang != "en":
        item_name = translate_text(item_name, canonical_lang)
        if comparison:
            comparison = translate_text(comparison, canonical_lang)
        if tip:
            tip = translate_text(tip, canonical_lang)

    return {
        "item": item_name,
        "item_name": item_name,
        "total_litres_per_kg": total,
        "green_water_litres": green,
        "blue_water_litres": blue,
        "grey_water_litres": grey,
        "green_wf": green,
        "blue_wf": blue,
        "grey_wf": grey,
        "unit": data.get("unit", "litres/kg"),
        "comparison": comparison,
        "tip": tip,
        "lang": canonical_lang,
    }


@router.post("/scan", tags=["Scanning"])
async def scan_image(
    file: UploadFile = File(..., description="Image file of the agricultural product/food"),
    lang: str = Query("en", description="Target response language code (e.g. 'en', 'hi', 'mr', 'gu', 'bn', 'ta', 'te', 'kn', 'ml', 'pa')"),
) -> Dict[str, Any]:
    """Accepts an image upload, recognizes the product with ML, and returns its water footprint."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid image (e.g. image/jpeg, image/png).",
        )

    # Validate language code against registry
    canonical_lang = normalize_language_code(lang)
    if not canonical_lang:
        supported = ", ".join(get_supported_codes())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language '{lang}'. Supported languages: {supported}",
        )

    # Save to a temporary file
    suffix = Path(file.filename or "scan.jpg").suffix or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name
        shutil.copyfileobj(file.file, tmp)

    try:
        recognized_label = None
        confidence = 0.0
        ml_reason = "model_inference_failed"
        ml_message = "I couldn't confidently identify this item. Try a clearer photo with the food centered in the frame."

        if predict_label is not None:
            try:
                ml_res = predict_label(tmp_path)
                if isinstance(ml_res, dict):
                    recognized_label = ml_res.get("label") or ml_res.get("predicted_label")
                    confidence = float(ml_res.get("confidence", 0.0))
                    ml_reason = ml_res.get("reason", ml_reason)
                    if ml_res.get("message"):
                        ml_message = ml_res.get("message")
                elif isinstance(ml_res, tuple) and len(ml_res) >= 2:
                    recognized_label, confidence = ml_res[0], float(ml_res[1])
            except Exception as ml_err:
                ml_message = f"Model evaluation error: {ml_err}"

        # Defensive validation: Low confidence or unrecognized item
        if not recognized_label or confidence < 0.60:
            suggested_display = ml_res.get("suggested_label") if isinstance(ml_res, dict) else recognized_label
            low_conf_msg = ml_message
            if canonical_lang != "en":
                low_conf_msg = translate_text(low_conf_msg, canonical_lang)
                if suggested_display:
                    suggested_display = translate_text(suggested_display, canonical_lang)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": False,
                    "reason": ml_reason if not recognized_label else "low_confidence",
                    "confidence": round(confidence, 3),
                    "message": low_conf_msg,
                    "suggested_label": suggested_display,
                    "canonical_label": recognized_label,
                    "lang": canonical_lang,
                },
            )

        # Lookup footprint for recognized product
        footprint = get_footprint_data(recognized_label)
        if not footprint:
            not_found_msg = f"Identified '{recognized_label}', but water footprint data is currently not available in database."
            if canonical_lang != "en":
                not_found_msg = translate_text(not_found_msg, canonical_lang)

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": False,
                    "reason": "item_not_found_in_database",
                    "confidence": round(confidence, 3),
                    "message": not_found_msg,
                    "suggested_label": recognized_label,
                    "canonical_label": recognized_label,
                    "lang": canonical_lang,
                },
            )

        green = float(footprint["green_wf"])
        blue = float(footprint["blue_wf"])
        grey = float(footprint["grey_wf"])
        total = round(green + blue + grey, 2)
        unit = footprint.get("unit", "litres/kg")
        comparison = footprint.get("comparison", "")
        tip = footprint.get("tip", "")
        label_display = footprint.get("item_name") or recognized_label

        # Localize human-readable fields via TranslationService
        if canonical_lang != "en":
            label_display = translate_text(label_display, canonical_lang)
            if comparison:
                comparison = translate_text(comparison, canonical_lang)
            if tip:
                tip = translate_text(tip, canonical_lang)

        return {
            "success": True,
            "item": label_display,
            "item_name": label_display,
            "label": label_display,
            "canonical_label": recognized_label,
            "confidence": round(confidence, 3),
            "total_litres_per_kg": total,
            "green_water_litres": green,
            "blue_water_litres": blue,
            "grey_water_litres": grey,
            "green_wf": green,
            "blue_wf": blue,
            "grey_wf": grey,
            "unit": unit,
            "comparison": comparison,
            "tip": tip,
            "lang": canonical_lang,
            "item_details": {
                "canonical_name": recognized_label,
                "display_name": label_display,
                "description": comparison,
            },
            "recognition": {
                "confidence": round(confidence, 3),
                "model": "mobilenet_v2_17class",
            },
            "water_footprint": {
                "green": green,
                "blue": blue,
                "grey": grey,
                "total": total,
                "unit": unit,
            },
        }
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
