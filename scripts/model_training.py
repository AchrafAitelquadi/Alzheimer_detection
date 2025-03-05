import mlflow
import mlflow.keras
from data_query import load_data
from mlflow_functions import train_log_model
from models_create import create_model

EXPERIMENT_NAME = "Alzheimer Detection"

# Load the data
train_generator, test_generator = load_data()


def train_all_models():
    """Train multiple models and log the best one."""

    mlflow.set_experiment(EXPERIMENT_NAME)

    train_data, test_data = load_data()
    model_results = {}

    for i in range(1, 4):
        model = create_model(i)
        accuracy = train_log_model(f"Model {i}", model, train_data, test_data, )
        model_results[i] = accuracy
    
    best_model_num = max(model_results, key=model_results.get)
    print(f"✅ Best Model: {best_model_num} with Accuracy={model_results[best_model_num]}")

    # Fetch the best model from MLflow
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    df = mlflow.search_runs(experiment.experiment_id)
    best_run = df.sort_values("metrics.accuracy", ascending=False).iloc[0]
    best_model_uri = f"runs:/{best_run['run_id']}/{best_run['params.model_name']}"

    # Load and save best model for deployment
    best_model = mlflow.keras.load_model(best_model_uri)
    best_model.save(r"D:\proj\MLOPS\Alzheimer_detection\models\best_alzheimer_model.h5")
    print("✅ Best model saved as best_alzheimer_model.h5")

if __name__ == "__main__":
    train_all_models()