import os
import cv2
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def validate_images(RAW_DIR):
    """
    Validates the images in the processed directory, checks for corrupted images,
    and removes them if found.
    """
    corrupted_images = []
    total_images = 0

    # Iterate over each class (subdirectory)
    for class_name in os.listdir(RAW_DIR):
        class_path = os.path.join(RAW_DIR, class_name)

        if not os.listdir(class_path):
            continue

        logging.info(f"Checking images in class: {class_name}")
        
        # Iterate over each image in the class
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            total_images += 1
            
            try:
                img = cv2.imread(img_path)

                # Check if the image is corrupted (None is returned if image cannot be read)
                if img is None:
                    corrupted_images.append(img_path)
            
            except Exception as e:
                logging.error(f"Error reading image {img_path}: {e}")
                continue

    # Handle corrupted images
    if corrupted_images:
        logging.warning(f"Found {len(corrupted_images)} corrupted images!")
        for img in corrupted_images:
            logging.info(f"Corrupted image: {img}")
            try:
                os.remove(img)
                logging.info(f"Removed corrupted image: {img}")
            except Exception as e:
                logging.error(f"Failed to remove image {img}: {e}")
    else:
        
        logging.info("All images are valid!")

    logging.info(f"Total images checked: {total_images}")


