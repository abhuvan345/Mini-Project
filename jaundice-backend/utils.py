"""
Utility functions for the Jaundice Detection backend
"""

import logging
import numpy as np
from pathlib import Path
from PIL import Image
import cv2

logger = logging.getLogger(__name__)

def load_image(image_path, target_size=(224, 224)):
    """Load and preprocess an image from file"""
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        img_array = np.array(img, dtype=np.float32) / 255.0
        return img_array
    except Exception as e:
        logger.error("Error loading image %s: %s", image_path, str(e))
        raise

def load_batch(image_paths, target_size=(224, 224)):
    """Load a batch of images"""
    images = []
    for path in image_paths:
        img = load_image(path, target_size)
        images.append(img)
    return np.array(images)

def get_dataset_statistics(dataset_path):
    """Get statistics about the dataset"""
    dataset_path = Path(dataset_path)
    stats = {
        'train': {
            'normal': len(list((dataset_path / 'train' / 'train N').glob('*'))),
            'jaundice': len(list((dataset_path / 'train' / 'train J').glob('*')))
        },
        'validate': {
            'normal': len(list((dataset_path / 'validate' / 'validate N').glob('*'))),
            'jaundice': len(list((dataset_path / 'validate' / 'validate J').glob('*')))
        },
        'test': {
            'normal': len(list((dataset_path / 'test' / 'test N').glob('*'))),
            'jaundice': len(list((dataset_path / 'test' / 'test J').glob('*')))
        }
    }
    
    total_normal = sum(v['normal'] for v in stats.values())
    total_jaundice = sum(v['jaundice'] for v in stats.values())
    
    stats['total'] = {
        'normal': total_normal,
        'jaundice': total_jaundice,
        'total': total_normal + total_jaundice
    }
    
    return stats

def format_confidence(confidence):
    """Format confidence as percentage"""
    return f"{confidence * 100:.2f}%"
