# Quick Start Guide

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- At least 8GB RAM (for model training)

## Installation

### 1. Create Virtual Environment

```bash
cd jaundice-backend
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Project

```bash
python setup.py
```

This will create necessary directories and check for datasets.

## Training the Model

```bash
python train_model.py
```

**What happens:**

- Loads images from `../datasets/` folder
- Trains a CNN model for 50 epochs (Phase 1) + 20 epochs fine-tuning (Phase 2)
- Saves model to `models/jaundice_detection_model.h5`
- Generates performance metrics
- Generates tensorboard logs

**Training Time:** ~30-60 minutes depending on your hardware

**Output:**

```
Training samples: 400+
Validation samples: 100+
Test samples: 100+

Training starts...
Epoch 1/50 - [training progress]
...
Model saved to: models/jaundice_detection_model.h5
Metrics saved to: models/model_metrics.json
```

## Running the API Server

```bash
python app.py
```

**Server Output:**

```
...
Loading model from: models/jaundice_detection_model.h5
Model loaded successfully
Server starting on http://localhost:5000
```

The API is now ready for predictions!

## Testing the Model

### Using CLI

```bash
# Show model info
python cli.py info

# Show dataset statistics
python cli.py stats

# Test on an image
python cli.py test path/to/image.jpg
```

### Using cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Get model info
curl http://localhost:5000/api/model/info

# Make prediction
curl -X POST http://localhost:5000/api/predict \
  -F "file=@path/to/image.jpg"
```

### Using Python

```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/predict', files=files)
    result = response.json()

print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Project Structure

```
jaundice-backend/
├── app.py                    # Flask API server
├── train_model.py            # Model training script
├── cli.py                    # Command-line interface
├── utils.py                  # Utility functions
├── setup.py                  # Project setup
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── models/                   # Trained models
│   ├── jaundice_detection_model.h5
│   └── model_metrics.json
├── logs/                     # Training logs
│   └── tensorboard/
├── README.md                 # Project readme
├── API_DOCUMENTATION.md      # API reference
├── FRONTEND_INTEGRATION.md   # Frontend guide
└── QUICK_START.md           # This file
```

## Common Commands

```bash
# Train model
python train_model.py

# Start API server
python app.py

# View model info
python cli.py info

# View dataset statistics
python cli.py stats

# Test prediction on an image
python cli.py test image.jpg

# View model info via API
curl http://localhost:5000/api/model/info

# View API stats
curl http://localhost:5000/api/stats

# Make a prediction
curl -X POST http://localhost:5000/api/predict -F "file=@image.jpg"
```

## Environment Variables

Edit `.env` to configure:

```env
FLASK_ENV=production          # Flask environment
FLASK_DEBUG=False             # Debug mode
PORT=5000                     # API port
MODEL_PATH=models/jaundice_detection_model.h5  # Model path
LOG_LEVEL=INFO                # Log level
```

## Troubleshooting

### Model training fails

- Ensure dataset exists at `../datasets/`
- Check disk space (needs ~2GB for training)
- Check RAM (needs ~8GB)

### API won't start

- Ensure model is trained: `python train_model.py`
- Check if port 5000 is already in use
- Try different port: Edit `.env` or `app.py`

### CORS errors in frontend

- Backend has CORS enabled by default
- Check frontend `VITE_API_URL` configuration

### Prediction errors

- Ensure image format is supported (jpg, png, etc.)
- Check image is not corrupted
- View server logs for details

## Performance Metrics

After training, view metrics with:

```bash
python cli.py info
```

Expected performance (on test set):

- Accuracy: 90-95%
- Precision: 85-92%
- Recall: 88-96%
- F1 Score: 88-94%

## Next Steps

1. **Train the Model**: `python train_model.py`
2. **Start the API**: `python app.py`
3. **Integrate with Frontend**: See `FRONTEND_INTEGRATION.md`
4. **Deploy**: Use Docker/Cloud service

## Support

For issues or questions, check:

- `API_DOCUMENTATION.md` - Full API reference
- `FRONTEND_INTEGRATION.md` - Frontend integration guide
- Server logs in `logs/` directory
- Model metrics in `models/model_metrics.json`
