#!/usr/bin/env python3
"""Training script for Agricultural Product Image Classifier using MobileNetV2 Transfer Learning."""

import os
import sys
import shutil
import pathlib
from pathlib import Path
from typing import List, Tuple, Dict

from PIL import Image

# Ensure stdout prints immediately
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, "reconfigure") else None

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
TRAINING_DATA_DIR = SCRIPT_DIR / "training_data"
MODELS_DIR = SCRIPT_DIR / "models"
MODEL_KERAS_PATH = MODELS_DIR / "model.keras"
LABELS_PATH = MODELS_DIR / "labels.txt"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42
MAX_EPOCHS = 10
EARLY_STOPPING_PATIENCE = 3
LEARNING_RATE = 0.001

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def check_and_clean_dataset(dataset_dir: Path) -> Tuple[List[str], Dict[str, int], List[str]]:
    """Inspect dataset, validate image integrity, report counts and corrupted files."""
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Training data directory not found at: {dataset_dir}")

    # Discover classes dynamically (subdirectories only)
    class_dirs = sorted([d for d in dataset_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])
    if not class_dirs:
        raise ValueError(
            f"No class folders found in {dataset_dir}. "
            "Please create folders for each class (e.g. ml_model/training_data/banana/)."
        )

    class_names = [d.name for d in class_dirs]
    image_counts: Dict[str, int] = {}
    corrupted_files: List[str] = []

    print("\n" + "=" * 50)
    print("DATASET QUALITY PRE-FLIGHT CHECK")
    print("=" * 50)
    print(f"Dataset root: {dataset_dir}")
    print(f"Classes ({len(class_names)}):")
    for name in class_names:
        print(f"  - {name}")

    total_valid_images = 0

    for class_dir in class_dirs:
        cname = class_dir.name
        valid_count = 0
        for file_path in class_dir.iterdir():
            if file_path.is_file():
                if file_path.name.startswith("."):
                    continue
                if file_path.suffix.lower() not in VALID_EXTENSIONS:
                    print(f"  [SKIPPED non-image] {file_path.relative_to(dataset_dir)}")
                    continue

                # Verify image readability and structure
                try:
                    with Image.open(file_path) as img:
                        img.verify()
                    # Re-open to verify full decode without truncation issues
                    with Image.open(file_path) as img:
                        img.convert("RGB")
                    valid_count += 1
                except Exception as e:
                    corrupted_files.append(str(file_path))
                    print(f"  [CORRUPTED/UNREADABLE] Skipping {file_path.name} ({e})")
                    # Quarantine or rename corrupted file so Keras dataset loader won't fail
                    bad_target = file_path.with_suffix(file_path.suffix + ".corrupt")
                    try:
                        file_path.rename(bad_target)
                        print(f"    -> Renamed to {bad_target.name} to prevent loader crash.")
                    except OSError:
                        pass

        image_counts[cname] = valid_count
        total_valid_images += valid_count

    print("\nImage counts per class:")
    for cname, count in image_counts.items():
        print(f"  {cname}: {count}")

    print(f"\nTotal valid images: {total_valid_images}")
    if corrupted_files:
        print(f"Total corrupted/skipped files: {len(corrupted_files)}")
    else:
        print("No corrupted image files detected.")

    # Class imbalance check
    if image_counts:
        min_count = min(image_counts.values())
        max_count = max(image_counts.values())
        if min_count < 10:
            print(f"\n[WARNING] Some classes have fewer than 10 images (min: {min_count}). Accuracy may be affected.")
        if max_count > 0 and (min_count / max_count) < 0.5:
            print(f"[NOTE] Class imbalance detected: min={min_count}, max={max_count}. Transfer learning and augmentation will help mitigate this.")

    print("=" * 50 + "\n")

    if total_valid_images == 0:
        raise ValueError(
            f"No valid images found in {dataset_dir}. "
            "Add image files (.jpg, .png, etc.) inside class subfolders before training."
        )

    return class_names, image_counts, corrupted_files


