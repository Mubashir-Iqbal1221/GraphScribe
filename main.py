from src.image_to_text import  ImageTextExtractor
from src.constant import TEST_IMAGE_PATH
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    image_path = TEST_IMAGE_PATH
    ocr_tool = ImageTextExtractor()
    ocr_results = ocr_tool.extract(image_path,display=True)
    
    for result in ocr_results:
        logger.info(result)

if __name__ == "__main__":
    main()