import os
import cv2
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

RAW_DIR = r"D:\proj\MLOPS\Alzheimer_detection\Data\raw"
PROCESSED_DIR = r"D:\proj\MLOPS\Alzheimer_detection\Data\processed"
IMG_SIZE = (100, 100)

def preprocess_and_save():
    logging.info("Starting preprocessing...")

    os.makedirs(PROCESSED_DIR, exist_ok=True)  # Creation of the new directory to save the processed images
    logging.info(f"Processed images will be saved to: {PROCESSED_DIR}")

    total_images_processed = 0  # Counter for total images processed

    for class_name in os.listdir(RAW_DIR):
        class_path = os.path.join(RAW_DIR, class_name)
        save_path = os.path.join(PROCESSED_DIR, class_name)
        os.makedirs(save_path, exist_ok=True)

        logging.info(f"Processing class: {class_name}")
        
        images_processed = 0  # Counter for images in the current class
        
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path)

            if img is None:
                logging.warning(f"Skipping corrupted image: {img_name}")
                continue
            
            # Preprocessing steps
            img = cv2.resize(img, IMG_SIZE)

            save_img_path = os.path.join(save_path, img_name)
            # Save image
            cv2.imwrite(save_img_path, img)
            images_processed += 1  # Increment image counter for the class
            total_images_processed += 1  # Increment total image counter

        logging.info(f"Processed {images_processed} images for class: {class_name}")
    
    logging.info(f"Total images processed: {total_images_processed}")
    logging.info("Preprocessing completed!")

if __name__ == "__main__":
    preprocess_and_save()
