import os
import base64
import numpy as np
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS

# TensorFlow/Keras
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "deepfake_model.h5")
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = load_model(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    except Exception as e:
        print(f"Failed to load model: {e}")
else:
    print("Model file not found. Please run train_model.py to create deepfake_model.h5.")


def preprocess_image_bytes(image_bytes: bytes) -> np.ndarray:
    """Convert raw image bytes to a model-ready tensor (1, 224, 224, 3)."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode image bytes")
    # Convert BGR (OpenCV) -> RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)  # (1, 224, 224, 3)
    return img


def decode_base64_image(data: str) -> bytes:
    """Decode a base64 string; supports data URLs like 'data:image/...;base64,XXX'."""
    if data.startswith("data:image"):
        # Strip the data URL header
        header, b64data = data.split(",", 1)
        return base64.b64decode(b64data)
    return base64.b64decode(data)


@app.route("/", methods=["GET"]) 
def index():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"]) 
def predict():
    if model is None:
        return jsonify({
            "error": "Model not loaded. Please train the model first by running train_model.py.",
            "detail": "Expected backend/deepfake_model.h5"
        }), 503

    try:
        image_bytes = None

        # 1) multipart/form-data
        if "file" in request.files:
            file_storage = request.files["file"]
            image_bytes = file_storage.read()
        else:
            # 2) JSON with base64.
            data = request.get_json(silent=True) or {}
            image_b64 = data.get("image_base64")
            if not image_b64:
                return jsonify({"error": "No image provided. Use form-data 'file' or JSON 'image_base64'."}), 400
            image_bytes = decode_base64_image(image_b64)

        # Preprocess
        input_tensor = preprocess_image_bytes(image_bytes)
        # Predict
        prob_fake = float(model.predict(input_tensor)[0][0])
        THRESHOLD = float(os.environ.get("FAKE_THRESHOLD", "0.5"))
        label = "fake" if prob_fake >= THRESHOLD else "real"

        return jsonify({
            "label": label,
            "prob_fake": prob_fake
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)