import cv2
import numpy as np
import yaml
import os

import cv2
import numpy as np
import os
from src.constants import IMAGE_TO_TEXT_OUTPUTS_DIR

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Read and preprocess an image for text recognition by applying dilation and erosion.
    The function saves both the original image and the preprocessed image to a folder.

    Args:
        image_path (str): Path of the image to be read and processed.

    Returns:
        np.ndarray: Preprocessed image in BGR format.
    """
    try:
        # Read the original image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image not found or unable to load: {image_path}")

        # Convert the image to grayscale for processing
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply dilation and erosion
        dilation_kernel = np.ones((2, 2), np.uint8)
        dilated_image = cv2.dilate(gray_image, dilation_kernel, iterations=1)
        erosion_kernel = np.ones((4, 4), np.uint8)
        eroded_image = cv2.erode(dilated_image, erosion_kernel, iterations=1)
        
        # Convert the processed image back to BGR format
        preprocessed_image = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2BGR)

        # Save original and preprocessed images
        save_images(image_path, image, preprocessed_image)

        return preprocessed_image

    except Exception as e:
        raise RuntimeError(f"Error raised during image processing: {e}")

def save_images(image_path: str, original_image: np.ndarray, preprocessed_image: np.ndarray):
    """
    Saves the original and preprocessed images with appropriate names in the IMAGE_TO_TEXT_OUTPUTS_DIR.

    Args:
        image_path (str): The path of the original image.
        original_image (np.ndarray): The original image.
        preprocessed_image (np.ndarray): The preprocessed image.
    """
    # Extract the base filename from the image path
    image_name = os.path.basename(image_path)
    base_name, ext = os.path.splitext(image_name)
    
    # Prepare the output directory and file paths
    if not os.path.exists(IMAGE_TO_TEXT_OUTPUTS_DIR):
        os.makedirs(IMAGE_TO_TEXT_OUTPUTS_DIR)  # Create the directory if it doesn't exist

    real_image_path = os.path.join(IMAGE_TO_TEXT_OUTPUTS_DIR, f"{base_name}_real{ext}")
    preprocessed_image_path = os.path.join(IMAGE_TO_TEXT_OUTPUTS_DIR, f"{base_name}_preprocessed{ext}")

    # Save the images
    cv2.imwrite(real_image_path, original_image)
    cv2.imwrite(preprocessed_image_path, preprocessed_image)

    print(f"Original image saved as: {real_image_path}")
    print(f"Preprocessed image saved as: {preprocessed_image_path}")


def load_config() -> dict:
    """
    Loads the YAML configuration file and returns it as a Python dictionary.
    """
    config_path = "configs/config.yaml"
    
    # Check if the file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    try:
        with open(config_path, "r") as config_file:
            return yaml.safe_load(config_file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML configuration file: {e}")
    except Exception as e:
        raise Exception(f"Error loading configuration file: {e}")