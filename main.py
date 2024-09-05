from src.util import preprocess_image
from src.image_to_text import  paddle_ocr_wrapper,display_anotated_image


image_path = "/home/mubashir/onboarding_project/dataset/test.jpg"
preprocessed_image = preprocess_image(image_path)
ocr_tool = paddle_ocr_wrapper()
ocr_results = ocr_tool.paddle_ocr(preprocessed_image)
display_anotated_image(ocr_results,image_path)