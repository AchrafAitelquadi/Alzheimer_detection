from fastapi import UploadFile
from PIL import Image
import numpy as np
from model import get_latest_model_alzheimer
import json
import os

CONFIG_PATH = "config.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

IMG_SIZE = tuple(config["IMG_SIZE"])
model = get_latest_model_alzheimer()

def preprocess_image_alzheimer(image_file: UploadFile, image_size : tuple[int, int] = IMG_SIZE):
   #Reading the image from the uploadfile
    image = Image.open(image_file.file).convert("RGB")
    #Resize the image
    image = image.resize(image_size)
    #Convert to numpy array and normalize it
    image = np.array(image) / 255.0
    #Add batch dimension 
    image_array = np.expand_dims(image, axis=0)

    return image_array

def make_predictions_alzheimer(image_file: UploadFile) -> int:
    image_array = preprocess_image_alzheimer(image_file)
    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction, axis=1)  # Find the index of the highest probability
    # Return the predicted class (index)
    return predicted_class[0]
