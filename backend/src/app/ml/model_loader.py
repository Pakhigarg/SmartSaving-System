import os
import joblib

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "smart_saving_classifier.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")

# Load ML Model
model = joblib.load(MODEL_PATH)

# Load Label Encoder
label_encoder = joblib.load(ENCODER_PATH)