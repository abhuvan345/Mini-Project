# Frontend Integration Guide

This guide explains how to integrate the Jaundice Detection backend API with the React frontend.

## Setup

### 1. Configure API Base URL

Update your frontend environment configuration to point to the backend API:

**Frontend `.env` file:**

```env
VITE_API_URL=http://localhost:5000
```

Or for production:

```env
VITE_API_URL=https://api.yourdomain.com
```

### 2. Create API Client

Create a utility file for API calls (`src/lib/api.ts`):

```typescript
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

export const api = {
  async healthCheck() {
    const response = await fetch(`${API_URL}/api/health`);
    return response.json();
  },

  async getModelInfo() {
    const response = await fetch(`${API_URL}/api/model/info`);
    return response.json();
  },

  async predict(file: File) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/api/predict`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Prediction failed");
    }

    return response.json();
  },

  async batchPredict(files: File[]) {
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    const response = await fetch(`${API_URL}/api/batch-predict`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Batch prediction failed");
    }

    return response.json();
  },

  async getStats() {
    const response = await fetch(`${API_URL}/api/stats`);
    return response.json();
  },
};
```

## Usage in Components

### Image Upload Component

```tsx
import { useState, useRef } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function ImageUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setError(null);

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target?.result as string);
      reader.readAsDataURL(selected);
    }
  };

  const handlePredict = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const prediction = await api.predict(file);
      setResult(prediction);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <Card className="p-6">
        <div className="space-y-4">
          {/* File Input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
          />

          <Button
            onClick={() => fileInputRef.current?.click()}
            variant="outline"
            className="w-full"
          >
            Select Image
          </Button>

          {/* Preview */}
          {preview && (
            <div className="mt-4">
              <img
                src={preview}
                alt="Preview"
                className="w-full max-h-96 object-contain rounded-lg"
              />
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="p-4 bg-red-50 text-red-800 rounded-lg">{error}</div>
          )}

          {/* Result */}
          {result && (
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold text-lg mb-2">Prediction Result</h3>
              <div className="space-y-2">
                <div>
                  <span className="font-medium">Prediction: </span>
                  <span
                    className={
                      result.prediction === "jaundice"
                        ? "text-red-600"
                        : "text-green-600"
                    }
                  >
                    {result.prediction.toUpperCase()}
                  </span>
                </div>
                <div>
                  <span className="font-medium">Confidence: </span>
                  <span>{(result.confidence * 100).toFixed(2)}%</span>
                </div>
                <div className="mt-4 space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>
                      Jaundice: {(result.probability_jaundice * 100).toFixed(2)}
                      %
                    </span>
                    <div className="w-32 h-2 bg-gray-200 rounded">
                      <div
                        className="h-full bg-red-500 rounded"
                        style={{
                          width: `${result.probability_jaundice * 100}%`,
                        }}
                      />
                    </div>
                  </div>
                  <div className="flex justify-between">
                    <span>
                      Normal: {(result.probability_normal * 100).toFixed(2)}%
                    </span>
                    <div className="w-32 h-2 bg-gray-200 rounded">
                      <div
                        className="h-full bg-green-500 rounded"
                        style={{ width: `${result.probability_normal * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Predict Button */}
          <Button
            onClick={handlePredict}
            disabled={!file || loading}
            className="w-full"
          >
            {loading ? "Analyzing..." : "Analyze Image"}
          </Button>
        </div>
      </Card>
    </div>
  );
}
```

### Model Info Component

```tsx
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card } from "@/components/ui/card";

export function ModelInfo() {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getModelInfo()
      .then(setInfo)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Model Information</h2>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <span className="text-gray-600">Version</span>
          <p className="font-semibold">{info?.version}</p>
        </div>
        <div>
          <span className="text-gray-600">Accuracy</span>
          <p className="font-semibold">{(info?.accuracy * 100).toFixed(2)}%</p>
        </div>
        <div>
          <span className="text-gray-600">Precision</span>
          <p className="font-semibold">{(info?.precision * 100).toFixed(2)}%</p>
        </div>
        <div>
          <span className="text-gray-600">Recall</span>
          <p className="font-semibold">{(info?.recall * 100).toFixed(2)}%</p>
        </div>
      </div>
    </Card>
  );
}
```

## Environment Configuration

### Development

```env
VITE_API_URL=http://localhost:5000
```

### Production

```env
VITE_API_URL=https://api.yourdomain.com
```

## Handling CORS Issues

If you encounter CORS issues, ensure the backend has CORS properly configured:

**Backend `app.py`:**

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:8080"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

## API Integration Checklist

- [ ] Backend API is running on port 5000
- [ ] Frontend `.env` has `VITE_API_URL` configured
- [ ] API utility file created in `src/lib/api.ts`
- [ ] Image upload component created
- [ ] CORS is properly configured
- [ ] Error handling is implemented
- [ ] Loading states are handled
- [ ] Results are displayed correctly

## Troubleshooting

### 404 Errors

- Ensure backend is running: `python app.py`
- Check `VITE_API_URL` in frontend `.env`

### CORS Errors

- Update CORS configuration in backend
- Ensure frontend URL matches backend CORS allowed origins

### Model Not Loaded

- Train the model: `python train_model.py`
- Check that `models/jaundice_detection_model.h5` exists

### Predictions Not Working

- Verify image format is supported (jpg, png, etc.)
- Check server logs for errors
- Ensure image file is valid
