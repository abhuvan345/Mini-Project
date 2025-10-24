"""
CLI tool for Jaundice Detection Backend
"""

import argparse
import logging
from pathlib import Path
import json
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from utils import get_dataset_statistics

def cmd_info(args):
    """Show model information"""
    metrics_path = Path("models/model_metrics.json")
    
    if not metrics_path.exists():
        logger.error("Model metrics not found. Train the model first.")
        return 1
    
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    print("\n" + "=" * 60)
    print("JAUNDICE DETECTION MODEL - INFORMATION")
    print("=" * 60)
    print(f"Model Version: {metrics.get('model_version', 'N/A')}")
    print(f"Training Date: {metrics.get('training_date', 'N/A')}")
    print(f"\nPerformance Metrics:")
    print(f"  Accuracy:  {metrics.get('accuracy', 0):.4f}")
    print(f"  Precision: {metrics.get('precision', 0):.4f}")
    print(f"  Recall:    {metrics.get('recall', 0):.4f}")
    print(f"  F1 Score:  {metrics.get('f1_score', 0):.4f}")
    print(f"\nConfusion Matrix (Test Set):")
    print(f"  True Negatives:  {metrics.get('true_negatives', 0)}")
    print(f"  False Positives: {metrics.get('false_positives', 0)}")
    print(f"  False Negatives: {metrics.get('false_negatives', 0)}")
    print(f"  True Positives:  {metrics.get('true_positives', 0)}")
    print(f"\nTest Samples: {metrics.get('total_samples', 0)}")
    print("=" * 60 + "\n")
    
    return 0

def cmd_stats(args):
    """Show dataset statistics"""
    dataset_path = Path("../datasets")
    
    if not dataset_path.exists():
        logger.error("Dataset not found at %s", dataset_path.absolute())
        return 1
    
    stats = get_dataset_statistics(dataset_path)
    
    print("\n" + "=" * 60)
    print("DATASET STATISTICS")
    print("=" * 60)
    for split, data in stats.items():
        print(f"\n{split.upper()}:")
        if split != 'total':
            print(f"  Normal:   {data.get('normal', 0)}")
            print(f"  Jaundice: {data.get('jaundice', 0)}")
            print(f"  Total:    {data.get('normal', 0) + data.get('jaundice', 0)}")
        else:
            print(f"  Normal:   {data.get('normal', 0)}")
            print(f"  Jaundice: {data.get('jaundice', 0)}")
            print(f"  Total:    {data.get('total', 0)}")
            print(f"  Balance:  Normal {data.get('normal', 0) / max(data.get('total', 1), 1) * 100:.1f}% / Jaundice {data.get('jaundice', 0) / max(data.get('total', 1), 1) * 100:.1f}%")
    print("=" * 60 + "\n")
    
    return 0

def cmd_test(args):
    """Test the model on a sample image"""
    try:
        import tensorflow as tf
        import numpy as np
        from PIL import Image
        
        model_path = Path("models/jaundice_detection_model.h5")
        if not model_path.exists():
            logger.error("Model not found. Train the model first.")
            return 1
        
        # Load model
        logger.info("Loading model...")
        model = tf.keras.models.load_model(str(model_path))
        
        # Load test image
        test_image_path = Path(args.image)
        if not test_image_path.exists():
            logger.error("Image not found: %s", test_image_path)
            return 1
        
        logger.info("Loading image: %s", test_image_path)
        img = Image.open(test_image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = img.resize((224, 224), Image.Resampling.LANCZOS)
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        prediction = model.predict(img_array, verbose=0)[0][0]
        confidence = max(prediction, 1 - prediction)
        predicted_class = 'JAUNDICE' if prediction > 0.5 else 'NORMAL'
        
        print("\n" + "=" * 60)
        print("PREDICTION RESULT")
        print("=" * 60)
        print(f"Image: {test_image_path.name}")
        print(f"Prediction: {predicted_class}")
        print(f"Confidence: {confidence * 100:.2f}%")
        print(f"  Jaundice Probability: {prediction * 100:.2f}%")
        print(f"  Normal Probability:   {(1 - prediction) * 100:.2f}%")
        print("=" * 60 + "\n")
        
        return 0
    
    except Exception as e:
        logger.error("Test failed: %s", str(e), exc_info=True)
        return 1

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Jaundice Detection Backend CLI"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Info command
    subparsers.add_parser('info', help='Show model information')
    
    # Stats command
    subparsers.add_parser('stats', help='Show dataset statistics')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test model on an image')
    test_parser.add_argument('image', help='Path to test image')
    
    args = parser.parse_args()
    
    if args.command == 'info':
        return cmd_info(args)
    elif args.command == 'stats':
        return cmd_stats(args)
    elif args.command == 'test':
        return cmd_test(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
