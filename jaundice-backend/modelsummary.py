from tensorflow.keras.models import load_model
from pathlib import Path

# Path to your trained model
MODEL_PATH = Path(r"C:\Users\bhuvan\Desktop\mini project\jaundice-backend\models\jaundice_detection_model.h5")

# Load model
model = load_model(MODEL_PATH)

# Print model summary
model.summary()
