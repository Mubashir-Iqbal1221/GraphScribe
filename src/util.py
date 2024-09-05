import cv2
import numpy as np
import yaml
import os

def preprocess_image(image_path:str) -> np.ndarray:
    """
    Read and preprocess an image for text recognition
    by applying dilation and erosion
    
    Args:
        image_path (str): Path of image to be read and processed
    
    Returns:
        np.ndarray : Preprocessed image in BGR form
    """
    try:
        image = cv2.imread(image_path) # Read the image
        if image is None:
            raise FileNotFoundError(f"Image not found or unable to load: {image_path}")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
        kernel = np.ones((2, 2), np.uint8) # kernel for dilation
        dilated_image = cv2.dilate(gray_image, kernel, iterations=1) #Appling dilation to remove noise form words
        kernel = np.ones((5, 5), np.uint8) # kernel for erosion
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1) # applying erosion to fill gaps in text boundaries
        preprocessed_image = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2BGR) #Convert the processed image back to a 3-channel image

        return preprocessed_image
    except Exception as e:
        raise RuntimeError(f"Error raised during Image processing {e}")


def load_config() -> dict:
    """
    Loads the YAML configuration file and returns it as a Python dictionary.
    """
    config_path = "/home/mubashir/onboarding_project/config.yaml"
    
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