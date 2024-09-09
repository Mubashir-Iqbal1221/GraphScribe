from src.image_to_text import ImageTextExtractor
from loguru import logger
from src.utils import load_config

from src.constants import LOG_FILE_PATH

config = load_config()
logger.add(LOG_FILE_PATH, rotation=config["logs"]["rotation"],level=config["logs"]["level"])

def extract_text_from_image(image_path: str):
    # Create the OCR tool instance
    ocr_tool = ImageTextExtractor()

    logger.info(f"Processing image: {image_path}")    
    ocr_results = ocr_tool.extract(image_path, save_image=True)
    
    # Check if results were found
    if ocr_results is None:
        logger.info("Image is too blurry or unclear. Please provide a new image.")
        return None
    else:
        # Log the results
        logger.info("OCR Results:")
        results = []
        for result in ocr_results:
            logger.info(result)
            results.append(result)
        return results
