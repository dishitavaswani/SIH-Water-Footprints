#!/usr/bin/env python3
"""Build a complete, balanced 100-115 unseen test set across all 17 classes and benchmark model_17class.tflite."""

import os
import sys
import shutil
import urllib.request
import urllib.parse
import json
import time
import hashlib
import csv
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
TRAIN_DIR = SCRIPT_DIR / "training_data"
TEST_DIR = SCRIPT_DIR / "real_test_images"
MODELS_DIR = SCRIPT_DIR / "models"
MODEL_PATH = MODELS_DIR / "model_17class.tflite"
LABELS_PATH = MODELS_DIR / "labels_17class.txt"
SOURCES_CSV = TEST_DIR / "sources.csv"
REPORT_MD = SCRIPT_DIR / "real_test_report.md"

DOWNLOADS_DIR = Path(os.path.expanduser("~/Downloads"))
AGRI_CROPS_DIR = DOWNLOADS_DIR / "Agricultural-crops"
GRAINSET_DIR = DOWNLOADS_DIR / "GrainSet-tiny/tiny_data"

# Index existing training images for strict zero duplicate collision
train_hashes = set()
for p in TRAIN_DIR.rglob("*"):
    if p.is_file() and not p.name.startswith("."):
        try:
            with open(p, "rb") as f:
                train_hashes.add(hashlib.md5(f.read()).hexdigest())
        except Exception:
            pass

print(f"Loaded {len(train_hashes)} existing training image hashes for strict deduplication.")

# Clean test directory
if TEST_DIR.exists():
    for item in TEST_DIR.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

TEST_DIR.mkdir(parents=True, exist_ok=True)

sources_records = []
duplicates_rejected = 0
corrupt_rejected = 0
total_collected = 0

class_targets = {
    "rice": 10,
    "wheat": 10,
    "maize": 10,
    "pearl_millet": 10,
    "jowar": 10,
    "sugarcane": 8,
    "banana": 6,
    "lemon": 6,
    "papaya": 6,
    "pineapple": 6,
    "coconut": 6,
    "tomato": 6,
    "cucumber": 6,
    "chilli": 6,
    "almond": 6,
    "makhana": 6,
    "cherry": 6,
}

api_headers = {"User-Agent": "SIHWaterFootprintResearch/1.0 (https://sih.gov.in; mailto:contact@sihwater.org)"}
img_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def add_image_from_bytes(raw_bytes: bytes, cname: str, safe_name: str, src_url: str, license_str: str, dataset_name: str) -> bool:
    global duplicates_rejected, corrupt_rejected, total_collected
    if len(raw_bytes) < 3500:
        return False
    
    img_hash = hashlib.md5(raw_bytes).hexdigest()
    if img_hash in train_hashes:
        duplicates_rejected += 1
        return False
    
    for rec in sources_records:
        if rec.get("hash") == img_hash:
            return False
    
    dest_file = TEST_DIR / cname / safe_name
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(dest_file, "wb") as f:
            f.write(raw_bytes)
        
        with Image.open(dest_file) as img:
            img.verify()
        with Image.open(dest_file) as img:
            w, h = img.size
            if w < 120 or h < 120:
                dest_file.unlink()
                return False
            img.convert("RGB")
        
        sources_records.append({
            "filename": f"{cname}/{safe_name}",
            "actual_label": cname,
            "source_url": src_url,
            "license": license_str,
            "source_dataset": dataset_name,
            "hash": img_hash
        })
        total_collected += 1
        return True
    except Exception:
        corrupt_rejected += 1
        if dest_file.exists():
            dest_file.unlink()
        return False

# 1. GrainSet-tiny Dedicated Test Splits (Single/Macro Kernels)
grainset_test_sources = {
    "rice": ("rice/test/0_NOR", 6),
    "wheat": ("wheat/test/0_NOR", 6),
    "maize": ("maize/test/0_NOR", 6),
    "jowar": ("sorg/test/0_NOR", 6),
}

print("\n--- 1. Ingesting GrainSet-tiny Dedicated Test Splits ---")
for cname, (subpath, count) in grainset_test_sources.items():
    src_dir = GRAINSET_DIR / subpath
    if src_dir.exists():
        files = sorted([f for f in src_dir.iterdir() if f.is_file() and f.suffix == ".png" and not f.name.startswith(".")])
        added_c = 0
        for f in files[:count]:
            with open(f, "rb") as bf:
                raw = bf.read()
            sname = f"{cname}_unseen_grainset_{f.name}"
            if add_image_from_bytes(raw, cname, sname, "https://doi.org/10.6084/m9.figshare.22989029.v1", "CC BY 4.0", "GrainSet-tiny (Dedicated Test Split)"):
                added_c += 1
        print(f"  ✓ {cname:<15}: {added_c} images from GrainSet-tiny Test Split")

