import mlflow
from data_query import load_data
from mlflow_functions import train_log_model, save_best_model
from models_create import create_model
import json

with open(r"D:\proj\MLOPS\Alzheimer_detection\scripts\config.json", "r") as f:
    config = json.load(f)

train_dir = config["train_dir"]
test_dir = config["test_dir"]
EXPERIMENT_NAME = config["EXPERIMENT_NAME"]
IMG_SIZE = tuple(config["IMG_SIZE"])
learning_rate = config["learning_rate"]
batch_size = config["batch_size"]
epochs = config["epochs"]
dropout_rate = config["dropout_rate"]
number_of_models = config["number_of_models"]

def train_all_models():
    """Train multiple models and log the best one."""

    mlflow.set_experiment(EXPERIMENT_NAME)

    train_data, test_data = load_data(train_dir, test_dir, IMG_SIZE, batch_size)
    num_classes = len(train_data.class_indices)

    model_results = {}

    for i in range(1, number_of_models + 1):
        model = create_model(i, IMG_SIZE, dropout_rate, num_classes)
        accuracy = train_log_model(f"Model{i}", model, train_data, test_data, learning_rate, batch_size, epochs)
        model_results[i] = accuracy
    
    save_best_model(EXPERIMENT_NAME, model_results)
    
if __name__ == "__main__":
    train_all_models()