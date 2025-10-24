"""
Setup and initialization script
Run this before first use
"""

import os
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup project environment"""
    logger.info("Setting up Jaundice Detection Backend...")
    
    # Create necessary directories
    directories = [
        Path("models"),
        Path("logs"),
        Path("datasets")
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        logger.info("✓ Directory ready: %s", directory)
    
    # Check for datasets
    dataset_path = Path("../datasets")
    if dataset_path.exists():
        logger.info("✓ Dataset found at: %s", dataset_path.absolute())
    else:
        logger.warning("! Dataset not found at: %s", dataset_path.absolute())
        logger.warning("  Please ensure datasets are in the parent directory")
    
    # Check for model
    model_path = Path("models/jaundice_detection_model.h5")
    if model_path.exists():
        logger.info("✓ Trained model found")
    else:
        logger.info("! Model not found. You need to train the model first:")
        logger.info("  Run: python train_model.py")
    
    logger.info("Setup complete!")

if __name__ == "__main__":
    setup_environment()