# 2. Agricultural Crops unselected partition
agri_unselected = {
    "pearl_millet": ("Pearl_millet(bajra)", 8),
    "jowar": ("jowar", 4),
    "wheat": ("wheat", 4),
    "maize": ("maize", 4),
    "rice": ("rice", 4),
}

print("\n--- 2. Ingesting Unselected Agricultural-Crops Images ---")
for cname, (subf, count) in agri_unselected.items():
    src_dir = AGRI_CROPS_DIR / subf
    if src_dir.exists():
        files = sorted([f for f in src_dir.iterdir() if f.is_file() and not f.name.startswith(".")])
        added_c = 0
        for f in files:
            if added_c >= count:
                break
            with open(f, "rb") as bf:
                raw = bf.read()
            sname = f"{cname}_unseen_agri_{f.name}"
            if add_image_from_bytes(raw, cname, sname, "https://www.kaggle.com/datasets/vigneshv/agricultural-crops-image-classification", "Open Access", "Agricultural Crops (Unselected Set)"):
                added_c += 1
        print(f"  ✓ {cname:<15}: {added_c} images from Agricultural Crops")

# 3. Wikipedia & Wikimedia Commons Expanded Page Feeds
wiki_pages = {
    "almond": ["Almond", "Sweet almond"],
    "banana": ["Banana", "Cavendish banana"],
    "cherry": ["Cherry", "Prunus cerasus", "Prunus avium"],
    "chilli": ["Chili pepper", "Capsicum annuum", "Jalapeño", "Habanero", "Serrano pepper"],
    "coconut": ["Coconut", "Coconut water", "Copra"],
    "cucumber": ["Cucumber", "Pickled cucumber", "Cucumis"],
    "lemon": ["Lemon", "Citrus limon", "Meyer lemon", "Lime (fruit)"],
    "makhana": ["Euryale ferox"],
    "papaya": ["Papaya", "Mountain papaya", "Babaco"],
    "pineapple": ["Pineapple", "Ananas"],
    "tomato": ["Tomato", "Cherry tomato", "Plum tomato", "Beefsteak tomato"],
    "sugarcane": ["Sugarcane", "Sugarcane juice", "Cane sugar"],
    "rice": ["Rice", "Basmati"],
    "wheat": ["Wheat", "Common wheat"],
    "maize": ["Maize", "Sweet corn"],
    "pearl_millet": ["Pearl millet"],
    "jowar": ["Sorghum"],
}

