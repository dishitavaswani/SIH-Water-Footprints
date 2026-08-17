#!/usr/bin/env python3
"""Image-recognition accuracy evaluation harness.

Evaluates the trained TFLite agricultural product classifier against all test images
in `ml_model/sample_images/` and displays a formatted summary table.
"""

import sys
from pathlib import Path
from typing import List

# Ensure parent path is in sys.path so ml_model can be imported regardless of working directory
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml_model.predict import predict_label, CONFIDENCE_THRESHOLD, DEFAULT_TFLITE_PATH, DEFAULT_LABELS_PATH

SAMPLE_IMAGES_DIR = SCRIPT_DIR / "sample_images"
VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def run_accuracy_test(sample_dir: Path = SAMPLE_IMAGES_DIR):
    """Run inference on every image in sample_images directory and print evaluation report."""
    print("\n" + "=" * 65)
    print("AGRICULTURAL PRODUCT CLASSIFIER - ACCURACY & INFERENCE TEST")
    print("=" * 65)
    print(f"Sample images directory: {sample_dir}")
    print(f"Model path:             {DEFAULT_TFLITE_PATH}")
    print(f"Labels path:            {DEFAULT_LABELS_PATH}")
    print(f"Confidence threshold:   {CONFIDENCE_THRESHOLD * 100:.1f}%")
    print("-" * 65)

    if not sample_dir.exists():
        print(f"[ERROR] Sample images directory does not exist: {sample_dir}")
        return

    # Find all sample images
    image_files: List[Path] = sorted(
        [
            f for f in sample_dir.iterdir()
            if f.is_file() and f.suffix.lower() in VALID_IMAGE_EXTENSIONS and not f.name.startswith(".")
        ]
    )

    if not image_files:
        print(
            f"[NOTICE] No test images found in {sample_dir}.\n"
            "To test predictions, add sample image files (.jpg, .png, etc.) into `ml_model/sample_images/`.\n"
            "Example: ml_model/sample_images/banana1.jpg"
        )
        print("=" * 65 + "\n")
        return

    print(f"{'Image':<26} {'Prediction':<18} {'Confidence':<12} {'Status'}")
    print("-" * 65)

    total_images = len(image_files)
    confident_count = 0
    fallback_count = 0

    for img_path in image_files:
        filename = img_path.name
        # Shorten filename if excessively long for table display
        display_name = filename if len(filename) <= 24 else filename[:21] + "..."

        result = predict_label(str(img_path))
        label = result.get("label")
        conf = result.get("confidence")

        if label is not None and conf is not None:
            confident_count += 1
            conf_str = f"{conf * 100:.1f}%"
            status = "✓ Confident"
            pred_display = label
        else:
            fallback_count += 1
            conf_str = "N/A"
            pred_display = "(Uncertain)"
            status = f"? Fallback: {result.get('message', 'Low confidence')}"

        print(f"{display_name:<26} {pred_display:<18} {conf_str:<12} {status}")

    print("-" * 65)
    print(f"SUMMARY: {total_images} total sample images tested.")
    print(f"  - Confident predictions (>= {CONFIDENCE_THRESHOLD * 100:.0f}%): {confident_count}/{total_images} ({confident_count / total_images * 100:.1f}%)")
    print(f"  - Fallback / below threshold:      {fallback_count}/{total_images}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_accuracy_test()
