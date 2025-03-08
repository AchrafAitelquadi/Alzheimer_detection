import os
import shutil
import random
import logging

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Set seed for reproducibility
random.seed(42)

def data_split(PROCESSED_DIR, OUTPUT_DIR, TRAIN_RATIO, TEST_RATIO):
    """ Splits data into training and testing sets and saves them in separate folders. """
    
    logging.info("Starting data splitting...")

    # Create output directories
    for split in ["train", "test"]:
        os.makedirs(os.path.join(OUTPUT_DIR, split), exist_ok=True)

    # Get list of class directories
    classes = [d for d in os.listdir(PROCESSED_DIR) if os.path.isdir(os.path.join(PROCESSED_DIR, d))]
    logging.info(f"Found {len(classes)} classes: {classes}")

    for class_name in classes:
        class_path = os.path.join(PROCESSED_DIR, class_name)
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
