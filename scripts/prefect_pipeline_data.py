import logging
from prefect import flow, task, get_run_logger
import data_preparation
import data_validation
import data_split

# Configure logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


@task(retries=3, retry_delay_seconds=10, timeout_seconds=300)
def validate():
    """Task to validate images."""

    try:
        logging.info("Step 1: Validating images...")
        data_validation.validate_images()
        logging.info("Step 1 completed successfully!")
    except Exception as e:
        logging.error(f"Error in validation step : {e}")
        raise

@task(retries=3, retry_delay_seconds=10, timeout_seconds=300)
def preprocess():
    """Task to preprocess images."""

    try:
        logging.info("Step 2: Preprocessing images...")
        data_preparation.preprocess_and_save()
        logging.info("Step 2 completed successfully!")
    except Exception as e:
        logging.error(f"Error in preprocessing step : {e}")
        raise

@task(retries=3, retry_delay_seconds=10, timeout_seconds=300)
def split():
    """Task to split data into train/test sets."""

    try:
        logging.info("Step 3: Splitting data...")
        data_split.data_split()
        logging.info("Step 3 completed successfully!")
    except Exception as e:
        logging.error(f"Error in data split step: {e}")
        raise

@flow(name = "Alzheimer_data_pipeline")
def data_pipeline():
    logger = get_run_logger()
    logger.info("Starting automated data processing pipeline...")
    validate()
    preprocess()
    split()
    logger.info("Data processing pipeline completed successfully!")

if __name__ == "__main__":
    data_pipeline()