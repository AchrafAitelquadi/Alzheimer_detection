import logging
from prefect import flow, task, get_run_logger
import train_optimize
import data_preparation
import data_validation
import data_split
import json

with open(r"D:\proj\MLOPS\Alzheimer_detection\scripts\config.json", "r") as f:
    config = json.load(f)

# Configure logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

RAW_DIR = config["RAW_DIR"]
PROCESSED_DIR = config["PROCESSED_DIR"]
IMG_SIZE = tuple(config["IMG_SIZE"])
TRAIN_RATIO = config["TRAIN_RATIO"]
TEST_RATIO = config["TEST_RATIO"]
OUTPUT_DIR = config["OUTPUT_DIR"]

args = {"retries" : 3, 
        "retry_delay_seconds" : 10, 
        "timeout_seconds" : 300}



@task(retries=3, retry_delay_seconds=10, timeout_seconds=300)
def validate():
    """Task to validate images."""

    try:
        logging.info("Step 1: Validating images...")
        data_validation.validate_images(RAW_DIR)
        logging.info("Step 1 completed successfully!")
    except Exception as e:
        logging.error(f"Error in validation step : {e}")
        raise

@task(retries=3, retry_delay_seconds=10, timeout_seconds=300)
def preprocess():
    """Task to preprocess images."""

    try:
        logging.info("Step 2: Preprocessing images...")
        data_preparation.preprocess_and_save(RAW_DIR, PROCESSED_DIR, IMG_SIZE)
        logging.info("Step 2 completed successfully!")
    except Exception as e:
        logging.error(f"Error in preprocessing step : {e}")
        raise

@task(retries=3, retry_delay_seconds=10, timeout_seconds=300)
def split():
    """Task to split data into train/test sets."""

    try:
        logging.info("Step 3: Splitting data...")
        data_split.data_split(PROCESSED_DIR, OUTPUT_DIR, TRAIN_RATIO, TEST_RATIO)
        logging.info("Step 3 completed successfully!")
    except Exception as e:
        logging.error(f"Error in data split step: {e}")
        raise

@task(retries = 3, retry_delay_seconds = 10, timeout_seconds = 300)
def train():
    try:
        logging.info("Step 3: Splitting data...")
        train_optimize.train_opti()
        logging.info("Step 3 completed successfully!")
    except Exception as e:
        logging.error(f"Error in data split step: {e}")
        raise


@flow(name = "Alzheimer_data_pipeline")
def data_train_pipeline():
    logger = get_run_logger()
    logger.info("Starting automated data processing pipeline...")
    validate()
    preprocess()
    split()
    train()
    logger.info("Data processing pipeline completed successfully!")

if __name__ == "__main__":
    data_train_pipeline()