def build_and_train():
    """Build MobileNetV2 transfer learning model and execute training."""
    # Lazy import TensorFlow so module can be inspected quickly without TF overhead
    import tensorflow as tf
    from tensorflow.keras import layers, models, callbacks

    print(f"TensorFlow Version: {tf.__version__}")

    # 1. Dataset quality check
    class_names, image_counts, _ = check_and_clean_dataset(TRAINING_DATA_DIR)
    num_classes = len(class_names)

    if num_classes < 2:
        raise ValueError(f"Need at least 2 classes to train classifier, found {num_classes}.")

    # 2. Create Training and Validation Datasets
    print("Loading training dataset (80%)...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        directory=str(TRAINING_DATA_DIR),
        labels="inferred",
        label_mode="categorical",
        class_names=class_names,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=RANDOM_SEED,
        shuffle=True,
    )

    print("Loading validation dataset (20%)...")
    val_ds = tf.keras.utils.image_dataset_from_directory(
        directory=str(TRAINING_DATA_DIR),
        labels="inferred",
        label_mode="categorical",
        class_names=class_names,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=RANDOM_SEED,
        shuffle=False,
    )

    # 3. Data Augmentation Pipeline (Applied to training set ONLY)
    data_augmentation = tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
        ],
        name="data_augmentation",
    )

    AUTOTUNE = tf.data.AUTOTUNE

    # Preprocessing: MobileNetV2 maps pixel values [0, 255] -> [-1, 1] via (x / 127.5) - 1.0
    def prepare_train_ds(ds):
        return (
            ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE)
            .map(lambda x, y: (tf.keras.applications.mobilenet_v2.preprocess_input(x), y), num_parallel_calls=AUTOTUNE)
            .prefetch(AUTOTUNE)
        )

    def prepare_val_ds(ds):
        return (
            ds.map(lambda x, y: (tf.keras.applications.mobilenet_v2.preprocess_input(x), y), num_parallel_calls=AUTOTUNE)
            .prefetch(AUTOTUNE)
        )

    train_ds_ready = prepare_train_ds(train_ds)
    val_ds_ready = prepare_val_ds(val_ds)

    # 4. Build Model with Pretrained MobileNetV2 Base
    print("\nInitializing MobileNetV2 base (pretrained on ImageNet)...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3),
        include_top=False,
        weights="imagenet",
    )
    # Freeze the base model
    base_model.trainable = False

    # Construct complete model (expects preprocessed [-1, 1] float32 inputs)
    inputs = tf.keras.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3), name="image_input")
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.Dropout(0.2, name="dropout")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="classification_head")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="agricultural_product_classifier")

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()

    # 5. Compute Class Weights for Imbalance Compensation
    total_samples = sum(image_counts.values())
    class_weights = {}
    print("\nClass Weights (Balanced):")
    for idx, name in enumerate(class_names):
        cnt = image_counts[name]
        weight = total_samples / (num_classes * cnt)
        class_weights[idx] = round(weight, 4)
        print(f"  [{idx:2d}] {name:<15}: weight={weight:.4f} (count: {cnt})")

    # 6. Training Callbacks & Paths
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save as model_17class.keras and labels_17class.txt
    output_keras_path = MODELS_DIR / "model_17class.keras"
    output_labels_path = MODELS_DIR / "labels_17class.txt"

    early_stopping = callbacks.EarlyStopping(
        monitor="val_loss",
        patience=EARLY_STOPPING_PATIENCE,
        restore_best_weights=True,
        verbose=1,
    )

    print("\n" + "=" * 50)
    print(f"STARTING 17-CLASS TRAINING (Max {MAX_EPOCHS} epochs, patience {EARLY_STOPPING_PATIENCE})")
    print("=" * 50)

    # 7. Fit Model with Class Weights
    history = model.fit(
        train_ds_ready,
        validation_data=val_ds_ready,
        epochs=MAX_EPOCHS,
        callbacks=[early_stopping],
        class_weight=class_weights,
        verbose=1,
    )

    # 8. Print Final Metrics Summary
    print("\n" + "=" * 50)
    print("TRAINING SUMMARY")
    print("=" * 50)
    for epoch, (loss, acc, val_loss, val_acc) in enumerate(
        zip(
            history.history.get("loss", []),
            history.history.get("accuracy", []),
            history.history.get("val_loss", []),
            history.history.get("val_accuracy", []),
        ),
        start=1,
    ):
        print(f"Epoch {epoch:2d}/{len(history.history['loss'])} - loss: {loss:.4f} - accuracy: {acc:.4f} - val_loss: {val_loss:.4f} - val_accuracy: {val_acc:.4f}")

    # 9. Save Trained Keras Model (model_17class.keras and active model.keras)
    print(f"\nSaving trained model to: {output_keras_path}")
    model.save(str(output_keras_path))
    # Also update model.keras for default pipeline while preserving model_11class_baseline.*
    model.save(str(MODEL_KERAS_PATH))

    # 10. Save Labels (labels_17class.txt and active labels.txt)
    print(f"Saving class labels to: {output_labels_path}")
    with open(output_labels_path, "w", encoding="utf-8") as f:
        for name in class_names:
            f.write(f"{name}\n")
    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        for name in class_names:
            f.write(f"{name}\n")

    print("\n" + "=" * 50)
    print("17-CLASS TRAINING COMPLETE!")
    print(f"  - Model saved to:  {output_keras_path} and {MODEL_KERAS_PATH}")
    print(f"  - Labels saved to: {output_labels_path} and {LABELS_PATH}")
    print(f"  - Baseline model:  ml_model/models/model_11class_baseline.tflite (Preserved)")
    print(f"  - Classes ({len(class_names)}): {', '.join(class_names)}")
    print("Next step: Run `python ml_model/convert_to_tflite.py` to generate model_17class.tflite")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    try:
        build_and_train()
    except Exception as err:
        print(f"\n[ERROR] Training failed: {err}", file=sys.stderr)
        sys.exit(1)
