from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import cv2
import numpy as np
from src.utils import load_config 
from src.utils import preprocess_image


class ImageTextExtractor:
    """
    Load PaddleOcr model and provide funtion "paddle_ocr" to extract text from image
    """
    def __init__(self):
        try:
            self.config = load_config()
            self.ocr_tool = PaddleOCR(use_angle_cls = self.config["ocr"]["use_angle_cls"], 
                                 lang=self.config["ocr"]["lang"])

        except Exception as e:
            raise RuntimeError(f"Failed to initialize PaddleOCR: {e}")
            
    def paddle_ocr(self,preprocessed_image:np.ndarray)-> list:
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

            return result[0]
        except Exception as e:
            raise RuntimeError(f"Error during OCR processing: {e}")
    
    def display_annotated_image(self,ocr_results:list,image_path:str)-> None:
        """
        Displays an image with bounding boxes and annotations for OCR results.
        
        Args:
            ocr_results (list): A list of OCR results, where each result is structured as:
                            [
                                [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],  # Bounding box coordinates
                                (predicted_text:str, confidence_score:float)         # Text and confidence score tuple
                            ]
            image_path (str): The file path to the image on which OCR was performed.

        Returns:
            None: This function displays the annotated image and does not return any value.

        """
        try:
            image = Image.open(image_path)

            # Create a figure and axis to plot on
            fig, ax = plt.subplots(1,figsize=(self.config["display"]["figure_width"],
                                            self.config["display"]["figure_height"]))
            ax.imshow(image)

            for result in ocr_results:
                p1 = result[0][0]
                p2 = result[0][1]
                p3 = result[0][2]
                p4 = result[0][3]
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

                # Annotate the word with its confidence, placing it slightly above the top-left corner of the box
                annotation = f"{word} ({score:.2f})"
                ax.text(x1, y1 - self.config["display"]["annotation_offset"], annotation, 
                        color=self.config["display"]["annotation_color"], fontsize=self.config["display"]["annotation_fontsize"])

            # Hide axes
            plt.axis('off')
            plt.show()
        except Exception as e:
            raise RuntimeError(f"Error while displaying annotated image : {e}")
        
    def extract(self,image_path:str,display:bool)-> None:
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
        if display:
            self.display_annotated_image(ocr_results,image_path)
        return ocr_results




