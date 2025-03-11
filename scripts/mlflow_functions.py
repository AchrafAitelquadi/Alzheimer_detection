import mlflow
import mlflow.keras
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, roc_auc_score, confusion_matrix, classification_report
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
    

def train_log_model(model_name, model, train_data, test_data, learning_rate, batch_size, epochs):
    """Train a model, log metrics, and save it in MLflow."""

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    model_name = f"Model_{model_name}_{current_time}_E{epochs}_BS{batch_size}"

    if mlflow.active_run(): 
        mlflow.end_run()

    with mlflow.start_run(run_name= model_name):
        optimizer = Adam(learning_rate=learning_rate)
        model.compile(
            optimizer = optimizer,
            loss = "sparse_categorical_crossentropy",
            metrics = ["accuracy"]
        )

        history = model.fit(train_data, epochs = epochs, 
                validation_data = test_data, 
                batch_size = batch_size,
                callbacks = [EarlyStopping(monitor = "val_loss", patience = 3, restore_best_weights = True)]
            )

        for epoch in range(len(history.history["loss"])):
            mlflow.log_metric("train_loss", history.history["loss"][epoch], step = epoch)
            mlflow.log_metric("val_loss", history.history["val_loss"][epoch], step = epoch)

            mlflow.log_metric("train_accuracy", history.history["accuracy"][epoch], step = epoch)
            mlflow.log_metric("val_accuracy", history.history["val_accuracy"][epoch], step = epoch)


        y_true = test_data.labels
        y_pred = model.predict(test_data).argmax(axis = 1)

        accuracy = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average="weighted")
        precision = precision_score(y_true, y_pred, average="weighted")
        recall = recall_score(y_true, y_pred, average="weighted")
        auc_roc = roc_auc_score(y_true, model.predict(test_data), multi_class="ovr")

        # Log everything to MLflow
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("batch_size", batch_size)  
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("date_time", current_time)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("auc", auc_roc)

        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize = (10, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=test_data.class_indices, yticklabels=test_data.class_indices)
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.title("Confusion Matrix")
        plt.savefig("confusion_matrix.png")
        plt.close()
        mlflow.log_artifact("confusion_matrix.png")
        os.remove("confusion_matrix.png")
        mlflow.keras.log_model(model, model_name)

        print(f"Logged {model_name} (Batch Size: {batch_size}): Accuracy={accuracy}, F1={f1}")
    return accuracy


def save_best_model(EXPERIMENT_NAME, model_results, save_dir=r"D:\proj\MLOPS\Alzheimer_detection\models"):
    # Determine the best model based on accuracy
    best_model_num = max(model_results, key=model_results.get)
    print(f"Best Model: {best_model_num} with Accuracy={model_results[best_model_num]}")

    # Fetch the best model from MLflow
    experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    df = mlflow.search_runs(experiment.experiment_id)

    # Get the best run based on accuracy
    best_run = df.sort_values("metrics.accuracy", ascending=False).iloc[0]
    model_name = best_run['params.model_name']
    best_model_uri = f"runs:/{best_run['run_id']}/{model_name}"

    # Load the best model
    best_model = mlflow.keras.load_model(best_model_uri)

    # Construct the save path dynamically
    save_path = os.path.join(save_dir, f"best_alzheimer_model_{model_name}.keras")
    
    # Save the model
    best_model.save(save_path, save_format="keras")

    print(f"Best model saved at: {save_path}")
    return save_path  # Return the saved model path
