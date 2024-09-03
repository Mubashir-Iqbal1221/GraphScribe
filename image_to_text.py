from paddleocr import PaddleOCR,draw_ocr
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import cv2
import numpy as np
# ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
print("imported")

class image_to_text():
    def __init__(self):
        print("iniitiated")
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
    
    def preprocess_image(self,image_path):

        image = cv2.imread(image_path) # Read the image
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert to grayscale
        kernel = np.ones((2, 2), np.uint8) # kernel for dilation
        dilated_image = cv2.dilate(gray_image, kernel, iterations=1) #Appling dilation to remove noise form words
        kernel = np.ones((5, 5), np.uint8) # kernel for erosion
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1) # applying erosion to fill gaps in text boundaries
        preprocessed_image = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2BGR) #Convert the processed image back to a 3-channel image
        
        return preprocessed_image
    
    
test = image_to_text()
image_path = "/home/mubashir/onboarding_project/test_images/test2.jpg"
pre_processed_image = test.preprocess_image(image_path)
plt.imshow(pre_processed_image)
plt.show()
