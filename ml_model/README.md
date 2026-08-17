# ML Image Recognition — Agricultural Product Classifier

This module implements the Machine Learning and Image Recognition pipeline for the **SIH Water Footprints** application. It classifies raw agricultural food products from camera images and passes the recognized product label and confidence score to the FastAPI backend for water-footprint calculations.

---

## 1. Pipeline Architecture

```text
Camera Photo / Upload
         │
         ▼
FastAPI Backend (/scan endpoint)
         │
         ▼
ml_model.predict.predict_label(image_path)
         │
    ┌────┴──────────────────────────┐
    ▼                               ▼
Confidence >= 0.60             Confidence < 0.60
{"label": "banana",           {"label": None,
 "confidence": 0.94}           "message": "Could not confidently..."}
    │                               │
    ▼                               ▼
Database Water Footprint       Fallback Prompt / Manual Selection
Lookup
```

---

## 2. Directory Structure

```text
ml_model/
├── models/
│   ├── model.tflite          # Deployed TFLite model
│   ├── labels.txt            # Dynamic class labels in exact model index order
│   └── model.keras           # Trained Keras checkpoint (local/ignored by git)
├── sample_images/            # Test photos for accuracy evaluation
├── training_data/            # Training dataset organized by class name (ignored by git)
│   ├── apple/
│   ├── banana/
│   ├── rice/
│   ├── tomato/
│   └── ...
├── __init__.py               # Package init exposing predict_label
├── train.py                  # MobileNetV2 transfer learning with pre-flight check
├── convert_to_tflite.py      # Exports trained Keras model to model.tflite
├── predict.py                # Fast inference module with singleton model caching
├── accuracy_test.py          # Batch evaluation test harness
├── requirements.txt          # ML-specific dependencies
└── README.md                 # This documentation
```

---

## 3. Dataset Setup

Place raw agricultural product images into class-specific folders under `training_data/`:

```text
ml_model/training_data/<class_name>/*.jpg
```

**Target scope:** Raw agricultural products and food items as encountered in kitchens, stores, or households (e.g. `apple`, `banana`, `rice`, `tomato`, `onion`, `cabbage`, `wheat`, etc.).  
*(Note: We classify raw items, NOT cooked/prepared dishes, plant diseases, leaves, or crop health).*

- **Dynamic classes:** The folder names are automatically detected and used as class labels.
- **Image formats:** `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`.
- **Quality verification:** `train.py` automatically validates all images before training, identifies corrupted/unreadable files, and reports class distribution.

---

## 4. Quick Start Commands

### A. Install Dependencies
```bash
pip install -r ml_model/requirements.txt
```

### B. Train the Model
```bash
python ml_model/train.py
```
- Performs a dataset pre-flight check and reports image counts per class.
- Uses transfer learning with **MobileNetV2** pretrained on ImageNet.
- Applies light data augmentation (horizontal flip, small rotation, small zoom) to training data only.
- Trains for up to 10 epochs with early stopping (patience = 3) on validation loss.
- Saves the trained model to `ml_model/models/model.keras` and exports `ml_model/models/labels.txt`.

### C. Convert to TensorFlow Lite
```bash
python ml_model/convert_to_tflite.py
```
- Converts `ml_model/models/model.keras` to `ml_model/models/model.tflite`.
- Verifies input/output tensor shapes.

### D. Run Accuracy Evaluation
```bash
python ml_model/accuracy_test.py
```
- Runs inference over all sample photos in `ml_model/sample_images/`.
- Outputs a clean summary table showing predicted labels, confidence percentages, and fallbacks.

---

## 5. Backend Integration

Aryaveer's FastAPI backend can directly import and invoke `predict_label`:

```python
from ml_model.predict import predict_label

result = predict_label("path/to/uploaded_image.jpg")
print(result)
```

### Response Formats:

**1. Confident Prediction ($\ge 0.60$):**
```python
{
    "label": "banana",
    "confidence": 0.9412
}
```

**2. Low Confidence Fallback ($< 0.60$):**
```python
{
    "label": None,
    "message": "Could not confidently identify this item"
}
```

**3. Error Handling (Missing image or file error):**
```python
{
    "label": None,
    "message": "Image not found at 'path/to/image.jpg'"
}
```

---

## 6. Preprocessing Specification

Both training (`train.py`) and inference (`predict.py`) use the **exact same MobileNetV2 preprocessing**:

1. Image is loaded and converted to standard 3-channel **RGB**.
2. Image is resized to **$224 \times 224$** pixels.
3. Pixel values ($[0, 255]$) are normalized to the range **$[-1.0, 1.0]$** using:
   $$\text{preprocessed} = \frac{\text{pixel}}{127.5} - 1.0$$
   *(Equivalent to `tf.keras.applications.mobilenet_v2.preprocess_input`).*

---

## 7. Model Performance & Limitations

- **Small Dataset & Class Imbalance:** Classes with fewer images (e.g., 15–20 vs 40+) may exhibit lower initial confidence. Transfer learning and light data augmentation mitigate this.
- **Real-World Variations:** Accuracy on user-uploaded camera photos can be influenced by background clutter, lighting variations, shadows, reflections, packaging, or unusual camera angles.
- **Safe Fallback:** The default confidence threshold of `0.60` ensures that ambiguous or uncertain images prompt the user gracefully rather than returning incorrect water-footprint calculations.