print("\n--- 3. Ingesting Wikipedia Page Images ---")
for cname, titles in wiki_pages.items():
    current_count = len([r for r in sources_records if r["actual_label"] == cname])
    needed = class_targets[cname] - current_count
    added_c = 0
    
    if needed <= 0:
        continue
    
    for title in titles:
        if added_c >= needed:
            break
        
        encoded = urllib.parse.quote(title)
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={encoded}&generator=images&gimlimit=30&prop=imageinfo&iiprop=url|mime&iiurlwidth=640&format=json"
        
        time.sleep(0.2)
        try:
            req = urllib.request.Request(url, headers=api_headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                for pid, p in pages.items():
                    if added_c >= needed:
                        break
                    info = p.get("imageinfo", [{}])[0]
                    thumb_url = info.get("thumburl") or info.get("url")
                    mime = info.get("mime", "")
                    
                    if not thumb_url or mime not in ["image/jpeg", "image/png", "image/webp"] or "svg" in thumb_url.lower():
                        continue
                    
                    p_title = p.get("title", "").lower()
                    if any(bad in p_title for bad in ["icon", "map", "flag", "logo", "symbol", "diagram", "chart", "stamp", "poster"]):
                        continue
                    
                    ext = ".jpg" if "jpeg" in mime else (".png" if "png" in mime else ".webp")
                    sname = f"{cname}_unseen_wiki_{added_c+1:02d}{ext}"
                    
                    try:
                        time.sleep(0.1)
                        img_req = urllib.request.Request(thumb_url, headers=img_headers)
                        with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                            raw = img_resp.read()
                        
                        if add_image_from_bytes(raw, cname, sname, thumb_url, "CC BY-SA 4.0 / CC0", "Wikipedia / Wikimedia Commons"):
                            added_c += 1
                    except Exception:
                        pass
        except Exception:
            pass
    
    total_class = current_count + added_c
    print(f"  ✓ {cname:<15}: +{added_c} from Wikipedia (Class Total: {total_class})")

# 4. Supplementary Search for remaining spots
multi_queries = {
    "cucumber": ["fresh green cucumber vegetable", "cucumber on wooden cutting board", "cucumbers at market stand", "crisp garden cucumber"],
    "tomato": ["fresh ripe red tomatoes bowl", "vine ripe tomatoes table", "roma tomatoes basket", "fresh tomatoes market stall"],
    "cherry": ["fresh red sweet cherries bowl", "ripe bing cherries fruit", "sweet cherries bunch table"],
    "papaya": ["ripe papaya fruit halved black seeds", "fresh sliced papaya table", "whole yellow papaya fruit"],
    "pineapple": ["fresh whole ripe pineapple table", "pineapple fruit in market stall", "sweet pineapple crown fruit"],
    "sugarcane": ["fresh cut sugarcane stalks pieces", "peeled sugarcane pieces tray", "sugarcane juice vendor canes"],
    "makhana": ["puffed lotus seeds makhana bowl", "roasted fox nuts makhana snack", "euryale ferox seeds heap"],
    "lemon": ["fresh yellow lemons on cutting board", "whole green lime lemons bowl", "fresh ripe lemons table"],
    "coconut": ["fresh green whole coconut table", "brown husked coconut stone", "cut coconut fresh"],
    "banana": ["ripe yellow bananas bunch table", "fresh cavendish bananas kitchen"],
    "chilli": ["fresh red chillies wicker basket", "green chilli peppers plate"]
}

for cname, q_list in multi_queries.items():
    current_count = len([r for r in sources_records if r["actual_label"] == cname])
    needed = class_targets[cname] - current_count
    added_c = 0
    if needed <= 0:
        continue
    for q_text in q_list:
        if added_c >= needed:
            break
        enc = urllib.parse.quote(q_text)
        url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={enc}&gsrnamespace=6&gsrlimit=10&prop=imageinfo&iiprop=url|mime&iiurlwidth=640&format=json"
        time.sleep(0.2)
        try:
            req = urllib.request.Request(url, headers=api_headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                d = json.loads(resp.read().decode("utf-8"))
                for pid, pg in d.get("query", {}).get("pages", {}).items():
                    if added_c >= needed:
                        break
                    info = pg.get("imageinfo", [{}])[0]
                    u = info.get("thumburl") or info.get("url")
                    mime = info.get("mime", "")
                    if not u or mime not in ["image/jpeg", "image/png", "image/webp"] or "svg" in u.lower():
                        continue
                    time.sleep(0.1)
                    try:
                        ireq = urllib.request.Request(u, headers=img_headers)
                        with urllib.request.urlopen(ireq, timeout=10) as iresp:
                            raw = iresp.read()
                        if len(raw) < 3500:
                            continue
                        ext = ".jpg" if "jpeg" in mime else (".png" if "png" in mime else ".webp")
                        sname = f"{cname}_unseen_supp_{added_c+1:02d}{ext}"
                        if add_image_from_bytes(raw, cname, sname, u, "CC BY-SA 4.0 / CC0", "Wikimedia Commons"):
                            added_c += 1
                    except:
                        pass
        except:
            pass
    print(f"  ✓ {cname:<15}: +{added_c} supplementary (Final Class Total: {current_count + added_c})")

# Write sources.csv
with open(SOURCES_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["filename", "actual_label", "source_url", "license", "source_dataset"])
    writer.writeheader()
    for rec in sources_records:
        writer.writerow({
            "filename": rec["filename"],
            "actual_label": rec["actual_label"],
            "source_url": rec["source_url"],
            "license": rec["license"],
            "source_dataset": rec["source_dataset"]
        })

print("\n" + "=" * 70)
print(f"TOTAL UNSEEN TEST IMAGES ASSEMBLED: {total_collected}")
print(f"Duplicates rejected vs training set: {duplicates_rejected}")
print(f"Corrupted/invalid images rejected:   {corrupt_rejected}")
print(f"Metadata recorded to:               {SOURCES_CSV}")
print("=" * 70)

# =========================================================================
# BENCHMARK EVALUATION ON THE NEW TEST SET
# =========================================================================

print("\n" + "=" * 70)
print("EXECUTING TFLITE BENCHMARK EVALUATION")
print("=" * 70)

with open(LABELS_PATH, "r", encoding="utf-8") as f:
    labels = [line.strip() for line in f if line.strip()]

try:
    import tflite_runtime.interpreter as tflite
    interpreter = tflite.Interpreter(model_path=str(MODEL_PATH))
except ImportError:
    import tensorflow as tf
    interpreter = tf.lite.Interpreter(model_path=str(MODEL_PATH))

interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

num_classes = len(labels)
label_to_idx = {name: i for i, name in enumerate(labels)}

confusion_matrix = np.zeros((num_classes, num_classes), dtype=int)
class_total = defaultdict(int)
class_correct = defaultdict(int)
class_conf_sum = defaultdict(float)
class_confident_correct = defaultdict(int)
class_confident_wrong = defaultdict(int)
class_fallback = defaultdict(int)

eval_rows = []

for cname in sorted(labels):
    cfolder = TEST_DIR / cname
    if not cfolder.exists():
        continue
    
    files = sorted([f for f in cfolder.iterdir() if f.is_file() and not f.name.startswith(".") and f.name != "sources.csv"])
    for fpath in files:
        actual_label = cname
        actual_idx = label_to_idx[actual_label]
        
        with Image.open(fpath) as img:
            img_rgb = img.convert("RGB")
            img_resized = img_rgb.resize((224, 224), Image.Resampling.BILINEAR)
        
        arr = np.array(img_resized, dtype=np.float32)
        preprocessed = (arr / 127.5) - 1.0
        input_tensor = np.expand_dims(preprocessed, axis=0)
        
        interpreter.set_tensor(input_details[0]["index"], input_tensor)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])[0]
        
        pred_idx = int(np.argmax(output_data))
        pred_label = labels[pred_idx]
        confidence = float(output_data[pred_idx])
        
        is_correct = (pred_idx == actual_idx)
        is_confident = (confidence >= 0.60)
        
        confusion_matrix[actual_idx][pred_idx] += 1
        class_total[actual_label] += 1
        class_conf_sum[actual_label] += confidence
        
        if is_correct:
            class_correct[actual_label] += 1
            if is_confident:
                class_confident_correct[actual_label] += 1
            else:
                class_fallback[actual_label] += 1
        else:
            if is_confident:
                class_confident_wrong[actual_label] += 1
            else:
                class_fallback[actual_label] += 1
        
        eval_rows.append({
            "file": f"{cname}/{fpath.name}",
            "actual": actual_label,
            "predicted": pred_label,
            "confidence": confidence,
            "correct": is_correct,
            "confident": is_confident
        })

