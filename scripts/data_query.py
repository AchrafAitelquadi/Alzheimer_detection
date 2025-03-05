import os
import mlflow
import mlflow.keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Paths to the split dataset
train_dir = r"D:\proj\MLOPS\Alzheimer_detection\Data\split\train"
test_dir = r"D:\proj\MLOPS\Alzheimer_detection\Data\split\test"

# Data Generator for training and validation
def load_data(IMG_SIZE = (100, 100), BATCH_SIZE = 256):
    # Use ImageDataGenerator to read images from the directories
    train_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)

    # Load the data from the directories (ensure class mode is 'binary' or 'categorical' based on your task)
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,  # Resize images to 224x224 (can be changed)
        batch_size=BATCH_SIZE,
        class_mode='sparse'  # Change to 'categorical' if you have multiple classes
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='sparse'  # Change to 'categorical' if you have multiple classes
    )

    return train_generator, test_generator
train_generator, test_generator = load_data()
