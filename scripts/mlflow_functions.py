import mlflow
import mlflow.keras
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from tensorflow.keras.callbacks import EarlyStopping


def train_log_model(model_name, model, train_data, test_data, batch_size = 256):
    """Train a model, log metrics, and save it in MLflow."""

    if mlflow.active_run():
        mlflow.end_run()

    with mlflow.start_run(run_name= model_name):

        model.compile(
            optimizer = "adam",
            loss = "sparse_categorical_crossentropy",
            metrics = ["accuracy"]
        )

        model.fit(train_data, epochs = 1, 
                validation_data = test_data, 
                batch_size = batch_size,
                callbacks = [EarlyStopping(monitor = "val_loss", patience = 3, restore_best_weights = True)]
            )

        y_true = test_data.labels
        y_pred = model.predict(test_data).argmax(axis = 1)

        accuracy = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average="weighted")
        precision = precision_score(y_true, y_pred, average="weighted")
        recall = recall_score(y_true, y_pred, average="weighted")

        # Log everything to MLflow
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("batch_size", batch_size)  # Log batch size

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)

        mlflow.keras.log_model(model, model_name)

        print(f"Logged {model_name} (Batch Size: {batch_size}): Accuracy={accuracy}, F1={f1}")
    return accuracy