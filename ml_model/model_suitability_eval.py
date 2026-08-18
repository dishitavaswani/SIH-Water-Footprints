"""Comprehensive TFLite Model Suitability Evaluation Harness."""

import os
import sys
import io
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ml_model.predict import predict_label, _get_interpreter, _get_labels, preprocess_image, CONFIDENCE_THRESHOLD

MODELS_DIR = REPO_ROOT / "ml_model" / "models"
SAMPLE_IMAGES_DIR = REPO_ROOT / "ml_model" / "sample_images"
REAL_TEST_DIR = REPO_ROOT / "ml_model" / "real_test_images"

def run_suitability_validation():
    print("=" * 80)
    print(" TFLITE MODEL SUITABILITY & BOUNDARY VALIDATION HARNESS ")
    print("=" * 80)

    # 1. Inspect TFLite Interpreter Specifications
    interpreter = _get_interpreter()
    labels = _get_labels()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print("\n[MODEL TENSOR SPECIFICATIONS]")
    print(f" • Model File        : ml_model/models/model_17class.tflite")
    print(f" • Total Classes     : {len(labels)}")
    print(f" • Input Shape       : {input_details[0]['shape'].tolist()} ({input_details[0]['dtype'].__name__})")
    print(f" • Output Shape      : {output_details[0]['shape'].tolist()} ({output_details[0]['dtype'].__name__})")
    print(f" • Preprocessing     : Resampling BILINEAR to (224, 224), Normalization (x / 127.5) - 1.0 -> [-1, 1]")
    print(f" • Interpretation    : Softmax probabilities over 17 classes; top prediction via argmax.")

    # 2. Test Matrix for all 17 Trained Classes
    print("\n" + "=" * 80)
    print(" 1. TEST MATRIX FOR ALL 17 KNOWN CLASSES (Sample Images)")
    print("=" * 80)
    print(f"{'Expected Class':<16} {'Predicted Class':<16} {'Confidence':<12} {'Match':<8} {'Status'}")
    print("-" * 80)

    known_matches = 0
    total_known = 0

    for label in labels:
        # Find matching sample file
        img_candidates = list(SAMPLE_IMAGES_DIR.glob(f"{label}_sample.*"))
        if not img_candidates:
            # Fallback to real_test_images subfolder
            img_candidates = list((REAL_TEST_DIR / label).glob("*.jpg")) + list((REAL_TEST_DIR / label).glob("*.png"))

        if not img_candidates:
            print(f"{label:<16} {'(No sample file)':<16} {'N/A':<12} {'N/A':<8} [SKIPPED]")
            continue

        img_path = img_candidates[0]
        total_known += 1

        res = predict_label(str(img_path), confidence_threshold=0.0)  # get raw top prediction
        pred_label = res.get("predicted_label") or res.get("label") or "None"
        conf = res.get("confidence", 0.0)
        is_match = (pred_label.lower() == label.lower())
        if is_match:
            known_matches += 1

        match_str = "✓ MATCH" if is_match else "✗ MISMATCH"
        conf_str = f"{conf * 100:.1f}%"
        status = "CONFIDENT" if conf >= CONFIDENCE_THRESHOLD else "LOW CONF"

        print(f"{label:<16} {pred_label:<16} {conf_str:<12} {match_str:<8} {status}")

    print("-" * 80)
    print(f"Known Class Accuracy: {known_matches}/{total_known} ({known_matches/total_known*100:.1f}%)" if total_known > 0 else "")

    # 3. Test Matrix for Out-of-Vocabulary Food Items (NOT in 17 classes)
    print("\n" + "=" * 80)
    print(" 2. OUT-OF-VOCABULARY FOOD ITEMS (In DB, but NOT in 17 Vision Classes)")
    print("=" * 80)
    print("Testing how model behaves when user scans un-trained foods...")
    print(f"{'Un-trained Food':<16} {'Predicted Class':<16} {'Confidence':<12} {'Over-Confident (>60%)?'}")
    print("-" * 80)

    # Synthetic out-of-vocabulary images representing foods not trained
    unseen_foods = ["apple", "potato", "chicken", "coffee", "chocolate", "bread", "milk", "egg"]
    overconfident_unseen = 0

    for food in unseen_foods:
        # Create a representative test image file for out-of-vocabulary item
        tmp_img_path = REPO_ROOT / "ml_model" / "sample_images" / f"test_{food}.jpg"
        if not tmp_img_path.exists():
            img = Image.new("RGB", (224, 224), color=(180, 80, 60))
            img.save(tmp_img_path)

        res = predict_label(str(tmp_img_path), confidence_threshold=0.0)
        pred_label = res.get("predicted_label") or res.get("label") or "None"
        conf = res.get("confidence", 0.0)
        is_overconfident = conf >= CONFIDENCE_THRESHOLD

        if is_overconfident:
            overconfident_unseen += 1
            status = "⚠️ OVERCONFIDENT FALSE POSITIVE"
        else:
            status = "✓ Safe Low Confidence (<60%)"

        print(f"{food:<16} {pred_label:<16} {conf*100:.1f}%{'':<6} {status}")

    # 4. Test Matrix for Non-Food Objects
    print("\n" + "=" * 80)
    print(" 3. NON-FOOD & SYNTHETIC OBJECTS (Testing Out-of-Distribution Behavior)")
    print("=" * 80)
    print(f"{'Non-Food Input':<20} {'Predicted Class':<16} {'Confidence':<12} {'Behavior'}")
    print("-" * 80)

    non_food_cases = [
        ("Solid White", (255, 255, 255)),
        ("Solid Black", (0, 0, 0)),
        ("Solid Grey", (128, 128, 128)),
        ("Blue Geometric", (30, 100, 200)),
    ]

    for name, color in non_food_cases:
        tmp_path = REPO_ROOT / "ml_model" / "sample_images" / f"test_nonfood_{name.replace(' ', '_')}.jpg"
        img = Image.new("RGB", (224, 224), color=color)
        img.save(tmp_path)

        res = predict_label(str(tmp_path), confidence_threshold=0.0)
        pred_label = res.get("predicted_label") or res.get("label") or "None"
        conf = res.get("confidence", 0.0)

        if conf >= CONFIDENCE_THRESHOLD:
            behavior = f"⚠️ False Positive ({pred_label})"
        else:
            behavior = "✓ Safe Fallback (<60%)"

        print(f"{name:<20} {pred_label:<16} {conf*100:.1f}%{'':<6} {behavior}")

    print("\n" + "=" * 80)
    print(" EVALUATION SUMMARY & CONCLUSIONS")
    print("=" * 80)

if __name__ == "__main__":
    run_suitability_validation()
