"""
Configuration module for Jaundice Detection Backend
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
DATASETS_DIR = PROJECT_ROOT.parent / "datasets"

# Flask Configuration
FLASK_ENV = os.getenv("FLASK_ENV", "production")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "0.0.0.0")

# Model Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "models/jaundice_detection_model.h5")
FULL_MODEL_PATH = MODELS_DIR / "jaundice_detection_model.h5"
MODEL_METRICS_PATH = MODELS_DIR / "model_metrics.json"
IMG_SIZE = 224
BATCH_SIZE = 32

# Prediction Configuration
PREDICTION_THRESHOLD = 0.5
ALLOWED_FILE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "gif"}
MAX_FILE_SIZE_MB = 10

# Training Configuration
TRAINING_EPOCHS = 50
FINE_TUNE_EPOCHS = 20
LEARNING_RATE = 0.001
FINE_TUNE_LEARNING_RATE = 0.0001
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Model Classes
CLASSES = ["normal", "jaundice"]
CLASS_MAPPING = {"normal": 0, "jaundice": 1}
REVERSE_CLASS_MAPPING = {0: "normal", 1: "jaundice"}

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

# Ensure directories exist
MODELS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Configuration dictionary for easy access
CONFIG = {
    "flask": {
        "env": FLASK_ENV,
        "debug": FLASK_DEBUG,
        "port": PORT,
        "host": HOST,
    },
    "model": {
        "path": FULL_MODEL_PATH,
        "metrics_path": MODEL_METRICS_PATH,
        "img_size": IMG_SIZE,
        "classes": CLASSES,
        "threshold": PREDICTION_THRESHOLD,
    },
    "training": {
        "epochs": TRAINING_EPOCHS,
        "fine_tune_epochs": FINE_TUNE_EPOCHS,
        "learning_rate": LEARNING_RATE,
        "fine_tune_learning_rate": FINE_TUNE_LEARNING_RATE,
        "batch_size": BATCH_SIZE,
    },
    "paths": {
        "models": str(MODELS_DIR),
        "logs": str(LOGS_DIR),
        "datasets": str(DATASETS_DIR),
    },
}


def print_config():
    """Print current configuration"""
    import json
    print(json.dumps(CONFIG, indent=2))


if __name__ == "__main__":
    print_config()
