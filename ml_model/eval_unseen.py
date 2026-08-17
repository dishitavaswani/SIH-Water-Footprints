#!/usr/bin/env python3
"""Evaluate all real unseen test images using the 17-class TFLite model."""

import os
import sys
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
MODELS_DIR = SCRIPT_DIR / "models"
MODEL_PATH = MODELS_DIR / "model_17class.tflite"
LABELS_PATH = MODELS_DIR / "labels_17class.txt"
TEST_DIR = SCRIPT_DIR / "real_test_images"

print("=" * 85)
print("17-CLASS TFLITE MODEL BENCHMARK ON UNSEEN REAL TEST IMAGES")
print("=" * 85)
print(f"Model:  {MODEL_PATH}")
print(f"Labels: {LABELS_PATH}")

with open(LABELS_PATH, "r", encoding="utf-8") as f:
    labels = [line.strip() for line in f if line.strip()]

print(f"Classes ({len(labels)}): {', '.join(labels)}\n")

try:
    import tflite_runtime.interpreter as tflite
    interpreter = tflite.Interpreter(model_path=str(MODEL_PATH))
except ImportError:
    import tensorflow as tf
    interpreter = tf.lite.Interpreter(model_path=str(MODEL_PATH))

interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def get_actual_label(filename: str) -> str:
    fn = filename.lower()
    if fn.startswith("mak"):
        return "makhana"
    elif fn.startswith("ma"):
        return "maize"
    elif fn.startswith("ri"):
        return "rice"
    elif fn.startswith("wh"):
        return "wheat"
    elif fn.startswith("jo"):
        return "jowar"
    elif fn.startswith("mi") or fn.startswith("pm"):
        return "pearl_millet"
    elif fn.startswith("su"):
        return "sugarcane"
    return "unknown"

test_files = sorted([f for f in TEST_DIR.iterdir() if f.is_file() and not f.name.startswith(".")])

results = []

for file_path in test_files:
    filename = file_path.name
    actual_label = get_actual_label(filename)
    
    with Image.open(file_path) as img:
        img_rgb = img.convert("RGB")
        img_resized = img_rgb.resize((224, 224), Image.Resampling.BILINEAR)
    
    img_arr = np.array(img_resized, dtype=np.float32)
    preprocessed = (img_arr / 127.5) - 1.0
    input_data = np.expand_dims(preprocessed, axis=0)
    
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])[0]
    
    top_idx = int(np.argmax(output_data))
    pred_label = labels[top_idx]
    confidence = float(output_data[top_idx])
    
    sorted_indices = np.argsort(output_data)[::-1]
    top3 = [(labels[i], float(output_data[i])) for i in sorted_indices[:3]]
    
    is_correct = (pred_label == actual_label)
    is_above_thresh = (confidence >= 0.60)
    
    results.append({
        "file": filename,
        "actual": actual_label,
        "predicted": pred_label,
        "confidence": confidence,
        "is_correct": is_correct,
        "is_above_thresh": is_above_thresh,
        "top3": top3
    })

print(f"{'Image File':<20} {'Actual':<14} {'Predicted':<14} {'Confidence':<12} {'Result':<10} {'Threshold (60%)'}")
print("-" * 85)

class_stats = defaultdict(lambda: {"total": 0, "correct": 0, "above_thresh": 0})
correct_total = 0
above_thresh_total = 0

for r in results:
    res_str = "CORRECT" if r["is_correct"] else "INCORRECT"
    thresh_str = "Pass (>=60%)" if r["is_above_thresh"] else "Fallback (<60%)"
    conf_pct = r["confidence"] * 100
    print(f"{r['file']:<20} {r['actual']:<14} {r['predicted']:<14} {conf_pct:6.2f}%      {res_str:<10} {thresh_str}")
    
    actual = r["actual"]
    class_stats[actual]["total"] += 1
    if r["is_correct"]:
        class_stats[actual]["correct"] += 1
        correct_total += 1
    if r["is_above_thresh"]:
        class_stats[actual]["above_thresh"] += 1
        above_thresh_total += 1

print("=" * 85)
print(f"Overall Accuracy: {correct_total}/{len(results)} ({correct_total / len(results) * 100:.1f}%)")
print(f"Confident Predictions (>= 60%): {above_thresh_total}/{len(results)} ({above_thresh_total / len(results) * 100:.1f}%)")
print("=" * 85)

print("\n--- PER-CLASS ACCURACY BREAKDOWN ---")
print(f"{'Class':<15} {'Total':<8} {'Correct':<10} {'Accuracy':<10} {'Confident (>=60%)'}")
print("-" * 60)
for cname, stats in sorted(class_stats.items()):
    acc = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
    print(f"{cname:<15} {stats['total']:<8} {stats['correct']:<10} {acc:6.1f}%    {stats['above_thresh']}/{stats['total']}")

print("\n--- CONFUSION & ERROR ANALYSIS (Top Predictions) ---")
for r in results:
    status_tag = "✓" if r["is_correct"] else "✗"
    top3_str = ", ".join([f"{l}: {p*100:.1f}%" for l, p in r["top3"]])
    print(f"  {status_tag} [{r['file']:<18}] Actual: {r['actual']:<12} -> {top3_str}")
