import argparse
import time
from src.constants import TEST_IMAGE_PATH, LOG_FILE_PATH
from src.ocr_service import extract_text_from_image
from src.generate_description import Descriptor
from loguru import logger
from src.utils import load_config, join_text_from_results

# Load the configuration
config = load_config()
logger.add(LOG_FILE_PATH, rotation=config["logs"]["rotation"], level=config["logs"]["level"])

def main(image_path):
    try:
        # Step 1: Extract Text from Image using OCR
        logger.info(f"Extracting text from image: {image_path}")
        # start_time = time.time()
        
        ocr_result = extract_text_from_image(image_path)
        joined_text = join_text_from_results(ocr_result)
        
        logger.info(f"OCR result: {joined_text}")
        if joined_text is None:
            logger.info("Image is not clear to interpret")
        else:
            llm = Descriptor()
            description = llm.generate_desc(joined_text)
            logger.info(f"Description: {description}")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="OCR Text Extraction and Interpretation using LLaMA Model")
    parser.add_argument("--image_path", type=str, default="/home/mubashir/onboarding_project/dataset/test5.jpg", help="Path to the input image")

    args = parser.parse_args()
    
    # Call the main function with provided arguments
    main(args.image_path)
