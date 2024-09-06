from src.image_to_text import  ImageTextExtractor
from src.constants import TEST_IMAGE_PATH
from loguru import logger

logger.add("file.log", rotation="5 MB",level="DEBUG")

def main():
    image_path = TEST_IMAGE_PATH
    ocr_tool = ImageTextExtractor()
    ocr_results = ocr_tool.extract(image_path,display=True)
    
    
    logger.info("OCR Results")
    for result in ocr_results:
        logger.info(result)

if __name__ == "__main__":
    main()
