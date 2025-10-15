import os
from pathlib import Path

# Base directory - where this config file is located
BASE_DIR = Path(__file__).resolve().parent

# Dataset configuration - points to database/garbage_classification
DATASET_DIR = os.getenv('DATASET_DIR', BASE_DIR.parent / 'database' / 'garbage_classification')
MODELS_DIR = os.getenv('MODELS_DIR', BASE_DIR / 'models')
LOGS_DIR = os.getenv('LOGS_DIR', BASE_DIR / 'logs')
RESULTS_DIR = os.getenv('RESULTS_DIR', BASE_DIR / 'results')
UPLOADS_DIR = os.getenv('UPLOADS_DIR', BASE_DIR / 'uploads')

# Model configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'waste_classifier_model.h5')
MODEL_PATH = MODELS_DIR / MODEL_NAME
CLASS_INDICES_PATH = MODELS_DIR / 'class_indices.json'

# Training hyperparameters
IMG_HEIGHT = int(os.getenv('IMG_HEIGHT', 128))
IMG_WIDTH = int(os.getenv('IMG_WIDTH', 128))
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 32))
EPOCHS = int(os.getenv('EPOCHS', 50))
LEARNING_RATE = float(os.getenv('LEARNING_RATE', 0.001))

# Data split ratios
VAL_SPLIT = float(os.getenv('VAL_SPLIT', 0.15))
TEST_SPLIT = float(os.getenv('TEST_SPLIT', 0.15))

# Database configuration
DB_PATH = os.getenv('DB_PATH', BASE_DIR / 'wastewise.db')

# Create directories if they don't exist
for directory in [MODELS_DIR, LOGS_DIR, RESULTS_DIR, UPLOADS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Waste categories (can be overridden by class_indices.json)
DEFAULT_WASTE_CATEGORIES = {
    0: 'battery',     1: 'biological',  2: 'brown-glass',
    3: 'cardboard',   4: 'clothes',     5: 'green-glass',
    6: 'metal',       7: 'paper',       8: 'plastic',
    9: 'shoes',      10: 'trash',      11: 'white-glass'
}
