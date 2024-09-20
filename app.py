from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
from src.image_description_generator import ImageDescriptionGenerator
from src.constants import image_encoder_path, decoder_model_path
from loguru import logger
import requests

# Initialize the model
model = ImageDescriptionGenerator(image_encoder_path=image_encoder_path,
                                  decoder_model_path=decoder_model_path)

app = FastAPI()

# Define the Pydantic model to validate the input
class ImagePathSchema(BaseModel):
    image_url: str
    
    @field_validator('image_url')
    def check_non_empty(cls, v):
        if not v.strip():
            raise ValueError('Image URL cannot be empty')
        return v


# Health Check Endpoint
@app.get("/health")
def health_status():
    return {"status": "healthy"}

# Define the API route for extracting text from the image
@app.post("/extract-text", status_code=status.HTTP_200_OK)
def extract_text(image_data: ImagePathSchema):
    try:
        
        check = ImageDescriptionGenerator.check_image_url_permission(image_data.image_url)
        logger.info(f"Check: {check}")
        if check["is_accessible"]:
            logger.info(f"Extracting text from image: {image_data.image_url}")
            
            # Generate description using the provided image URL
            description = model.generate_image_description(image_data.image_url)
            
            return {
                "Description": description,
                "status": status.HTTP_200_OK,
                "message": "Text extraction completed successfully."
            }
        else:
            logger.error(f"Image URL permission denied or inaccessible: {image_data.image_url}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Image URL is not accessible or permission denied.")
    
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        logger.error(f"Failed to connect to the image URL: {image_data.image_url}, Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to connect to the image URL. {str(e)}")
    except Exception as e:
        # Handle any other exceptions during processing
        logger.error(f"An error occurred during image processing: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred during image processing. {str(e)}")

# Allow the app to run with `python app.py` directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

    
    
"""import requests
from io import BytesIO
from base64 import b64encode
from PIL import Image

def upload_image_to_imgbb(pil_image: Image.Image, api_key: str):
    # Convert the PIL image to a BytesIO object
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    buffered.seek(0)

    # Convert the image to base64
    img_str = b64encode(buffered.getvalue()).decode('utf-8')

    # Set up the request URL and payload
    url = 'https://api.imgbb.com/1/upload'
    data = {
        'key': api_key,
        'image': img_str,
        'name': 'uploaded_image.png',
    }

    # Post the request
    response = requests.post(url, data=data)

    # Check if the upload was successful
    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        return response.json()

# Example usage:
# im = Image.open('example.png')
# print(upload_image_to_imgbb(im, 'your_imgbb_api_key'))
"""