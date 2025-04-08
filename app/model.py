import os
import tensorflow as tf 

def get_latest_model_alzheimer(model_dir : str = os.path.join(os.getcwd(), "models")):
    #Get all saved models
    print(model_dir)
    model_files = [os.path.join(model_dir, f) for f in os.listdir(model_dir) if f.endswith(".keras")]
    if not model_files:
        raise FileNotFoundError("No model files found in the directory.")
    
    latest_model = max(model_files, key = os.path.getmtime) #Getting the latest model based on time (the recent saved)
    model = tf.keras.models.load_model(latest_model)

    return model