import cv2
import numpy as np
import yaml

def preprocess_image(image_path:str) -> np.ndarray:
    """
    Read and preprocess an image for text recognition
    by applying dilation and erosion
    
    Args:
        image_path (str): Path of image to be read and processed
    
    Returns:
        np.ndarray : Preprocessed image in BGR form
    """
    image = cv2.imread(image_path) # Read the image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    kernel = np.ones((2, 2), np.uint8) # kernel for dilation
    dilated_image = cv2.dilate(gray_image, kernel, iterations=1) #Appling dilation to remove noise form words
    kernel = np.ones((5, 5), np.uint8) # kernel for erosion
    eroded_image = cv2.erode(dilated_image, kernel, iterations=1) # applying erosion to fill gaps in text boundaries
    preprocessed_image = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2BGR) #Convert the processed image back to a 3-channel image

    return preprocessed_image


def load_config() -> dict:
    """
    Loads the YAML configuration file and returns it as a Python dictionary.
    """
    with open("/home/mubashir/onboarding_project/config.yaml", "r") as config_file:
        return yaml.safe_load(config_file)