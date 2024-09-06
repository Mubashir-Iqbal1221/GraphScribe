from src.image_to_text import  ImageTextExtractor
from src.constants import TEST_IMAGE_PATH,LOG_FILE_PATH
from loguru import logger
from src.utils import load_config
config = load_config()

logger.add(LOG_FILE_PATH, rotation=config["logs"]["rotation"],level=config["logs"]["level"])

def main():
    image_path = TEST_IMAGE_PATH
    ocr_tool = ImageTextExtractor()
    ocr_results = ocr_tool.extract(image_path,save_image=True)
    
    
    logger.info("OCR Results")
    for result in ocr_results:
        logger.info(result)

if __name__ == "__main__":
    main()
