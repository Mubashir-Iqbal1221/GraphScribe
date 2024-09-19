import torch
from PIL import Image
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MiniCPMv26ChatHandler
from loguru import logger
import requests

# logger.

class ImageDescriptionGenerator():
    def __init__(self,image_encoder_path:str,decoder_model_path:str):
       # Initialize the image encoder and language model (LLM)
        self.image_encoder = MiniCPMv26ChatHandler(clip_model_path=image_encoder_path)
        self.llm = Llama(
                    model_path=decoder_model_path,
                    chat_handler=self.image_encoder,
                    n_ctx=2048, # n_ctx should be increased to accommodate the image embedding
                )
    @staticmethod    
    def check_image_url_permission(image_url:str)-> dict:
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
                # Image is accessible
                return {"success": True, "message": "Image is accessible."}
            elif response.status_code == 403:
                # Permission denied (Forbidden)
                return {"success": False, "message": "Permission denied: Access forbidden (403)."}
            elif response.status_code == 404:
                # Image not found
                return {"success": False, "message": "Image not found (404)."}
            else:
                # Any other status code
                return {"success": False, "message": f"HTTP error {response.status_code} occurred."}

        except requests.exceptions.Timeout:
            # Handle timeout exception
            return {"success": False, "message": "Request timed out."}
        except requests.exceptions.RequestException as e:
            # Handle other request exceptions (e.g., connection error, invalid URL)
            return {"success": False, "message": f"Error occurred: {str(e)}"}
    
    
    def generate_image_description(image_url:str)->str:
        """
            Generates a textual description of the image provided via URL.

            Args:
                image_url (str): The URL of the image to describe.

            Returns:
                str: The generated description of the image.
        """
        
        response = llm.create_chat_completion(
                        messages = [
                            {"role": "system", "content": "You are an assistant who perfectly describes images."},
                            {
                                "role": "user",
                                "content": [
                                    {"type" : "text", "text": "Describe this flowgraph step by step"},
                                    {"type": "image_url", "image_url":{"url":image_url}}
                                ]
                            }
                        ]
                    )
        return response["choices"][0]['message']['content']
    
                            
    