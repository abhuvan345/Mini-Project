"""
Verification script to check backend setup
Run this to ensure everything is properly configured
"""

import os
import sys
from pathlib import Path
import json

def check_file_exists(filepath, description):
    """Check if a file exists"""
    path = Path(filepath)
    status = "✓" if path.exists() else "✗"
    print(f"  {status} {description}")
    return path.exists()

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    path = Path(dirpath)
    status = "✓" if path.exists() else "✗"
    print(f"  {status} {description}")
    return path.exists()

def check_python_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"  ✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"  ✗ {package_name} is NOT installed")
        return False

def main():
    print("=" * 70)
    print("JAUNDICE DETECTION BACKEND - VERIFICATION CHECKLIST")
    print("=" * 70)
    
    all_ok = True
    
    # Check files
    print("\n📁 PROJECT FILES:")
    files_to_check = [
        ("app.py", "API Server"),
        ("train_model.py", "Training Script"),
        ("utils.py", "Utilities"),
        ("config.py", "Configuration"),
        ("cli.py", "CLI Tool"),
        ("requirements.txt", "Dependencies"),
        (".env", "Environment Variables"),
        ("README.md", "Documentation"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    # Check directories
    print("\n📂 PROJECT DIRECTORIES:")
    dirs_to_check = [
        ("models", "Models Directory"),
        ("logs", "Logs Directory"),
    ]
    
    for dirpath, description in dirs_to_check:
        if not check_directory_exists(dirpath, description):
            all_ok = False
    
    # Check dataset
    print("\n📊 DATASET:")
    datasets_to_check = [
        ("../datasets/train", "Training Dataset"),
        ("../datasets/validate", "Validation Dataset"),
        ("../datasets/test", "Test Dataset"),
    ]
    
    for dirpath, description in datasets_to_check:
        if not check_directory_exists(dirpath, description):
            all_ok = False
    
    # Check Python packages
    print("\n🐍 PYTHON PACKAGES:")
    packages_to_check = [
        "flask",
        "flask_cors",
        "tensorflow",
        "keras",
        "numpy",
        "pillow",
        "cv2",
        "sklearn",
    ]
    
    for package in packages_to_check:
        if not check_python_package(package):
            all_ok = False
    
    # Check model
    print("\n🤖 TRAINED MODEL:")
    model_path = Path("models/jaundice_detection_model.h5")
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ Model exists ({size_mb:.1f} MB)")
        
        # Check metrics
        metrics_path = Path("models/model_metrics.json")
        if metrics_path.exists():
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            print(f"  ✓ Metrics available")
            print(f"    - Accuracy: {metrics.get('accuracy', 'N/A'):.4f}")
            print(f"    - Precision: {metrics.get('precision', 'N/A'):.4f}")
            print(f"    - Recall: {metrics.get('recall', 'N/A'):.4f}")
            print(f"    - F1 Score: {metrics.get('f1_score', 'N/A'):.4f}")
        else:
            print(f"  ✗ Metrics file not found")
            all_ok = False
    else:
        print(f"  ✗ Model not found (run: python train_model.py)")
        all_ok = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok and model_path.exists():
        print("✓ ALL CHECKS PASSED - System is ready!")
        print("\nNext steps:")
        print("1. Start the API: python app.py")
        print("2. Test endpoint: curl http://localhost:5000/api/health")
        print("3. Integrate frontend: See FRONTEND_INTEGRATION.md")
    elif all_ok and not model_path.exists():
        print("⚠ PARTIAL - Files ready, model needs training")
        print("\nNext steps:")
        print("1. Train the model: python train_model.py")
        print("2. Start the API: python app.py")
    else:
        print("✗ ISSUES FOUND - Please fix above problems")
        print("\nCommon fixes:")
        print("1. Install packages: pip install -r requirements.txt")
        print("2. Check dataset path: ../datasets/")
        print("3. Train model: python train_model.py")
    
    print("=" * 70)
    
    return 0 if all_ok and model_path.exists() else 1

if __name__ == "__main__":
    sys.exit(main())
