import torch
from PIL import Image
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MoondreamChatHandler
from loguru import logger
import requests

class ImageDescriptionGenerator:
    
    def __init__(self, image_encoder_path: str, decoder_model_path: str):
        """
        Initializes the image encoder and language model (LLM).

        Args:
            image_encoder_path (str): Path to the image encoder model.
            decoder_model_path (str): Path to the LLM (language model).
        """
        # Initialize the image encoder and language model
        self.image_encoder = MoondreamChatHandler(clip_model_path=image_encoder_path)
        self.llm = Llama(
            model_path=decoder_model_path,
            chat_handler=self.image_encoder,
            n_ctx=2048  # n_ctx should be increased to accommodate the image embedding
        )

    @staticmethod
    def check_image_url_permission(image_url: str) -> dict:
        """
        Checks if the provided image URL can be accessed.

        Args:
            image_url (str): The URL of the image to check.

        Returns:
            dict: A dictionary with 'success' (True/False) and 'message' (a descriptive message).
        """
        try:
            # Send a GET request to the image URL
            response = requests.get(image_url, timeout=10)
            
            # Check the HTTP status code and return corresponding results
            if response.status_code == 200:
                return {"success": True, "message": "Image is accessible."}
            elif response.status_code == 403:
                return {"success": False, "message": "Permission denied: Access forbidden (403)."}
            elif response.status_code == 404:
                return {"success": False, "message": "Image not found (404)."}
            else:
                return {"success": False, "message": f"HTTP error {response.status_code} occurred."}
        
        except requests.exceptions.Timeout:
            return {"success": False, "message": "Request timed out."}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Error occurred: {str(e)}"}

    def generate_image_description(self, image_url: str) -> str:
        """
        Generates a textual description of the image provided via URL.

        Args:
            image_url (str): The URL of the image to describe.

        Returns:
            str: The generated description of the image.
        """
        # Check if the image URL is accessible
        permission_check = self.check_image_url_permission(image_url)
        if not permission_check['success']:
            return permission_check['message']

        # Generate image description using the language model
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are an assistant who perfectly describes images."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe this flowgraph step by step"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ]
        )
        
        return response["choices"][0]["message"]["content"]
