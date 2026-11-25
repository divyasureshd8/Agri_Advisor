
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load trained crop recommendation model
with open("model/crop_model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return jsonify({
        "message": "Crop Recommendation API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    try:
        N = float(data["N"])
        P = float(data["P"])
        K = float(data["K"])
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        ph = float(data["ph"])
        rainfall = float(data["rainfall"])

        features = np.array([[
            N, P, K, temperature,
            humidity, ph, rainfall
        ]])

        prediction = model.predict(features)

        return jsonify({
            "recommended_crop": str(prediction[0])
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Please provide all seven valid input values."
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
  
