from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import cv2
import numpy as np
from src.util import load_config 


class paddle_ocr_wrapper:
    """
    Load PaddleOcr model and provide funtion "paddle_ocr" to extract text from image
    """
    def __init__(self):
        self.config = load_config()
        self.ocr = PaddleOCR(use_angle_cls = self.config["ocr"]["use_angle_cls"], lang=self.config["ocr"]["lang"])
    
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
        image = preprocessed_image.copy()
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        # Perform OCR
        result = self.ocr.ocr(image_rgb, cls=True)

        return result[0]
    
def display_annotated_image(ocr_results:list,image_path:str)-> None:
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
    image = Image.open(image_path)
    config = load_config()

    # Create a figure and axis to plot on
    fig, ax = plt.subplots(1,figsize=config["display"]["figure_size"])
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
        rect = patches.Rectangle((x1, y1), width, height, linewidth=config["display"]["linewidth"],
                                 edgecolor=config["display"]["edgecolor"], facecolor=config["display"]["facecolor"])
        ax.add_patch(rect)

        # Annotate the word with its confidence, placing it slightly above the top-left corner of the box
        annotation = f"{word} ({score:.2f})"
        ax.text(x1, y1 - config["display"]["annotation_offset"], annotation, 
                color=config["display"]["annotation_color"], fontsize=config["display"]["annotation_fontsize"])

    # Hide axes
    plt.axis('off')
    plt.show()




