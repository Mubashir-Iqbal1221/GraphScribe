from src.image_to_text import ImageTextExtractor
from loguru import logger
from typing import List, Optional


def extract_text_from_image(image_path: str,config:dict)-> Optional[List]:
    """
    Extracts text from a given image using Optical Character Recognition (OCR).

    Args:
        image_path (str): The file path to the image from which to extract text.

    Returns:
        Optional[List]: A list of OCR results (if text was successfully extracted), where each 
        result contains OCR metadata. Returns `None` if no text could be extracted (e.g., the image is too blurry).
    
    Logs the OCR processing steps and results.
    """
    # Create the OCR tool instance
    ocr_tool = ImageTextExtractor(config)

    logger.info(f"Processing image: {image_path}")    
    ocr_results = ocr_tool.extract(image_path, save_image=config["save_image"])
    
    # Check if results were found
    if ocr_results is None:
        logger.info("Image is too blurry or unclear. Please provide a new image.")
        return None
    else:
        # Log the results
        logger.info("OCR Results:")
        # results = []
        for result in ocr_results:
            logger.info(result)
            # results.append(result)
        return ocr_results

