import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import numpy as np
import os
from PIL import Image
from paddleocr import PaddleOCR
from src.utils import preprocess_image
from src.constants import IMAGE_TO_TEXT_OUTPUTS_DIR
from loguru import logger


class ImageTextExtractor:
    """
    Load PaddleOcr model and provide funtion "paddle_ocr" to extract text from image
    """
    def __init__(self,config:dict):
        """Recieve config["ocr"]
        """
        try:
            self.config = config
            self.ocr_tool = PaddleOCR(use_angle_cls = self.config["use_angle_cls"], 
                                 lang=self.config["lang"])

        except Exception as e:
            raise RuntimeError(f"Failed to initialize PaddleOCR: {e}")
            
    def paddle_ocr(self, preprocessed_image:np.ndarray)-> list:
        """
        Extract text from a preprocessed image using PaddleOCR.
        
        This function takes a preprocessed image as input and uses the PaddleOCR model 
        to perform optical character recognition (OCR). It returns a list of results, 
        each containing a bounding box and a tuple of predicted text and confidence score.

        Args:
            preprocessed_image (np.ndarray): The preprocessed image (usually in RGB or grayscale format)
                                            from which text will be extracted.

        Returns:
            list: A list of OCR results, where each result is structured as:
                [
                    [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],  # Bounding box coordinates
                    (predicted_text, confidence_score)         # Text and confidence score tuple
                ]
                - Bounding box: A list of four [x, y] coordinates representing the detected text region.
                - predicted_text (str): The text recognized by PaddleOCR.
                - confidence_score (float): The confidence score of the OCR prediction.
        """
        
        try:
            image = preprocessed_image.copy()
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            # Perform OCR
            result = self.ocr_tool.ocr(image_rgb, cls=True)
            if result[0] is None:
                logger.info("Image is too blurry")
                return result[0]
            # else:
            #     print(result)

            return result[0]
        except Exception as e:
            raise RuntimeError(f"Error during OCR processing: {e}")

    def save_annotated_image(self, ocr_results: list, image_path: str, save_directory: str = IMAGE_TO_TEXT_OUTPUTS_DIR) -> None:
        """
        Saves an image with bounding boxes and annotations for OCR results to a specified directory.

        Args:
            ocr_results (list): A list of OCR results, where each result is structured as:
                                [
                                    [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],  # Bounding box coordinates
                                    (predicted_text:str, confidence_score:float)         # Text and confidence score tuple
                                ]
            image_path (str): The file path to the image on which OCR was performed.
            save_directory (str): The directory where the annotated image will be saved. The directory will be created if it does not exist.

        Returns:
            None: This function saves the annotated image in the given directory.
        """
        try:
            # Load the image
            image = Image.open(image_path)

            # Create a figure and axis to plot on
            fig, ax = plt.subplots(1, figsize=(self.config["display"]["figure_width"],
                                            self.config["display"]["figure_height"]))
            ax.imshow(image)
            

            for result in ocr_results:
                p1 = result[0][0]
                p2 = result[0][1]
                p3 = result[0][2]
                _ = result[0][3]
                word = result[1][0]
                score = result[1][1]

                width = p2[0] - p1[0]
                height = p3[1] - p1[1]
                x1 = p1[0]
                y1 = p1[1]

                # Create a rectangle patch and add it to the plot
                rect = patches.Rectangle((x1, y1), width, height, linewidth=self.config["display"]["linewidth"],
                                        edgecolor=self.config["display"]["edgecolor"], facecolor=self.config["display"]["facecolor"])
                ax.add_patch(rect)

            # Hide axes
            plt.axis('off')

            # Ensure the directory exists
            os.makedirs(save_directory, exist_ok=True)

            # Save the annotated image to the specified directory
            save_path = os.path.join(save_directory, os.path.basename(image_path))
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)

            # Close the plot to avoid memory issues
            plt.close()

        except Exception as e:
            raise RuntimeError(f"Error while saving annotated image: {e}")
            
    def extract(self, image_path:str, save_image:bool)-> None:
        """ Displays image with extracted text from image

        Args:
            image_path (str): Path of the image from which text needs to be extracted.
            display (bool)  : Boolean to display image or not
        Returns:
            ocr_results (list): A list of OCR results, where each result is structured as:
                            [
                                [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],       # Bounding box coordinates
                                (predicted_text:str, confidence_score:float)    # Text and confidence score tuple
                            ]

        """
        preprocessed_image = preprocess_image(image_path)
        ocr_results = self.paddle_ocr(preprocessed_image)
        if ocr_results is None:
            return None
        if save_image:
            self.save_annotated_image(ocr_results=ocr_results, image_path=image_path)
        return ocr_results




