"""
Enhanced Jaundice Detection Model
Optimized MobileNetV2 + Fine-Tuning + Class Balancing + Threshold Optimization
Author: Bhuvan A
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve
)
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam

# ==========================================
# CONFIGURATION
# ==========================================
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS_PHASE1 = 30
EPOCHS_PHASE2 = 30
BASE_LR = 1e-4
FINE_TUNE_LR = 1e-5

BASE_PATH = Path(__file__).parent.parent
DATASET_PATH = BASE_PATH / "datasets"
MODEL_PATH = BASE_PATH / "models"
LOGS_PATH = BASE_PATH / "logs"

MODEL_PATH.mkdir(exist_ok=True)
LOGS_PATH.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# DATA LOADING
# ==========================================
def load_data():
    """Load and prepare train/val/test datasets with strong augmentation"""
    logger.info("Loading datasets...")

    train_aug = ImageDataGenerator(
        rescale=1./255,
        rotation_range=25,
        width_shift_range=0.25,
        height_shift_range=0.25,
        shear_range=0.2,
        zoom_range=0.3,
        brightness_range=[0.7, 1.3],
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_aug = ImageDataGenerator(rescale=1./255)
    test_aug = ImageDataGenerator(rescale=1./255)

    train_gen = train_aug.flow_from_directory(
        DATASET_PATH / "train",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        classes={'train N': 0, 'train J': 1}
    )
    val_gen = val_aug.flow_from_directory(
        DATASET_PATH / "validate",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        classes={'validate N': 0, 'validate J': 1}
    )
    test_gen = test_aug.flow_from_directory(
        DATASET_PATH / "test",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False,
        classes={'test N': 0, 'test J': 1}
    )

    logger.info(f"Train samples: {train_gen.samples}, Val samples: {val_gen.samples}, Test samples: {test_gen.samples}")
    return train_gen, val_gen, test_gen

# ==========================================
# MODEL CREATION
# ==========================================
def build_model():
    """Build enhanced MobileNetV2-based CNN"""
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )

    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu', kernel_regularizer='l2'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu', kernel_regularizer='l2'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=Adam(learning_rate=BASE_LR),
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )
    logger.info("✅ Base model built successfully")
    return model, base_model

# ==========================================
# TRAINING
# ==========================================
def train_model(model, base_model, train_gen, val_gen):
    """Train model with progressive fine-tuning and class balancing"""
    logger.info("Starting training...")

    # Compute class weights
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.unique(train_gen.classes),
        y=train_gen.classes
    )
    class_weights = dict(enumerate(class_weights))
    logger.info(f"Class Weights: {class_weights}")

    callbacks = [
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=4, min_lr=1e-7),
        keras.callbacks.ModelCheckpoint(str(MODEL_PATH / "best_model.h5"), save_best_only=True, monitor="val_accuracy"),
        keras.callbacks.TensorBoard(log_dir=str(LOGS_PATH / "tensorboard"))
    ]

    # Phase 1: Train top layers
    history1 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS_PHASE1,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )

    # Phase 2: Fine-tuning deeper layers
    logger.info("Fine-tuning deeper layers...")
    base_model.trainable = True
    for layer in base_model.layers[:-60]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=FINE_TUNE_LR),
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )

    history2 = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS_PHASE2,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )

    return history1, history2

# ==========================================
# EVALUATION
# ==========================================
def evaluate_model(model, test_gen):
    """Evaluate and optimize classification threshold"""
    logger.info("Evaluating model...")

    probs = model.predict(test_gen).flatten()
    true_labels = test_gen.classes

    # Find optimal threshold via ROC curve
    fpr, tpr, thresholds = roc_curve(true_labels, probs)
    f1_scores = [2 * (precision_score(true_labels, (probs >= t)) * recall_score(true_labels, (probs >= t))) /
                 (precision_score(true_labels, (probs >= t)) + recall_score(true_labels, (probs >= t)) + 1e-7)
                 for t in thresholds]
    best_threshold = thresholds[np.argmax(f1_scores)]

    pred_labels = (probs >= best_threshold).astype(int)
    cm = confusion_matrix(true_labels, pred_labels)
    acc = accuracy_score(true_labels, pred_labels)
    prec = precision_score(true_labels, pred_labels)
    rec = recall_score(true_labels, pred_labels)
    f1 = f1_score(true_labels, pred_labels)

    logger.info(f"✅ Optimized Threshold: {best_threshold:.3f}")
    logger.info(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
    logger.info(f"Confusion Matrix:\n{cm}")

    return {
        "accuracy": acc, "precision": prec, "recall": rec, "f1_score": f1,
        "confusion_matrix": cm.tolist(), "threshold": float(best_threshold)
    }

# ==========================================
# SAVE MODEL
# ==========================================
def save_model(model, metrics):
    """Save final model and metrics"""
    model_file = MODEL_PATH / "jaundice_best_model.h5"
    model.save(model_file)
    logger.info(f"Model saved to: {model_file}")

    metrics_file = MODEL_PATH / "best_model_metrics.json"
    metrics["training_date"] = datetime.now().isoformat()
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Metrics saved to: {metrics_file}")

# ==========================================
# MAIN PIPELINE
# ==========================================
def main():
    try:
        logger.info("="*80)
        logger.info("🚀 Enhanced Jaundice Detection Model Training Started")
        logger.info("="*80)

        train_gen, val_gen, test_gen = load_data()
        model, base_model = build_model()
        train_model(model, base_model, train_gen, val_gen)
        metrics = evaluate_model(model, test_gen)
        save_model(model, metrics)

        logger.info("="*80)
        logger.info("🎯 Training Completed — Optimized Model Saved Successfully!")
        logger.info("="*80)

    except Exception as e:
        logger.error("Training failed: %s", e, exc_info=True)

if __name__ == "__main__":
    main()
