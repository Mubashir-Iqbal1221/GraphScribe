from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image


class Description:
    """
    This module provides functionality to load and use the original Moondream model without quantization.
    It supports loading the model and tokenizer from a local directory and generating detailed descriptions
    of flowgraphs based on input images.

    Classes:
        - Description: A class that handles loading the original Moondream model and generating textual descriptions
                       of flowgraphs based on input images.

    Usage:
        The Description class in this module is intended to work with the original Moondream model.
        It does not support quantized models or optimizations like GGUF. The model and tokenizer must be
        loaded from the local directory, and a PIL image is required to generate a description.
    """

    def __init__(self, model_path: str) -> None:
        """This class is for original moondream model without any quantization"""

        # Load the model and tokenizer from the local directory
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def generate(self, image: Image.Image) -> str:
        """
        Generates a description of the flowgraph based on an input image.

        This method encodes the input image using the model's encoder, then uses the encoded image
        to answer a prompt that describes the flowgraph step by step.

        Args:
            image (Image.Image): The input image to be encoded, expected to be a PIL Image object.

        Returns:
            str: A string description of the flowgraph, describing each step in detail.
        """

        # prompt = "Describe the flowgraph step by step. Each step should be described."
        prompt = """Describe the flowgraph in a detailed, step-by-step manner.
                    For each step, explain what action is being taken, the input required, 
                    the output generated, and how this step connects to the next. Ensure that each 
                    explanation provides clarity on the purpose of the step and its role in the overall flow."""
        enc_image = self.model.encode_image(image)
        description = self.model.answer_question(enc_image, prompt, self.tokenizer)
        return description
