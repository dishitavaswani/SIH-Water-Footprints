"""Water Impact Insights Service.

Calculates human-readable volumetric comparisons, color-coded severity levels,
and mathematical water savings percentages from authoritative database values.
"""

from typing import Dict, Any, Optional
import math
from database.lookup import get_water_footprint, get_tip

# Centralized Benchmark Configuration (litres)
BENCHMARKS = [
    {"id": "water_bottle", "name": "water bottle", "plural": "water bottles", "volume": 1.0, "icon": "🧴"},
    {"id": "bucket", "name": "bucket", "plural": "buckets", "volume": 15.0, "icon": "🪣"},
    {"id": "shower", "name": "shower", "plural": "showers", "volume": 65.0, "icon": "🚿"},
    {"id": "bathtub", "name": "bathtub", "plural": "bathtubs", "volume": 150.0, "icon": "🛁"},
    {"id": "swimming_pool", "name": "swimming pool", "plural": "swimming pools", "volume": 25000.0, "icon": "🏊"},
]

# Centralized Impact Severity Threshold Configuration (litres/kg)
SEVERITY_THRESHOLDS = [
    {"max": 500.0, "level": "low", "label": "Low Water Impact", "color": "green", "icon": "🟢", "badge_class": "severity-low"},
    {"max": 1500.0, "level": "moderate", "label": "Moderate Water Impact", "color": "blue", "icon": "🔵", "badge_class": "severity-moderate"},
    {"max": 4000.0, "level": "high", "label": "High Water Impact", "color": "orange", "icon": "🟠", "badge_class": "severity-high"},
    {"max": float("inf"), "level": "very_high", "label": "Very High Water Impact", "color": "red", "icon": "🔴", "badge_class": "severity-very-high"},
]


def calculate_volumetric_comparison(total_litres: float) -> Dict[str, Any]:
    """Select the most intuitive benchmark comparison for a given total litres."""
    safe_litres = max(0.0, float(total_litres))

    if safe_litres < 30.0:
        best = BENCHMARKS[0] # water_bottle (1 L)
    elif safe_litres < 300.0:
        best = BENCHMARKS[1] # bucket (15 L)
    elif safe_litres < 500.0:
        best = BENCHMARKS[2] # shower (65 L)
    elif safe_litres < 15000.0:
        best = BENCHMARKS[3] # bathtub (150 L)
    else:
        best = BENCHMARKS[4] # swimming_pool (25000 L)

    exact_quantity = safe_litres / best["volume"]
    display_quantity = max(1, round(exact_quantity))
    unit_name = best["plural"] if display_quantity > 1 else best["name"]

    return {
        "benchmark": best["id"],
        "benchmark_name": best["name"],
        "benchmark_volume_litres": best["volume"],
        "quantity": round(exact_quantity, 2),
        "display_quantity": display_quantity,
        "unit_name": unit_name,
        "icon": best["icon"],
        "display_text": f"≈ {display_quantity} {unit_name}",
    }


def calculate_impact_severity(total_litres: float) -> Dict[str, Any]:
    """Classify water impact severity based on centralized thresholds."""
    safe_litres = max(0.0, float(total_litres))
    for t in SEVERITY_THRESHOLDS:
        if safe_litres < t["max"]:
            return {
                "level": t["level"],
                "label": t["label"],
                "color": t["color"],
                "icon": t["icon"],
                "badge_class": t["badge_class"],
            }
    return SEVERITY_THRESHOLDS[-1]


def calculate_alternative_savings(item_name: str, original_total_wf: float) -> Dict[str, Any]:
    """Look up alternative recommendations and calculate exact mathematical water savings if data exists."""
    clean_item = item_name.strip().lower()

    # Pre-mapped canonical alternative candidates in database
    alt_candidates_map = {
        "beef": ["chicken", "pulses"],
        "rice": ["wheat", "jowar", "pearl_millet", "potato"],
        "chicken": ["pulses"],
        "coffee": ["tea"],
        "chocolate": ["banana", "apple"],
        "almonds": ["coconut"],
        "cheese": ["milk"],
        "pork": ["chicken", "pulses"],
        "butter": ["coconut"],
    }

    candidates = alt_candidates_map.get(clean_item, [])
    best_alt = None

    for candidate_name in candidates:
        alt_db = get_water_footprint(candidate_name)
        if alt_db:
            alt_total = alt_db["green_wf"] + alt_db["blue_wf"] + alt_db["grey_wf"]
            if alt_total < original_total_wf:
                best_alt = {
                    "name": alt_db["item_name"],
                    "water_footprint": alt_total,
                    "unit": alt_db["unit"],
                }
                break

    # Fallback to database tip if no direct candidates map
    tip_text = get_tip(clean_item)

    if best_alt:
        savings = ((original_total_wf - best_alt["water_footprint"]) / original_total_wf) * 100.0
        savings_pct = max(1, round(savings))
        return {
            "has_alternative": True,
            "name": best_alt["name"].capitalize(),
            "water_footprint": best_alt["water_footprint"],
            "savings_percentage": savings_pct,
            "has_savings_percentage": True,
            "tip_text": tip_text,
            "display_text": f"Consider {best_alt['name'].capitalize()} as an alternative (Potential water saving: ≈ {savings_pct}%)",
        }
    elif tip_text and "Consider replacing with" in tip_text:
        # Alternative exists in text but no exact database footprint match
        suggested_name = tip_text.split("Consider replacing with")[1].split("for")[0].strip()
        return {
            "has_alternative": True,
            "name": suggested_name.capitalize(),
            "water_footprint": None,
            "savings_percentage": None,
            "has_savings_percentage": False,
            "tip_text": tip_text,
            "display_text": f"Consider {suggested_name} as an alternative",
        }
    else:
        return {
            "has_alternative": False,
            "name": None,
            "water_footprint": None,
            "savings_percentage": None,
            "has_savings_percentage": False,
            "tip_text": tip_text or "Conserve water by choosing locally grown produce.",
            "display_text": tip_text or "Conserve water by choosing locally grown produce.",
        }


def generate_water_impact_insights(
    item_name: str,
    green_wf: float,
    blue_wf: float,
    grey_wf: float,
    unit: str = "litres/kg",
    lang: str = "en",
) -> Dict[str, Any]:
    """Generate complete Water Impact Insights dictionary with multilingual translation."""
    total = round(float(green_wf) + float(blue_wf) + float(grey_wf), 2)
    comparison = calculate_volumetric_comparison(total)
    severity = calculate_impact_severity(total)
    alt_savings = calculate_alternative_savings(item_name, total)

    explanation = (
        f"Producing 1 kg of {item_name.lower()} requires approximately {total:,.0f} litres of water. "
        f"That's roughly {comparison['display_text']} of water."
    )

    if lang and lang.lower() != "en":
        try:
            from backend.app.services.translation_service import translate_text
            severity["label"] = translate_text(severity["label"], lang)
            alt_savings["display_text"] = translate_text(alt_savings["display_text"], lang)
            explanation = translate_text(explanation, lang)
        except Exception:
            pass

    return {
        "total_litres": total,
        "unit": unit,
        "comparison": comparison,
        "severity": severity,
        "alternative": alt_savings,
        "explanation": explanation,
    }
