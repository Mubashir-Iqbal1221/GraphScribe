import requests
from io import BytesIO
from PIL import Image
import base64


def upload_image_to_imgbb(api_key: str, image: Image) -> dict:
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
    
    # Convert image to bytes
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    
    # Encode image to base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    url = 'https://api.imgbb.com/1/upload'
    payload = {
        'key': api_key,
        'image': encoded_image
    }
    
    # Make the API request
    response = requests.post(url, data=payload)
    response.raise_for_status()  # To raise an error for unsuccessful requests
    return response.json()



# # # Example usage:
# image = Image.open('/home/mubashir/onboarding_project/dataset/test.png')
# print(upload_image_to_imgbb(api_key,image)["data"]["url"])

