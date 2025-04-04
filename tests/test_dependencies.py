import tensorflow as tf
import sklearn
import prefect
import optuna
import mlflow

def test_imports():
    assert tf.__version__, "Tensorflow not installed"
    assert sklearn.__version__, "Sklearn not installed"
    assert prefect.__version__, "Prefect not installed"
    assert optuna.__version__, "Optuna not installed"
    assert mlflow.__version__, "Mlflow not installed"