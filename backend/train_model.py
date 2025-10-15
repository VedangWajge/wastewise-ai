import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
)
from datetime import datetime

# ============================================================================
# CONFIGURATION - Use relative paths
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Dataset is in the database/garbage_classification folder
DATASET_DIR = os.path.join(os.path.dirname(BASE_DIR), "database", "garbage_classification")
MODELS_DIR = os.path.join(BASE_DIR, "models")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Create necessary directories
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Model configuration
IMG_HEIGHT, IMG_WIDTH = 128, 128
BATCH_SIZE = 32  # Increased from 8
EPOCHS = 50  # Increased from 3
LEARNING_RATE = 0.001  # Increased from 0.0001
MODEL_NAME = "waste_classifier_model.h5"
MODEL_PATH = os.path.join(MODELS_DIR, MODEL_NAME)

# Train/Val/Test split ratios
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15

print("=" * 80)
print("WASTEWISE AI MODEL TRAINING")
print("=" * 80)
print(f"Dataset Directory: {DATASET_DIR}")
print(f"Model will be saved to: {MODEL_PATH}")
print(f"Image Size: {IMG_HEIGHT}x{IMG_WIDTH}")
print(f"Batch Size: {BATCH_SIZE}")
print(f"Max Epochs: {EPOCHS}")
print("=" * 80)

# ============================================================================
# 1. PREPARE DATA GENERATORS (NO FILE COPYING)
# ============================================================================
print("\n[1/6] Setting up data generators...")

# Enhanced data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.25,
    height_shift_range=0.25,
    shear_range=0.2,
    zoom_range=0.25,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest',
    validation_split=VAL_SPLIT  # Use built-in validation split
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Training generator
train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True,
    subset='training'  # Use training subset
)

# Validation generator
validation_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False,
    subset='validation'  # Use validation subset
)

# Get class information
num_classes = len(train_generator.class_indices)
class_names = list(train_generator.class_indices.keys())

print(f"[OK] Found {num_classes} classes: {class_names}")
print(f"[OK] Training samples: {train_generator.samples}")
print(f"[OK] Validation samples: {validation_generator.samples}")

# ============================================================================
# 2. BUILD IMPROVED CNN MODEL
# ============================================================================
print("\n[2/6] Building improved CNN model...")

model = Sequential([
    # First Convolutional Block
    Conv2D(32, (3, 3), activation='relu', padding='same',
           input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    BatchNormalization(),
    Conv2D(32, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Second Convolutional Block
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Third Convolutional Block
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Fourth Convolutional Block (NEW)
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Fully Connected Layers
    Flatten(),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("[OK] Model compiled successfully!")
print("\nModel Architecture:")
model.summary()

# ============================================================================
# 3. SETUP CALLBACKS
# ============================================================================
print("\n[3/6] Setting up training callbacks...")

# Early Stopping - stop if validation loss doesn't improve for 10 epochs
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

# Model Checkpoint - save best model
checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

# Learning Rate Reduction - reduce LR when validation loss plateaus
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-7,
    verbose=1
)

# TensorBoard - for visualization
tensorboard_callback = TensorBoard(
    log_dir=os.path.join(LOGS_DIR, f'run_{datetime.now().strftime("%Y%m%d_%H%M%S")}'),
    histogram_freq=1
)

callbacks = [early_stopping, checkpoint, reduce_lr, tensorboard_callback]

print("[OK] Callbacks configured:")
print("  - Early Stopping (patience=10)")
print("  - Model Checkpoint (save best)")
print("  - Reduce LR on Plateau")
print("  - TensorBoard logging")

# ============================================================================
# 4. TRAIN MODEL
# ============================================================================
print("\n[4/6] Starting model training...")
print("=" * 80)

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

print("=" * 80)
print(f"[OK] Training completed! Best model saved to: {MODEL_PATH}")

# ============================================================================
# 5. EVALUATE MODEL
# ============================================================================
print("\n[5/6] Evaluating model performance...")

# Load best model
from tensorflow.keras.models import load_model
best_model = load_model(MODEL_PATH)

# Evaluate on validation set
val_loss, val_accuracy = best_model.evaluate(validation_generator, verbose=0)
print(f"\nValidation Results:")
print(f"  Loss: {val_loss:.4f}")
print(f"  Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")

# Generate predictions
validation_generator.reset()
Y_pred = best_model.predict(validation_generator, verbose=1)
y_pred = np.argmax(Y_pred, axis=1)
y_true = validation_generator.classes

# Classification Report
print("\n" + "=" * 80)
print("CLASSIFICATION REPORT")
print("=" * 80)
report = classification_report(y_true, y_pred, target_names=class_names)
print(report)

# Save classification report
with open(os.path.join(RESULTS_DIR, 'classification_report.txt'), 'w') as f:
    f.write(f"Validation Accuracy: {val_accuracy:.4f}\n\n")
    f.write(report)

# ============================================================================
# 6. VISUALIZE RESULTS
# ============================================================================
print("\n[6/6] Generating visualizations...")

# Plot training history
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Accuracy plot
axes[0].plot(history.history['accuracy'], label='Training Accuracy')
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
axes[0].set_title('Model Accuracy Over Epochs')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

# Loss plot
axes[1].plot(history.history['loss'], label='Training Loss')
axes[1].plot(history.history['val_loss'], label='Validation Loss')
axes[1].set_title('Model Loss Over Epochs')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'training_history.png'), dpi=300)
print(f"[OK] Saved training history plot")

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'confusion_matrix.png'), dpi=300)
print(f"[OK] Saved confusion matrix plot")

# Save class indices for future reference
import json
class_indices_path = os.path.join(MODELS_DIR, 'class_indices.json')
with open(class_indices_path, 'w') as f:
    json.dump(train_generator.class_indices, f, indent=2)
print(f"[OK] Saved class indices to: {class_indices_path}")

print("\n" + "=" * 80)
print("TRAINING COMPLETE!")
print("=" * 80)
print(f"Model saved: {MODEL_PATH}")
print(f"Results saved: {RESULTS_DIR}")
print(f"TensorBoard logs: {LOGS_DIR}")
print("\nTo view TensorBoard:")
print(f"  tensorboard --logdir={LOGS_DIR}")
print("=" * 80)
