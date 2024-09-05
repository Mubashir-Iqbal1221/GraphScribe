from src.util import preprocess_image
from src.image_to_text import  paddle_ocr_wrapper,display_annotated_image
from src.constant import TEST_IMAGE_PATH,IMAGE_TO_ANNOTATE

def main():
    image_path = TEST_IMAGE_PATH
    preprocessed_image = preprocess_image(image_path)
    ocr_tool = paddle_ocr_wrapper()
    ocr_results = ocr_tool.paddle_ocr(preprocessed_image)
    display_annotated_image(ocr_results,IMAGE_TO_ANNOTATE)

if __name__ == "__main__":
    main()