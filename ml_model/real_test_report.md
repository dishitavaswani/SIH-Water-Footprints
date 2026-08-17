# Real-World Unseen Benchmark Report (17-Class Classifier)

- **Test Execution Date:** 2026-08-18 03:26:01
- **Model Evaluated:** [`ml_model/models/model_17class.tflite`](file://ml_model/models/model_17class.tflite)
- **Labels File:** [`ml_model/models/labels_17class.txt`](file://ml_model/models/labels_17class.txt)
- **Total Unseen Images Evaluated:** **85** across all 17 classes
- **Duplicate Filtering vs Training Data:** **0 overlaps** (Strict MD5 verification)

## 1. Executive Summary & Key Metrics

- **Raw Top-1 Accuracy:** **42 / 85 (49.41%)**
- **Confident Correct (Confidence $\ge 60\%$ & Correct):** **38 / 85 (44.71%)**
- **Confident Wrong (Confidence $\ge 60\%$ & Incorrect):** **16 / 85 (18.82%)**
- **Safe Fallback (Confidence $< 60\%$):** **31 / 85 (36.47%)**

## 2. Per-Class Accuracy & Confidence Breakdown

| Class | Total Images | Top-1 Correct | Top-1 Accuracy | Avg Confidence | Confident Correct ($\ge 60\%$) | Confident Wrong | Safe Fallback (<60%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`almond`** | 6 | 0 | **0.0%** | 54.5% | 0 | 1 | 5 |
| **`banana`** | 4 | 2 | **50.0%** | 54.7% | 1 | 1 | 2 |
| **`cherry`** | 3 | 2 | **66.7%** | 90.4% | 2 | 1 | 0 |
| **`chilli`** | 6 | 0 | **0.0%** | 42.7% | 0 | 0 | 6 |
| **`coconut`** | 5 | 2 | **40.0%** | 51.8% | 1 | 1 | 3 |
| **`cucumber`** | 4 | 1 | **25.0%** | 85.6% | 1 | 3 | 0 |
| **`jowar`** | 8 | 5 | **62.5%** | 74.6% | 4 | 1 | 3 |
| **`lemon`** | 4 | 0 | **0.0%** | 70.6% | 0 | 3 | 1 |
| **`maize`** | 8 | 7 | **87.5%** | 88.3% | 7 | 0 | 1 |
| **`makhana`** | 2 | 2 | **100.0%** | 97.5% | 2 | 0 | 0 |
| **`papaya`** | 2 | 1 | **50.0%** | 85.3% | 1 | 1 | 0 |
| **`pearl_millet`** | 5 | 3 | **60.0%** | 80.9% | 2 | 2 | 1 |
| **`pineapple`** | 4 | 1 | **25.0%** | 48.1% | 1 | 0 | 3 |
| **`rice`** | 8 | 8 | **100.0%** | 93.9% | 8 | 0 | 0 |
| **`sugarcane`** | 4 | 1 | **25.0%** | 44.4% | 1 | 0 | 3 |
| **`tomato`** | 4 | 1 | **25.0%** | 64.7% | 1 | 2 | 1 |
| **`wheat`** | 8 | 6 | **75.0%** | 81.1% | 6 | 0 | 2 |

## 3. Confusion Matrix (17x17)

Rows = Ground Truth Label, Columns = Predicted Label

| Actual \ Pred | `almo` | `bana` | `cher` | `chil` | `coco` | `cucu` | `jowa` | `lemo` | `maiz` | `makh` | `papa` | `pear` | `pine` | `rice` | `suga` | `toma` | `whea` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`almond`** | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| **`banana`** | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`cherry`** | 0 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`chilli`** | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 | 1 |
| **`coconut`** | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`cucumber`** | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`jowar`** | 0 | 1 | 0 | 0 | 0 | 0 | 5 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **`lemon`** | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`maize`** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`makhana`** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`papaya`** | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| **`pearl_millet`** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 2 | 0 | 0 |
| **`pineapple`** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| **`rice`** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 |
| **`sugarcane`** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0 |
| **`tomato`** | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| **`wheat`** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 6 |

## 4. Top Confused Class Pairs

| Actual Label | Predicted Label | Error Count | Primary Reason |
| :--- | :--- | :---: | :--- |
| **`almond`** | `jowar` | **4** | Visual texture and color similarity under unconstrained backgrounds |
| **`banana`** | `maize` | **2** | Visual texture and color similarity under unconstrained backgrounds |
| **`chilli`** | `tomato` | **2** | Visual texture and color similarity under unconstrained backgrounds |
| **`lemon`** | `cherry` | **2** | Visual texture and color similarity under unconstrained backgrounds |
| **`lemon`** | `maize` | **2** | Visual texture and color similarity under unconstrained backgrounds |
| **`pearl_millet`** | `sugarcane` | **2** | Visual texture and color similarity under unconstrained backgrounds |
| **`almond`** | `lemon` | **1** | Visual texture and color similarity under unconstrained backgrounds |
| **`almond`** | `sugarcane` | **1** | Visual texture and color similarity under unconstrained backgrounds |
| **`cherry`** | `jowar` | **1** | Visual texture and color similarity under unconstrained backgrounds |
| **`chilli`** | `almond` | **1** | Visual texture and color similarity under unconstrained backgrounds |
