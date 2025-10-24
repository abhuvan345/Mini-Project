/**
 * API Client for Jaundice Detection Backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export interface PredictionResult {
  prediction: 'jaundice' | 'normal';
  confidence: number;
  probability_jaundice: number;
  probability_normal: number;
  timestamp: string;
  model_version: string;
}

export interface ModelInfo {
  model_name: string;
  version: string;
  input_shape: number[];
  classes: string[];
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1_score?: number;
  training_date?: string;
  test_samples?: number;
  timestamp: string;
}

export interface HealthCheck {
  status: string;
  timestamp: string;
  model_loaded: boolean;
}

export const api = {
  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<HealthCheck> {
    const response = await fetch(`${API_URL}/api/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  },

  /**
   * Get model information
   */
  async getModelInfo(): Promise<ModelInfo> {
    const response = await fetch(`${API_URL}/api/model/info`);
    if (!response.ok) {
      throw new Error('Failed to fetch model info');
    }
    return response.json();
  },

  /**
   * Predict jaundice from a single image
   */
  async predict(file: File): Promise<PredictionResult> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_URL}/api/predict`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Prediction failed');
    }
    
    return response.json();
  },

  /**
   * Batch predict from multiple images
   */
  async batchPredict(files: File[]): Promise<any> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    
    const response = await fetch(`${API_URL}/api/batch-predict`, {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Batch prediction failed');
    }
    
    return response.json();
  },

  /**
   * Get model statistics
   */
  async getStats(): Promise<any> {
    const response = await fetch(`${API_URL}/api/stats`);
    if (!response.ok) {
      throw new Error('Failed to fetch stats');
    }
    return response.json();
  }
};
