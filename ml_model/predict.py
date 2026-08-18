"""Image-label prediction with a confidence threshold fallback.

Inference pipeline for raw agricultural products using MobileNetV2 TFLite model.
Used directly by the FastAPI backend:
    from ml_model.predict import predict_label
    result = predict_label("path/to/image.jpg")
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import numpy as np
from PIL import Image

# Configurable defaults
CONFIDENCE_THRESHOLD = 0.60
INPUT_SIZE = (224, 224)

SCRIPT_DIR = Path(__file__).resolve().parent
MODELS_DIR = SCRIPT_DIR / "models"
DEFAULT_TFLITE_PATH = MODELS_DIR / "model_17class.tflite"
DEFAULT_LABELS_PATH = MODELS_DIR / "labels_17class.txt"

# Module-level singletons for lazy loading
_INTERPRETER = None
_LABELS: Optional[List[str]] = None
_INPUT_DETAILS = None
_OUTPUT_DETAILS = None


def _get_interpreter(model_path: Path = DEFAULT_TFLITE_PATH):
    """Load and cache the TFLite Interpreter singleton."""
    global _INTERPRETER, _INPUT_DETAILS, _OUTPUT_DETAILS

    if _INTERPRETER is not None:
        return _INTERPRETER

    if not model_path.exists():
        raise FileNotFoundError(
            f"TFLite model not found at '{model_path}'. "
            "Please train the model (`python ml_model/train.py`) and convert it (`python ml_model/convert_to_tflite.py`)."
        )

    # Support either tflite_runtime or full tensorflow
    try:
        import tflite_runtime.interpreter as tflite
        interpreter = tflite.Interpreter(model_path=str(model_path))
    except ImportError:
        try:
            import tensorflow as tf
            interpreter = tf.lite.Interpreter(model_path=str(model_path))
        except ImportError as e:
            raise ImportError(
                "Neither 'tensorflow' nor 'tflite_runtime' is installed. "
                "Please run `pip install -r ml_model/requirements.txt`."
            ) from e

    interpreter.allocate_tensors()
    _INPUT_DETAILS = interpreter.get_input_details()
    _OUTPUT_DETAILS = interpreter.get_output_details()
    _INTERPRETER = interpreter
    return _INTERPRETER


def _get_labels(labels_path: Path = DEFAULT_LABELS_PATH) -> List[str]:
    """Load and cache the class labels list singleton."""
    global _LABELS

    if _LABELS is not None:
        return _LABELS

    if not labels_path.exists():
        raise FileNotFoundError(
            f"Labels file not found at '{labels_path}'. "
            "Please run `python ml_model/train.py` to generate the labels file."
        )

    with open(labels_path, "r", encoding="utf-8") as f:
        labels = [line.strip() for line in f if line.strip()]

    if not labels:
        raise ValueError(f"Labels file '{labels_path}' is empty.")

    _LABELS = labels
    return _LABELS


def preprocess_image(image_path: str) -> np.ndarray:
    """Load image from path, convert to RGB, resize, and apply MobileNetV2 preprocessing.

    Preprocessing:
        Scales pixel values from [0, 255] to [-1, 1] via: (x / 127.5) - 1.0
        Exactly matches tf.keras.applications.mobilenet_v2.preprocess_input.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at '{image_path}'")

    try:
        # Validate structural integrity first
        with Image.open(image_path) as img:
            img.verify()
        with Image.open(image_path) as img:
            img_rgb = img.convert("RGB")
            img_resized = img_rgb.resize(INPUT_SIZE, Image.Resampling.BILINEAR)
    except Exception as err:
        raise ValueError(f"Corrupted or invalid image file: {err}") from err

    img_array = np.array(img_resized, dtype=np.float32)
    # MobileNetV2 preprocessing: [0, 255] -> [-1, 1]
    preprocessed = (img_array / 127.5) - 1.0

    # Add batch dimension: (1, 224, 224, 3)
    return np.expand_dims(preprocessed, axis=0)


def predict_label(image_path: str, confidence_threshold: float = CONFIDENCE_THRESHOLD) -> Dict[str, Any]:
    """Classify an agricultural product image and return predicted label with confidence.

    Args:
        image_path: Path to the image file.
        confidence_threshold: Minimum confidence required (default 0.60).

    Returns:
        Dict with 'label', 'confidence', and details if confident, or
        'label': None, 'reason', and 'message' if below threshold or on error.
    """
    try:
        interpreter = _get_interpreter()
        labels = _get_labels()

        input_data = preprocess_image(image_path)

        # Run inference
        interpreter.set_tensor(_INPUT_DETAILS[0]["index"], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(_OUTPUT_DETAILS[0]["index"])[0]

        # Extract top prediction
        top_idx = int(np.argmax(output_data))
        confidence = float(output_data[top_idx])

        if top_idx < 0 or top_idx >= len(labels):
            return {
                "label": None,
                "confidence": round(confidence, 4),
                "reason": "invalid_class_index",
                "message": f"Predicted index {top_idx} out of range for labels ({len(labels)} classes)."
            }

        predicted_class = labels[top_idx]

        tensor_meta = {
            "predicted_class_index": top_idx,
            "model_input_shape": _INPUT_DETAILS[0]["shape"].tolist(),
            "model_input_dtype": _INPUT_DETAILS[0]["dtype"].__name__,
            "output_tensor_shape": _OUTPUT_DETAILS[0]["shape"].tolist(),
        }

        if confidence >= confidence_threshold:
            return {
                "label": predicted_class,
                "predicted_label": predicted_class,
                "confidence": round(confidence, 4),
                **tensor_meta,
            }
        else:
            return {
                "label": None,
                "confidence": round(confidence, 4),
                "suggested_label": predicted_class,
                "reason": "low_confidence",
                "message": "I couldn't confidently identify this item. Try a clearer photo with the food centered in the frame.",
                **tensor_meta,
            }

    except FileNotFoundError as fnf_err:
        return {
            "label": None,
            "confidence": 0.0,
            "reason": "file_not_found",
            "message": str(fnf_err)
        }
    except ValueError as val_err:
        return {
            "label": None,
            "confidence": 0.0,
            "reason": "invalid_image",
            "message": str(val_err)
        }
    except Exception as err:
        return {
            "label": None,
            "confidence": 0.0,
            "reason": "inference_error",
            "message": f"Inference failed: {err}"
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ml_model/predict.py <path_to_image>")
        sys.exit(1)

    test_image = sys.argv[1]
    res = predict_label(test_image)
    print("Prediction Result:", res)
