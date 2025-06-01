from fastapi import UploadFile
from PIL import Image
import numpy as np
from model import get_latest_model_alzheimer
import json
import os
import mlflow
from mlflow.tracking import MlflowClient
import time

CONFIG_PATH = "config.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

IMG_SIZE = tuple(config["IMG_SIZE"])
model = get_latest_model_alzheimer()

# MLflow setup
mlflow.set_tracking_uri("http://mlflow_ui:5000")  # Use container name
client = MlflowClient()

def preprocess_image_alzheimer(image_file: UploadFile, image_size: tuple[int, int] = IMG_SIZE):
    image = Image.open(image_file.file).convert("RGB")
    image = image.resize(image_size)
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def make_predictions_alzheimer(image_file: UploadFile) -> tuple[int, float]:
    image_file.file.seek(0)
    
    start_time = time.time()

    image_array = preprocess_image_alzheimer(image_file)
    
    prediction_probs = model.predict(image_array)
    predicted_class = np.argmax(prediction_probs, axis=1)[0]
    confidence = float(np.max(prediction_probs))

    latency = time.time() - start_time

    image_file.file.seek(0)
    image_data = image_file.file.read()
    temp_image_path = f"/tmp/{image_file.filename}"
    with open(temp_image_path, "wb") as f:
        f.write(image_data)

    with mlflow.start_run():
        mlflow.log_param("image_filename", image_file.filename)
        mlflow.log_param("model_version", "v1.0")
        mlflow.log_metric("prediction_confidence", confidence)
        mlflow.log_metric("prediction_latency", latency)
        mlflow.log_metric("predicted_class", predicted_class)
        mlflow.log_artifact(temp_image_path)

    os.remove(temp_image_path)

    return predicted_class, confidence