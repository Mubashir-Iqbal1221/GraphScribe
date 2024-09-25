import requests
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
from src.image_description_generator import ImageDescriptionGenerator
from src.utils import load_config
from loguru import logger


config = load_config()
logger.add(config["logs"]["log_file_path"], rotation=config["logs"]["rotation"], 
           retention=config["logs"]["retention"])

# Initialize the model
model = ImageDescriptionGenerator(config=config["model"])

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
    """
    Extract text description from an image URL.

    Parameters:
        - image_data: A JSON object containing an image URL.

    Returns:
        - A JSON response with the description of the image or an error message
          if the image URL is inaccessible or processing fails.
    """
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

