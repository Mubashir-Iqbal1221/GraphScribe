import requests
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MoondreamChatHandler


class ImageDescriptionGenerator:
    """
    ImageDescriptionGenerator is responsible for generating textual descriptions of images 
    by utilizing an image encoder and a language model. It interacts with external models and 
    services to encode images and generate natural language descriptions.

    Attributes:
        image_encoder (MoondreamChatHandler): An instance of the image encoder used to process images.
        llm (Llama): A large language model instance that generates image descriptions based on the encoded images.
        config (dict): Configuration dictionary used to set up the models and other parameters.
    
    Methods:
        __init__(config: dict):
            Initializes the ImageDescriptionGenerator by loading the image encoder and language model based on the configuration.

        check_image_url_permission(image_url: str) -> dict:
            Verifies if the provided image URL is accessible over the network, returning a dictionary with the access status and message.

        generate_image_description(image_url: str) -> str:
            Takes an image URL, checks if the image is accessible, and generates a textual description using the language model.
    """
    
    def __init__(self, config : dict):
        """
        Initializes the components necessary for generating image descriptions.
        This includes setting up an image encoder and a language model with the specified configuration.

        Args:
            config (dict): Configuration dictionary with keys:
                - 'ENCODER_MODEL_PATH': Path to the image encoder model.
                - 'DECODER_MODEL_PATH': Path to the LLM (language model).
                - 'CONTEXT_LENGHT': Context lenght size.
        """
        # Initialize the image encoder and language model
        self.image_encoder = MoondreamChatHandler(clip_model_path=config["ENCODER_MODEL_PATH"])
        self.llm = Llama(
            model_path=config["DECODER_MODEL_PATH"],
            chat_handler=self.image_encoder,
            n_ctx=config["CONTEXT_LENGHT"],  # n_ctx should be increased to accommodate the image embedding
            
        )
        self.config=config

    @staticmethod
    def check_image_url_permission(image_url: str) -> dict:
        """
        Verifies whether the specified image URL is accessible over the network.

        Args:
            image_url (str): URL of the image to be checked.

        Returns:
            dict: A dictionary containing:
                - 'is_accessible' (bool): True if the image is accessible, False otherwise.
                - 'message' (str): Description of the accessibility status or error message.
        """
        try:
            # Send a GET request to the image URL
            response = requests.get(image_url, timeout=10)
            
            # Check the HTTP status code and return corresponding results
            if response.status_code == 200:
                return {"is_accessible": True, "message": "Image is accessible."}
            elif response.status_code == 403:
                return {"is_accessible": False, "message": "Permission denied: Access forbidden (403)."}
            elif response.status_code == 404:
                return {"is_accessible": False, "message": "Image not found (404)."}
            else:
                return {"is_accessible": False, "message": f"HTTP error {response.status_code} occurred."}
        
        except requests.exceptions.Timeout:
            return {"is_accessible": False, "message": "Request timed out."}
        except requests.exceptions.RequestException as e:
            return {"is_accessible": False, "message": f"Error occurred: {str(e)}"}
        
    def generate_image_description(self, image_url: str) -> str:
        """
        Generates a textual description for the image located at the provided URL.

        Args:
            image_url (str): URL of the image to describe.

        Returns:
            str: Textual description of the image or an error message if the image cannot be accessed.
        """
        # Check if the image URL is accessible
        permission_check = self.check_image_url_permission(image_url)
        if not permission_check['is_accessible']:
            return permission_check['message']

        # Generate image description using the language model
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are an assistant who perfectly describe images."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe what is this flowgraph about step by step :"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            temperature= self.config["TEMPERATURE"]
        )
        
        return response["choices"][0]["message"]["content"]
    
    