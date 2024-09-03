from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import cv2
import numpy as np
# ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
# print("imported")

class image_to_text():
    def __init__(self):
        # print("iniitiated")
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
    
    def preprocess_image(self,image_path):
        self.image_path = image_path

        image = cv2.imread(image_path) # Read the image
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
        kernel = np.ones((2, 2), np.uint8) # kernel for dilation
        dilated_image = cv2.dilate(gray_image, kernel, iterations=1) #Appling dilation to remove noise form words
        kernel = np.ones((5, 5), np.uint8) # kernel for erosion
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1) # applying erosion to fill gaps in text boundaries
        preprocessed_image = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2BGR) #Convert the processed image back to a 3-channel image

        return preprocessed_image
    
    
    def paddle_ocr(self,preprocessed_image):
        image = preprocessed_image.copy()
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        # Perform OCR
        result = self.ocr.ocr(image_rgb, cls=True)

        return result[0]
    
    def display_anotated_image(self,results,image_path=None, ):
    # Open the image
        if image_path is None:
            image = Image.open(self.image_path)
        else:
            image = Image.open(image_path)

        # Create a figure and axis to plot on
        fig, ax = plt.subplots(1,figsize=(10,10))
        ax.imshow(image)
        print(len(results))

        for result in results:
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
            rect = patches.Rectangle((x1, y1), width, height, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

            # Annotate the word with its confidence, placing it slightly above the top-left corner of the box
            annotation = f"{word} ({score:.2f})"
            ax.text(x1, y1 - 10, annotation, color='blue', fontsize=6)

        # Hide axes
        plt.axis('off')
        plt.show()

    
test = image_to_text()
image_path = "/home/mubashir/onboarding_project/test_images/test2.jpg"
pre_processed_image = test.preprocess_image(image_path)
result = test.paddle_ocr(pre_processed_image)
test.display_anotated_image(result)
# plt.imshow(pre_processed_image)
# plt.show()
