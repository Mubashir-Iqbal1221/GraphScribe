import os
import requests
from io import BytesIO
from PIL import Image
import base64
import yaml


def upload_image_to_imgbb(api_key: str, image: Image, config : dict) -> dict:
    """
    Uploads an image to the imgbb API by converting the image into a base64-encoded string.

    Args:
        api_key (str): The API key required for authentication with the imgbb API.
        image (Image): A PIL Image object that you want to upload to imgbb.

    Returns:
        dict: A dictionary containing the response from the imgbb API, typically with details
              about the uploaded image or error messages if the upload fails.
    
    Raises:
        requests.exceptions.RequestException: If the API request fails or there's an issue with the network.
    """
    # config = load_config()
    image_upload_web_url = config["IMGBB_UPLOAD_URL"]
    image_deletion_time = config["IMAGE_EXPIRATION"]
    
    # Convert image to bytes
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    
    # Encode image to base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    payload = {
        'key': api_key,
        'image': encoded_image,
        'expiration':image_deletion_time
    }
    
    # Make the API request
    response = requests.post(image_upload_web_url, data=payload)
    response.raise_for_status()  # To raise an error for unsuccessful requests
    return response.json()


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
