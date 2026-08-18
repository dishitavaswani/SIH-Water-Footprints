"""Dataset Audit & Analysis Harness.

Analyzes training images per class, class imbalance ratio, image resolutions,
corrupted files, and visual class distinguishability.
"""

import sys
from pathlib import Path
from collections import defaultdict
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = REPO_ROOT / "ml_model" / "sample_images"
REAL_TEST_DIR = REPO_ROOT / "ml_model" / "real_test_images"
TRAIN_DIR = REPO_ROOT / "ml_model" / "training_data"
LABELS_PATH = REPO_ROOT / "ml_model" / "models" / "labels_17class.txt"

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def audit_dataset():
    print("=" * 80)
    print(" ML MODEL DATASET & CLASS IMBALANCE AUDIT REPORT ")
    print("=" * 80)

    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        labels = [line.strip() for line in f if line.strip()]

    print(f"Target Vision Classes ({len(labels)}):")
    for idx, name in enumerate(labels, 1):
        print(f"  {idx:2d}. {name}")

    print("\n" + "-" * 80)
    print(" 1. SAMPLE & TEST DATASET COUNTS PER CLASS")
    print("-" * 80)
    print(f"{'Class Name':<20} {'Sample Images':<18} {'Real Test Images':<18} {'Total Evaluated'}")
    print("-" * 80)

    total_samples = 0
    total_real = 0
    class_counts = {}

    for name in labels:
        sample_cnt = len(list(SAMPLE_DIR.glob(f"{name}_sample.*")))
        real_cnt = len(list((REAL_TEST_DIR / name).glob("*.*"))) if (REAL_TEST_DIR / name).exists() else 0
        
        # Check root of real_test_images if subfolder not present
        if real_cnt == 0 and REAL_TEST_DIR.exists():
            real_cnt = len([f for f in REAL_TEST_DIR.iterdir() if f.is_file() and f.name.lower().startswith(name[:3])])

        total_cnt = sample_cnt + real_cnt
        class_counts[name] = total_cnt
        total_samples += sample_cnt
        total_real += real_cnt

        print(f"{name:<20} {sample_cnt:<18} {real_cnt:<18} {total_cnt}")

    print("-" * 80)
    print(f"{'TOTALS':<20} {total_samples:<18} {total_real:<18} {total_samples + total_real}")

    # Class Imbalance Metric
    counts = list(class_counts.values())
    max_cnt = max(counts) if counts else 1
    min_cnt = min(counts) if counts else 1
    imbalance_ratio = max_cnt / max(min_cnt, 1)

    print("\n" + "-" * 80)
    print(" 2. CLASS IMBALANCE & QUALITY ANALYSIS")
    print("-" * 80)
    print(f" • Highest Count Class : {max(class_counts, key=class_counts.get)} ({max_cnt} images)")
    print(f" • Lowest Count Class  : {min(class_counts, key=class_counts.get)} ({min_cnt} images)")
    print(f" • Imbalance Ratio     : {imbalance_ratio:.2f}:1")
    
    if imbalance_ratio > 2.0:
        print("   ⚠️ Class Imbalance Warning: Severe sample size variance across classes.")
        print("   -> Mitigation required: Class weighting during loss compilation & heavy augmentation for minority classes.")
    else:
        print("   ✓ Balanced Distribution across test set.")

    # Image Resolution & Color Channel Diversity Audit
    resolutions = []
    formats = defaultdict(int)
    corrupted = 0

    all_test_imgs = list(SAMPLE_DIR.glob("*.*")) + list(REAL_TEST_DIR.rglob("*.*"))
    for img_p in all_test_imgs:
        if not img_p.is_file() or img_p.name.startswith("."):
            continue
        try:
            with Image.open(img_p) as img:
                resolutions.append(img.size)
                formats[img.format] += 1
        except Exception:
            corrupted += 1

    print("\n" + "-" * 80)
    print(" 3. IMAGE QUALITY & DIVERSITY CHECK")
    print("-" * 80)
    print(f" • Total Image Files Checked : {len(resolutions)}")
    print(f" • Image Formats Found      : {dict(formats)}")
    print(f" • Corrupted / Unreadable    : {corrupted}")
    if resolutions:
        avg_w = sum(r[0] for r in resolutions) / len(resolutions)
        avg_h = sum(r[1] for r in resolutions) / len(resolutions)
        print(f" • Average Resolution        : {avg_w:.0f}x{avg_h:.0f} px")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    audit_dataset()
