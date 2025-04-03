import optuna
import mlflow
import json
from models_create import create_model
from data_query import load_data
from mlflow_functions import train_log_model, save_best_model
from pathlib import Path
import os

if "GITHUB_WORKSPACE" in os.environ:
    BASE_PATH = Path(os.environ["GITHUB_WORKSPACE"]) 
else:
    BASE_PATH = Path(__file__).resolve().parent.parent 

CONFIG_PATH = BASE_PATH / "scripts" / "config.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

train_dir = BASE_PATH / config["train_dir"]
test_dir = BASE_PATH / config["test_dir"]

EXPERIMENT_NAME = config["EXPERIMENT_NAME"]
IMG_SIZE = tuple(config["IMG_SIZE"])
epochs = config["epochs"]

# Initialiser MLflow
mlflow.set_experiment(EXPERIMENT_NAME)


def load_train(train_dir, test_dir, IMG_SIZE, batch_size, dropout_rate, learning_rate, epochs):
    # Charger les données
    train_data, test_data = load_data(train_dir, test_dir, IMG_SIZE, batch_size)
    num_classes = len(train_data.class_indices)  

    #Créer et entrainer le modele
    model = create_model(IMG_SIZE, dropout_rate, num_classes)
    accuracy = train_log_model("Model", model, train_data, test_data, learning_rate, batch_size, epochs)

    return accuracy

def objective(trial):
    """Optimisation des hyperparamètres avec Optuna."""
    
    # Optuna génère des hyperparamètres optimaux
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-2)
    dropout_rate = trial.suggest_float("dropout_rate", 0.5, 0.7)
    batch_size = trial.suggest_categorical("batch_size", [256, 512])

    accuracy = load_train(train_dir, test_dir, IMG_SIZE, batch_size, dropout_rate, learning_rate, epochs)

    return accuracy

def train_opti():
    # Lancer Optuna pour optimiser les hyperparamètres
    study = optuna.create_study(direction="maximize", storage="sqlite:///optuna.db")  # Maximisation de l'accuracy
    study.optimize(objective, n_trials=2)  # Nombre d'essais

    # Meilleurs hyperparamètres trouvés
    best_params = study.best_params
    print("Meilleurs hyperparamètres :", best_params)

    # Charger les données avec le **meilleur batch_size**
    train_data, test_data = load_data(train_dir, test_dir, IMG_SIZE, best_params["batch_size"])
    num_classes = len(train_data.class_indices)

    # Entraîner le modèle final avec les meilleurs hyperparamètres
    final_model = create_model(IMG_SIZE, best_params["dropout_rate"], num_classes)
    final_accuracy = train_log_model("Final_Optimized_Model", final_model, train_data, test_data, best_params["learning_rate"], best_params["batch_size"], epochs)

    # Sauvegarde du modèle final
    save_best_model(EXPERIMENT_NAME, {1: final_accuracy})

    print("Entraînement terminé avec les meilleurs hyperparamètres !")
