
import os
import pickle
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Find the project directory
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Load trained ML model
MODEL_PATH = os.path.join(
    BASE_DIR, "model", "crop_model.pkl"
)

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return jsonify({
        "message": "Crop Recommendation API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON input"}), 400

    try:
        N = float(data["N"])
        P = float(data["P"])
        K = float(data["K"])
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        ph = float(data["ph"])
        rainfall = float(data["rainfall"])

        values = [
            N, P, K, temperature,
            humidity, ph, rainfall
        ]

        if not all(np.isfinite(values)):
            raise ValueError("Values must be finite numbers")

        features = np.array([values])

        prediction = model.predict(features)

        return jsonify({
            "recommended_crop": str(prediction[0])
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Please provide all seven valid numeric values."
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

