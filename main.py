import argparse
from src.image_to_text import  ImageTextExtractor
from src.constants import TEST_IMAGE_PATH,LOG_FILE_PATH
from loguru import logger
from src.utils import load_config

# print(f"path : {LOG_FILE_PATH}")
config = load_config()
logger.add(LOG_FILE_PATH, rotation=config["logs"]["rotation"],level=config["logs"]["level"])

def main():
    parser = argparse.ArgumentParser(description="Process an image and extract text using OCR.")
    parser.add_argument("image_path", type=str, nargs="?", default=TEST_IMAGE_PATH, help="Path to the image to process")
    args = parser.parse_args()
    # image_path = TEST_IMAGE_PATH
    ocr_tool = ImageTextExtractor()
    image_path = args.image_path
    logger.info(f"Processing image: {image_path}")    
    ocr_results = ocr_tool.extract(image_path,save_image=True)
    if ocr_results is None:
        logger.info("Image is too blurry or unclear. Please provide a new image.")
    else:
        # If OCR results are valid, log them
        logger.info("OCR Results:")
        for result in ocr_results:
            logger.info(result)
        

    
if __name__ == "__main__":
    main()
