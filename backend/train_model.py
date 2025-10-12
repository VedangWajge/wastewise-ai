# train_basic_cnn.py
import os
import shutil
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, LambdaCallback
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# -----------------------------
# Parameters
# -----------------------------
DATASET_DIR = r"D:\WasteWiseAi\wastewise-ai\backend\dataset"
TRAIN_DIR = r"D:\WasteWiseAi\wastewise-ai\backend\train_dataset"
TEST_DIR = r"D:\WasteWiseAi\wastewise-ai\backend\test_dataset"
IMG_HEIGHT, IMG_WIDTH = 128, 128   # smaller for faster training
BATCH_SIZE = 8
EPOCHS = 20  # maximum, but we will stop at 3
TEST_SPLIT = 0.2
MODEL_PATH = r"D:\WasteWiseAi\wastewise-ai\backend\basic_cnn_model.h5"

# -----------------------------
# 1️⃣ Prepare train/test split
# -----------------------------
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

categories = os.listdir(DATASET_DIR)

for category in categories:
    category_path = os.path.join(DATASET_DIR, category)
    images = os.listdir(category_path)
    train_imgs, test_imgs = train_test_split(images, test_size=TEST_SPLIT, random_state=42)

    os.makedirs(os.path.join(TRAIN_DIR, category), exist_ok=True)
    os.makedirs(os.path.join(TEST_DIR, category), exist_ok=True)

    for img in train_imgs:
        shutil.copy(os.path.join(category_path, img), os.path.join(TRAIN_DIR, category, img))
    for img in test_imgs:
        shutil.copy(os.path.join(category_path, img), os.path.join(TEST_DIR, category, img))

print("✅ Train/test split done!")

# -----------------------------
# 2️⃣ Image Data Generators
# -----------------------------
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

validation_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# -----------------------------
# 3️⃣ Build Basic CNN Model
# -----------------------------
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(categories), activation='softmax')
])

model.compile(optimizer=Adam(0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("✅ Model compiled!")

# -----------------------------
# 4️⃣ Callbacks
# -----------------------------
# Stop training exactly at 3 epochs
stop_at_epoch_3 = LambdaCallback(
    on_epoch_end=lambda epoch, logs: setattr(model, 'stop_training', True) if epoch + 1 >= 3 else None
)

checkpoint = ModelCheckpoint(MODEL_PATH, save_best_only=True, save_freq='epoch')

# -----------------------------
# 5️⃣ Train Model
# -----------------------------
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=[stop_at_epoch_3, checkpoint]
)

print(f"✅ Training stopped and best model saved at {MODEL_PATH}")

# -----------------------------
# 6️⃣ Evaluate Model
# -----------------------------
validation_generator.reset()
Y_pred = model.predict(validation_generator)
y_pred = np.argmax(Y_pred, axis=1)
y_true = validation_generator.classes

# Classification report
report = classification_report(y_true, y_pred, target_names=categories)
print("📊 Classification Report:\n")
print(report)
