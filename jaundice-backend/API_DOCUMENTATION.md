# API Documentation

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Health Check

**GET** `/api/health`

Check if the API is running and model is loaded.

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2024-10-24T10:30:00.000000",
  "model_loaded": true
}
```

**Status Codes:**

- `200` - OK
- `500` - Server error

---

### 2. Model Information

**GET** `/api/model/info`

Get information about the trained model.

**Response:**

```json
{
  "model_name": "jaundice_detection_model",
  "version": "1.0",
  "input_shape": [224, 224, 3],
  "classes": ["normal", "jaundice"],
  "timestamp": "2024-10-24T10:30:00.000000",
  "accuracy": 0.92,
  "precision": 0.9,
  "recall": 0.94,
  "f1_score": 0.92,
  "training_date": "2024-10-24T09:15:30.123456",
  "test_samples": 150
}
```

**Status Codes:**

- `200` - OK
- `500` - Server error

---

### 3. Make Prediction

**POST** `/api/predict`

Upload an image and get jaundice detection prediction.

**Request:**

```
Content-Type: multipart/form-data

Parameters:
- file (required): Image file (jpg, jpeg, png, bmp, gif)
```

**Response:**

```json
{
  "prediction": "jaundice",
  "confidence": 0.95,
  "probability_jaundice": 0.95,
  "probability_normal": 0.05,
  "timestamp": "2024-10-24T10:30:00.000000",
  "model_version": "1.0"
}
```

**Status Codes:**

- `200` - Success
- `400` - Bad request (invalid file)
- `500` - Server error

**Example using cURL:**

```bash
curl -X POST http://localhost:5000/api/predict \
  -F "file=@path/to/image.jpg"
```

**Example using Python:**

```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/predict', files=files)
    result = response.json()
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}")
```

**Example using JavaScript/React:**

```javascript
async function predictImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:5000/api/predict", {
    method: "POST",
    body: formData,
  });

  return await response.json();
}

// Usage
const fileInput = document.getElementById("imageInput");
const file = fileInput.files[0];
const result = await predictImage(file);
console.log(`Prediction: ${result.prediction}`);
console.log(`Confidence: ${(result.confidence * 100).toFixed(2)}%`);
```

---

### 4. Batch Prediction

**POST** `/api/batch-predict`

Upload multiple images and get predictions for all.

**Request:**

```
Content-Type: multipart/form-data

Parameters:
- files (required): Multiple image files
```

**Response:**

```json
{
  "results": [
    {
      "filename": "image1.jpg",
      "status": "success",
      "prediction": "jaundice",
      "confidence": 0.95,
      "probability_jaundice": 0.95,
      "probability_normal": 0.05
    },
    {
      "filename": "image2.jpg",
      "status": "success",
      "prediction": "normal",
      "confidence": 0.88,
      "probability_jaundice": 0.12,
      "probability_normal": 0.88
    }
  ],
  "total": 2,
  "successful": 2,
  "timestamp": "2024-10-24T10:30:00.000000"
}
```

**Status Codes:**

- `200` - OK (even if some files failed)
- `400` - Bad request
- `500` - Server error

---

### 5. Model Statistics

**GET** `/api/stats`

Get detailed model performance statistics.

**Response:**

```json
{
  "model_name": "jaundice_detection_model",
  "version": "1.0",
  "training_date": "2024-10-24T09:15:30.123456",
  "metrics": {
    "accuracy": 0.92,
    "precision": 0.9,
    "recall": 0.94,
    "f1_score": 0.92
  },
  "confusion_matrix": {
    "true_negatives": 70,
    "false_positives": 5,
    "false_negatives": 3,
    "true_positives": 72
  },
  "test_samples": 150
}
```

**Status Codes:**

- `200` - OK
- `404` - Metrics not available
- `500` - Server error

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

**Common Errors:**

| Status | Error Message         | Solution                        |
| ------ | --------------------- | ------------------------------- |
| 400    | No file provided      | Include a file in the request   |
| 400    | Empty filename        | Ensure file has a valid name    |
| 400    | Invalid file type     | Use jpg, jpeg, png, bmp, or gif |
| 500    | Prediction failed     | Check server logs               |
| 500    | Internal server error | Restart the server              |

---

## Request Examples

### JavaScript/Fetch

```javascript
// Single image prediction
async function predict(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:5000/api/predict", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

// Get model info
async function getModelInfo() {
  const response = await fetch("http://localhost:5000/api/model/info");
  return await response.json();
}

// Health check
async function healthCheck() {
  const response = await fetch("http://localhost:5000/api/health");
  return await response.json();
}
```

### Python/Requests

```python
import requests

# Single prediction
def predict_image(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'http://localhost:5000/api/predict',
            files=files
        )
    return response.json()

# Batch prediction
def batch_predict(image_paths):
    files = []
    for path in image_paths:
        files.append(('files', open(path, 'rb')))

    response = requests.post(
        'http://localhost:5000/api/batch-predict',
        files=files
    )
    return response.json()

# Get stats
def get_stats():
    response = requests.get('http://localhost:5000/api/stats')
    return response.json()
```

---

## CORS Policy

The API has CORS enabled for all origins. You can make requests from any domain.

If you need to restrict CORS, modify the `CORS(app)` configuration in `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## Rate Limiting

Currently, the API has no rate limiting. For production, consider adding:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## Response Times

Typical response times (on modern hardware):

- Health Check: < 10ms
- Model Info: < 10ms
- Single Prediction: 50-150ms (depends on image size)
- Batch Prediction (10 images): 500ms - 1.5s

---

## Notes

1. Model loads on first request and is cached in memory
2. Images are automatically resized to 224x224
3. Predictions are real-time, no caching
4. Confidence is always between 0 and 1
5. All timestamps are in ISO 8601 format
