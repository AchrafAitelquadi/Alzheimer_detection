import os
import shutil
import random
import logging
import json
# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

with open(r"D:\proj\MLOPS\Alzheimer_detection\scripts\config.json", "r") as f:
    config = json.load(f)

# Set seed for reproducibility
random.seed(42)

# Define directories
DATA_DIR = config["PROCESSED_DIR"]
OUTPUT_DIR = config["OUTPUT_DIR"]

# Train-test split ratios
TRAIN_RATIO = config["TRAIN_RATIO"]
TEST_RATIO = config["TEST_RATIO"]

def data_split():
    """ Splits data into training and testing sets and saves them in separate folders. """
    
    logging.info("Starting data splitting...")

    # Create output directories
    for split in ["train", "test"]:
        os.makedirs(os.path.join(OUTPUT_DIR, split), exist_ok=True)

    # Get list of class directories
    classes = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    logging.info(f"Found {len(classes)} classes: {classes}")

    for class_name in classes:
        class_path = os.path.join(DATA_DIR, class_name)
        images = os.listdir(class_path)

        if not images:
            logging.warning(f"No images found in class: {class_name}. Skipping...")
            continue

        random.shuffle(images)

        # Calculate split indices
        train_idx = int(len(images) * TRAIN_RATIO)
        train_images = images[:train_idx]
        test_images = images[train_idx:]

        logging.info(f"Class '{class_name}': {len(train_images)} train images, {len(test_images)} test images.")

        # Create class-specific directories in train/test folders
        for split in ["train", "test"]:
            os.makedirs(os.path.join(OUTPUT_DIR, split, class_name), exist_ok=True)

        # Function to copy images with error handling
        def move_images(img_list, split_name):
            success_count = 0
            for img in img_list:
                src = os.path.join(class_path, img)
                dst = os.path.join(OUTPUT_DIR, split_name, class_name, img)
                try:
                    shutil.copy(src, dst)
                    success_count += 1
                except Exception as e:
                    logging.error(f"Error copying {src} to {dst}: {e}")
            logging.info(f"Moved {success_count}/{len(img_list)} images to '{split_name}/{class_name}'")

        # Move images to respective folders
        move_images(train_images, "train")
        move_images(test_images, "test")

    logging.info("Data split completed successfully!")
