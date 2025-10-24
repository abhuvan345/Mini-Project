"""
Flask API for Jaundice Detection
Production-grade REST API for serving predictions
"""

import os
import logging
import json
from pathlib import Path
from datetime import datetime
from functools import lru_cache

import numpy as np
import cv2
from PIL import Image
import io

import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv('PORT', 5000))
MODEL_PATH = os.getenv('MODEL_PATH', 'models/jaundice_detection_model.h5')
IMG_SIZE = 224
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif'}

# Flask app
app = Flask(__name__)
CORS(app)

# Global model cache
_model = None
_metrics = None

def get_model():
    """Load model lazily"""
    global _model
    if _model is None:
        logger.info("Loading model from: %s", MODEL_PATH)
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please train the model first.")
        _model = tf.keras.models.load_model(MODEL_PATH)
        logger.info("Model loaded successfully")
    return _model

def get_metrics():
    """Load model metrics"""
    global _metrics
    if _metrics is None:
        metrics_path = Path(MODEL_PATH).parent / "model_metrics.json"
        if metrics_path.exists():
            with open(metrics_path, 'r') as f:
                _metrics = json.load(f)
        else:
            _metrics = {}
    return _metrics

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_data):
    """Preprocess image for model prediction"""
    try:
        # Load image
        img = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to model input size
        img = img.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        logger.error("Error preprocessing image: %s", str(e))
        raise ValueError(f"Invalid image: {str(e)}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        model = get_model()
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.now().isoformat(),
            'model_loaded': model is not None
        }), 200
    except Exception as e:
        logger.error("Health check failed: %s", str(e))
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    try:
        metrics = get_metrics()
        model = get_model()
        
        response = {
            'model_name': 'jaundice_detection_model',
            'version': '1.0',
            'input_shape': [IMG_SIZE, IMG_SIZE, 3],
            'classes': ['normal', 'jaundice'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Add metrics if available
        if metrics:
            response.update({
                'accuracy': metrics.get('accuracy', 0),
                'precision': metrics.get('precision', 0),
                'recall': metrics.get('recall', 0),
                'f1_score': metrics.get('f1_score', 0),
                'training_date': metrics.get('training_date', ''),
                'test_samples': metrics.get('total_samples', 0)
            })
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error("Error getting model info: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict jaundice from uploaded image"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Read image data
        image_data = file.read()
        
        # Preprocess image
        img_array = preprocess_image(image_data)
        
        # Get prediction
        model = get_model()
        prediction = model.predict(img_array, verbose=0)[0][0]
        
        # Prepare response
        confidence = float(max(prediction, 1 - prediction))
        predicted_class = 'jaundice' if prediction > 0.5 else 'normal'
        
        response = {
            'prediction': predicted_class,
            'confidence': confidence,
            'probability_jaundice': float(prediction),
            'probability_normal': float(1 - prediction),
            'timestamp': datetime.now().isoformat(),
            'model_version': '1.0'
        }
        
        logger.info("Prediction: %s (confidence: %.2f%%)", predicted_class, confidence * 100)
        
        return jsonify(response), 200
    
    except ValueError as e:
        logger.warning("Validation error: %s", str(e))
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        logger.error("Prediction error: %s", str(e), exc_info=True)
        return jsonify({'error': 'Prediction failed: ' + str(e)}), 500

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """Batch predict from multiple images"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if not files:
            return jsonify({'error': 'No files provided'}), 400
        
        results = []
        model = get_model()
        
        for file in files:
            try:
                if not allowed_file(file.filename):
                    results.append({
                        'filename': file.filename,
                        'status': 'error',
                        'error': 'Invalid file type'
                    })
                    continue
                
                image_data = file.read()
                img_array = preprocess_image(image_data)
                
                prediction = model.predict(img_array, verbose=0)[0][0]
                confidence = float(max(prediction, 1 - prediction))
                predicted_class = 'jaundice' if prediction > 0.5 else 'normal'
                
                results.append({
                    'filename': file.filename,
                    'status': 'success',
                    'prediction': predicted_class,
                    'confidence': confidence,
                    'probability_jaundice': float(prediction),
                    'probability_normal': float(1 - prediction)
                })
            
            except Exception as e:
                logger.error("Error processing file %s: %s", file.filename, str(e))
                results.append({
                    'filename': file.filename,
                    'status': 'error',
                    'error': str(e)
                })
        
        return jsonify({
            'results': results,
            'total': len(files),
            'successful': sum(1 for r in results if r['status'] == 'success'),
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error("Batch prediction error: %s", str(e), exc_info=True)
        return jsonify({'error': 'Batch prediction failed: ' + str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get model statistics"""
    try:
        metrics = get_metrics()
        
        if not metrics:
            return jsonify({'error': 'Model metrics not available'}), 404
        
        response = {
            'model_name': 'jaundice_detection_model',
            'version': '1.0',
            'training_date': metrics.get('training_date', ''),
            'metrics': {
                'accuracy': metrics.get('accuracy', 0),
                'precision': metrics.get('precision', 0),
                'recall': metrics.get('recall', 0),
                'f1_score': metrics.get('f1_score', 0)
            },
            'confusion_matrix': {
                'true_negatives': metrics.get('true_negatives', 0),
                'false_positives': metrics.get('false_positives', 0),
                'false_negatives': metrics.get('false_negatives', 0),
                'true_positives': metrics.get('true_positives', 0)
            },
            'test_samples': metrics.get('total_samples', 0)
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error("Error getting stats: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error("Internal server error: %s", str(error))
    return jsonify({'error': 'Internal server error'}), 500

@app.before_request
def before_request():
    """Log incoming requests"""
    logger.debug("%s %s", request.method, request.path)

@app.after_request
def after_request(response):
    """Log response status"""
    logger.debug("Response status: %d", response.status_code)
    return response

if __name__ == '__main__':
    try:
        logger.info("=" * 80)
        logger.info("Starting Jaundice Detection API Server")
        logger.info("=" * 80)
        logger.info("Loading model from: %s", MODEL_PATH)
        
        # Pre-load model
        get_model()
        get_metrics()
        
        logger.info("Server starting on http://localhost:%d", PORT)
        logger.info("API Documentation available at http://localhost:%d/api/docs", PORT)
        
        app.run(
            host='0.0.0.0',
            port=PORT,
            debug=False,
            threaded=True
        )
    
    except Exception as e:
        logger.error("Failed to start server: %s", str(e), exc_info=True)
        raise
