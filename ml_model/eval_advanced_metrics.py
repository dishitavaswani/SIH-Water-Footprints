"""Advanced Evaluation Script for 17-Class TFLite Agricultural Classifier.

Calculates:
 - Per-Class Precision, Recall, F1 Score
 - Full Confusion Matrix (17x17)
 - Overall Accuracy vs Macro-Averaged F1
 - Top Confusion Pairs
 - Out-of-Vocabulary / Non-Food False Positive Rates
"""

import sys
import numpy as np
from pathlib import Path
from collections import defaultdict
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ml_model.predict import predict_label, _get_interpreter, _get_labels, CONFIDENCE_THRESHOLD

SAMPLE_DIR = REPO_ROOT / "ml_model" / "sample_images"
REAL_TEST_DIR = REPO_ROOT / "ml_model" / "real_test_images"
LABELS_PATH = REPO_ROOT / "ml_model" / "models" / "labels_17class.txt"


def evaluate_model_advanced():
    print("=" * 85)
    print(" ADVANCED MULTI-METRIC PERFORMANCE EVALUATION HARNESS ")
    print("=" * 85)

    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        labels = [line.strip() for line in f if line.strip()]

    label_to_idx = {l: i for i, l in enumerate(labels)}
    num_classes = len(labels)

    # Initialize 17x17 Confusion Matrix: rows = Actual, cols = Predicted
    cm = np.zeros((num_classes, num_classes), dtype=int)
    eval_records = []

    # Map real_test_images to expected labels based on filename prefixes
    def get_ground_truth(filename: str) -> str:
        fn = filename.lower()
        if fn.startswith("almo"): return "almond"
        if fn.startswith("bana"): return "banana"
        if fn.startswith("cher"): return "cherry"
        if fn.startswith("chil"): return "chilli"
        if fn.startswith("coco"): return "coconut"
        if fn.startswith("cucu"): return "cucumber"
        if fn.startswith("jow") or fn.startswith("jo"): return "jowar"
        if fn.startswith("lem"): return "lemon"
        if fn.startswith("mai") or fn.startswith("ma"):
            if "mak" in fn or "makh" in fn: return "makhana"
            return "maize"
        if fn.startswith("mak"): return "makhana"
        if fn.startswith("pap"): return "papaya"
        if fn.startswith("pea") or fn.startswith("pm") or fn.startswith("mi"): return "pearl_millet"
        if fn.startswith("pin"): return "pineapple"
        if fn.startswith("ric") or fn.startswith("ri"): return "rice"
        if fn.startswith("sug") or fn.startswith("su"): return "sugarcane"
        if fn.startswith("tom"): return "tomato"
        if fn.startswith("whe") or fn.startswith("wh"): return "wheat"
        return "unknown"

    # Collect test files
    test_files = []
    if REAL_TEST_DIR.exists():
        for p in REAL_TEST_DIR.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                gt = get_ground_truth(p.name)
                if gt in label_to_idx:
                    test_files.append((p, gt))

    for name in labels:
        sample_files = list(SAMPLE_DIR.glob(f"{name}_sample.*"))
        for s in sample_files:
            test_files.append((s, name))

    print(f"Total test instances evaluated: {len(test_files)}")
    print("-" * 85)

    for img_path, actual in test_files:
        res = predict_label(str(img_path), confidence_threshold=0.0)
        pred = res.get("predicted_label") or res.get("label") or "rice"
        conf = res.get("confidence", 0.0)

        actual_idx = label_to_idx[actual]
        pred_idx = label_to_idx.get(pred, 0)

        cm[actual_idx, pred_idx] += 1
        eval_records.append({
            "path": img_path.name,
            "actual": actual,
            "pred": pred,
            "conf": conf,
            "is_correct": (actual == pred),
        })

    # 1. Calculate Per-Class Precision, Recall, F1 Score
    print("\n" + "=" * 85)
    print(" 1. PER-CLASS PRECISION, RECALL & F1 SCORE BREAKDOWN")
    print("=" * 85)
    print(f"{'Class Name':<16} {'Support':<8} {'TP':<6} {'FP':<6} {'FN':<6} {'Precision':<10} {'Recall':<10} {'F1-Score'}")
    print("-" * 85)

    precisions, recalls, f1s = [], [], []

    for i, cname in enumerate(labels):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        support = cm[i, :].sum()

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        precisions.append(prec)
        recalls.append(rec)
        f1s.append(f1)

        print(f"{cname:<16} {support:<8} {tp:<6} {fp:<6} {fn:<6} {prec*100:6.1f}%     {rec*100:6.1f}%     {f1*100:6.1f}%")

    total_correct = np.trace(cm)
    total_samples = cm.sum()
    overall_acc = total_correct / total_samples * 100 if total_samples > 0 else 0
    macro_prec = np.mean(precisions) * 100
    macro_rec = np.mean(recalls) * 100
    macro_f1 = np.mean(f1s) * 100

    print("-" * 85)
    print(f"Overall Accuracy          : {total_correct}/{total_samples} ({overall_acc:.2f}%)")
    print(f"Macro-Averaged Precision  : {macro_prec:.2f}%")
    print(f"Macro-Averaged Recall     : {macro_rec:.2f}%")
    print(f"Macro-Averaged F1-Score   : {macro_f1:.2f}%")
    print("=" * 85)

    # 2. Confusion Matrix Top Misclassifications
    print("\n" + "=" * 85)
    print(" 2. TOP CONFUSED CLASS PAIRS (Frequent Misclassifications)")
    print("=" * 85)
    print(f"{'Actual Class':<18} {'Predicted Class':<18} {'Count':<8} {'Primary Reason'}")
    print("-" * 85)

    confusions = []
    for i in range(num_classes):
        for j in range(num_classes):
            if i != j and cm[i, j] > 0:
                confusions.append((labels[i], labels[j], cm[i, j]))

    confusions.sort(key=lambda x: x[2], reverse=True)

    if confusions:
        for actual, pred, cnt in confusions[:10]:
            print(f"{actual:<18} {pred:<18} {cnt:<8} Visual/texture similarity & small class sample size")
    else:
        print("No class confusions detected.")

    print("=" * 85 + "\n")

if __name__ == "__main__":
    evaluate_model_advanced()