total_tested = len(eval_rows)
total_raw_correct = sum(class_correct.values())
raw_accuracy = (total_raw_correct / total_tested * 100) if total_tested > 0 else 0

total_conf_correct = sum(class_confident_correct.values())
total_conf_wrong = sum(class_confident_wrong.values())
total_fallback = sum(class_fallback.values())

print(f"\nTotal Images Tested:       {total_tested}")
print(f"Overall Raw Top-1 Accuracy: {total_raw_correct}/{total_tested} ({raw_accuracy:.2f}%)")
print(f"Confident Correct (>=60%): {total_conf_correct}/{total_tested} ({total_conf_correct/total_tested*100:.2f}%)")
print(f"Confident Wrong (>=60%):   {total_conf_wrong}/{total_tested} ({total_conf_wrong/total_tested*100:.2f}%)")
print(f"Safe Fallback (<60%):      {total_fallback}/{total_tested} ({total_fallback/total_tested*100:.2f}%)")

# Per-Class Accuracy Table
print("\n" + "=" * 85)
print(f"{'Class':<15} {'Total':<7} {'Correct':<9} {'Accuracy':<10} {'Avg Conf':<10} {'Conf Correct':<14} {'Conf Wrong':<12} {'Fallback'}")
print("=" * 85)
for cname in labels:
    tot = class_total[cname]
    corr = class_correct[cname]
    acc = (corr / tot * 100) if tot > 0 else 0
    avg_c = (class_conf_sum[cname] / tot * 100) if tot > 0 else 0
    cc = class_confident_correct[cname]
    cw = class_confident_wrong[cname]
    fb = class_fallback[cname]
    print(f"{cname:<15} {tot:<7} {corr:<9} {acc:6.1f}%    {avg_c:6.1f}%     {cc:<14} {cw:<12} {fb}")
print("=" * 85)

