#!/usr/bin/env python3
"""Convert trained Keras model to TensorFlow Lite (.tflite) format."""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MODELS_DIR = SCRIPT_DIR / "models"
DEFAULT_KERAS_PATH = MODELS_DIR / "model.keras"
DEFAULT_TFLITE_PATH = MODELS_DIR / "model.tflite"


def convert_keras_to_tflite(keras_model_path: Path = None, tflite_path: Path = None) -> Path:
    """Load trained Keras model and convert to TFLite format without lossy quantization."""
    # Auto-detect 17-class model if present
    if keras_model_path is None:
        keras_17class = MODELS_DIR / "model_17class.keras"
        keras_model_path = keras_17class if keras_17class.exists() else DEFAULT_KERAS_PATH

    if tflite_path is None:
        tflite_path = MODELS_DIR / "model_17class.tflite" if "17class" in str(keras_model_path) else DEFAULT_TFLITE_PATH

    if not keras_model_path.exists():
        raise FileNotFoundError(
            f"Keras model not found at {keras_model_path}. "
            "Please run `python ml_model/train.py` first to train and save the model."
        )

    import tensorflow as tf

    print(f"Loading Keras model from: {keras_model_path}...")
    model = tf.keras.models.load_model(str(keras_model_path))

    print("Converting model to TensorFlow Lite format...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    # Use standard default optimizations without aggressive quantization for hackathon reliability
    tflite_model = converter.convert()

    tflite_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

    # Also update active model.tflite if converting 17class model
    if tflite_path.name == "model_17class.tflite":
        with open(DEFAULT_TFLITE_PATH, "wb") as f:
            f.write(tflite_model)

    size_mb = tflite_path.stat().st_size / (1024 * 1024)
    print(f"Successfully converted and saved TFLite model to: {tflite_path} ({size_mb:.2f} MB)")
    if tflite_path.name == "model_17class.tflite":
        print(f"  -> Also updated active model at: {DEFAULT_TFLITE_PATH}")

    # Validate the exported TFLite model by initializing interpreter
    try:
        interpreter = tf.lite.Interpreter(model_path=str(tflite_path))
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        print("\nTFLite Model Validation:")
        print(f"  - Input shape:  {input_details[0]['shape']} (type: {input_details[0]['dtype'].__name__})")
        print(f"  - Output shape: {output_details[0]['shape']} (type: {output_details[0]['dtype'].__name__})")
        print("  - Status: Ready for inference\n")
    except Exception as e:
        print(f"[WARNING] TFLite validation check encountered an issue: {e}")

    return tflite_path


if __name__ == "__main__":
    try:
        convert_keras_to_tflite()
    except Exception as err:
        print(f"[ERROR] Conversion failed: {err}", file=sys.stderr)
        sys.exit(1)
