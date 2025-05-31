import json
from flask import Blueprint, request, jsonify, render_template
from PIL import Image
from dotenv import load_dotenv
import io
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory

from app.models.model_utils import load_model_and_labels, preprocess_image, F1_score
from app.models.train_model import train_model

load_dotenv()

IMG_SIZE = (int(os.getenv("IMG_HEIGHT")), int(os.getenv("IMG_WIDTH")))
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
DATA_DIR = os.getenv("DATA_DIR")
MODEL_PATH = os.getenv("MODEL_PATH")

api_blueprint = Blueprint("api", __name__)

model, class_names = load_model_and_labels()

@api_blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@api_blueprint.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return render_template("index.html", result={"class": "No file found", "confidence": 0})

    file = request.files["file"]
    try:
        img = Image.open(io.BytesIO(file.read())).convert("RGB")
        processed_img = preprocess_image(img)
        predictions = model.predict(processed_img)[0]
        top_class = class_names[int(np.argmax(predictions))]
        confidence = float(np.max(predictions))

        return render_template("index.html", result={
            "class": top_class,
            "confidence": round(confidence, 4)
        })

    except Exception as e:
        return render_template("index.html", result={"class": "Error", "confidence": 0})


@api_blueprint.route("/train", methods=["POST"])
def train():
    try:
        result = train_model()
        return render_template("index.html", train_status=result["status"])
    except Exception as e:
        return render_template("index.html", train_status=str(e))


@api_blueprint.route("/test", methods=["POST"])
def test():
    try:
        if not os.path.exists(MODEL_PATH):
            return render_template("index.html", test_status="Model not found. Train the model first.")

        val_ds = image_dataset_from_directory(
            os.path.join(DATA_DIR, "valid"),
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            label_mode="categorical"
        )

        model = load_model(MODEL_PATH, custom_objects={'F1_score': F1_score})
        results = model.evaluate(val_ds)
        loss = results[0]
        accuracy = results[1]
        f1 = results[2] if len(results) > 2 else None

        return render_template("index.html", test_result={
            "loss": round(float(loss), 4),
            "accuracy": round(float(accuracy), 4),
            "f1_score": round(float(f1), 4) if f1 is not None else None
        })

    except Exception as e:
        return render_template("index.html", test_status=f"Error: {str(e)}")

@api_blueprint.route("/training/status", methods=["GET"])
def training_status():
    try:
        with open("app/models/training_status.json") as f:
            status = json.load(f)
        return jsonify(status)
    except Exception:
        return jsonify({"status": "unknown", "error": "no status file"}), 404


@api_blueprint.route("/training/error", methods=["GET"])
def training_error():
    try:
        with open("app/models/training_status.json") as f:
            status = json.load(f)
        return jsonify({"error": status.get("error")})
    except Exception:
        return jsonify({"error": "status file not found"}), 404


@api_blueprint.route("/models", methods=["GET"])
def list_models():
    try:
        models_list = [f for f in os.listdir("data") if f.endswith(".h5")]
        return jsonify({"models": models_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