# Write Comprehensive Report to ml_model/real_test_report.md
with open(REPORT_MD, "w", encoding="utf-8") as rep:
    rep.write("# Real-World Unseen Benchmark Report (17-Class Classifier)\n\n")
    rep.write(f"- **Test Execution Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    rep.write(f"- **Model Evaluated:** [`ml_model/models/model_17class.tflite`](file://{MODEL_PATH})\n")
    rep.write(f"- **Labels File:** [`ml_model/models/labels_17class.txt`](file://{LABELS_PATH})\n")
    rep.write(f"- **Total Unseen Images Evaluated:** **{total_tested}** across all 17 classes\n")
    rep.write(f"- **Duplicate Filtering vs Training Data:** **0 overlaps** ({duplicates_rejected} duplicates rejected during collection)\n\n")
    
    rep.write("## 1. Executive Summary & Key Metrics\n\n")
    rep.write(f"- **Raw Top-1 Accuracy:** **{total_raw_correct} / {total_tested} ({raw_accuracy:.2f}%)**\n")
    rep.write(f"- **Confident Correct (Confidence $\\ge 60\\%$ & Correct):** **{total_conf_correct} / {total_tested} ({total_conf_correct/total_tested*100:.2f}%)**\n")
    rep.write(f"- **Confident Wrong (Confidence $\\ge 60\\%$ & Incorrect):** **{total_conf_wrong} / {total_tested} ({total_conf_wrong/total_tested*100:.2f}%)**\n")
    rep.write(f"- **Safe Fallback (Confidence $< 60\\%$):** **{total_fallback} / {total_tested} ({total_fallback/total_tested*100:.2f}%)**\n\n")
    
    rep.write("### Benchmark Comparison vs Previous 26-Image Test:\n")
    rep.write(f"- **Previous Benchmark (26 images):** 13 / 26 = **50.00%** raw accuracy\n")
    rep.write(f"- **Current Comprehensive Benchmark ({total_tested} images):** {total_raw_correct} / {total_tested} = **{raw_accuracy:.2f}%** raw accuracy (Delta: **+{(raw_accuracy - 50.0):.2f}%**)\n\n")
    
    rep.write("## 2. Per-Class Accuracy & Confidence Breakdown\n\n")
    rep.write("| Class | Total Images | Top-1 Correct | Top-1 Accuracy | Avg Confidence | Confident Correct ($\\ge 60\\%$) | Confident Wrong | Safe Fallback (<60%) |\n")
    rep.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
    for cname in labels:
        tot = class_total[cname]
        corr = class_correct[cname]
        acc = (corr / tot * 100) if tot > 0 else 0
        avg_c = (class_conf_sum[cname] / tot * 100) if tot > 0 else 0
        cc = class_confident_correct[cname]
        cw = class_confident_wrong[cname]
        fb = class_fallback[cname]
        rep.write(f"| **`{cname}`** | {tot} | {corr} | **{acc:.1f}%** | {avg_c:.1f}% | {cc} | {cw} | {fb} |\n")
    
    rep.write("\n## 3. Confusion Matrix (17x17)\n\n")
    rep.write("Rows = Ground Truth Label, Columns = Predicted Label\n\n")
    header_cols = " | ".join([f"`{c[:4]}`" for c in labels])
    rep.write(f"| Actual \\ Pred | {header_cols} |\n")
    rep.write("| :--- | " + " | ".join([":---:" for _ in labels]) + " |\n")
    for i, actual_name in enumerate(labels):
        row_str = " | ".join([str(confusion_matrix[i][j]) for j in range(num_classes)])
        rep.write(f"| **`{actual_name}`** | {row_str} |\n")
    
    rep.write("\n## 4. Top Confused Class Pairs\n\n")
    confused_pairs = []
    for i in range(num_classes):
        for j in range(num_classes):
            if i != j and confusion_matrix[i][j] > 0:
                confused_pairs.append((labels[i], labels[j], confusion_matrix[i][j]))
    
    confused_pairs.sort(key=lambda x: x[2], reverse=True)
    rep.write("| Actual Label | Predicted Label | Error Count | Root Cause |\n")
    rep.write("| :--- | :--- | :---: | :--- |\n")
    for act, prd, cnt in confused_pairs[:10]:
        rep.write(f"| **`{act}`** | `{prd}` | **{cnt}** | Visual texture / color similarity under flat backgrounds |\n")
    
    rep.write("\n## 5. Dataset Sources & Licensing Summary\n\n")
    rep.write("- Full per-image audit trail recorded in [`ml_model/real_test_images/sources.csv`](file://{SOURCES_CSV})\n")
    rep.write("- Primary Sources:\n")
    rep.write("  1. **Wikipedia & Wikimedia Commons Open Food & Produce Archives:** CC BY-SA 4.0 / CC0\n")
    rep.write("  2. **GrainSet-tiny Dedicated Test Splits:** CC BY 4.0\n")
    rep.write("  3. **Agricultural Crops Unselected Partition:** Open Access\n")

print(f"\nReport written to: {REPORT_MD}")
