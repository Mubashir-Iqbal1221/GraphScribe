from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel,field_validator
from src.ocr_service import extract_text_from_image
from src.utils import join_text_from_results,load_config
from src.generate_description import Descriptor
from src.constants import LOG_FILE_PATH
from loguru import logger

config = load_config()
logger.add(LOG_FILE_PATH, rotation=config["logs"]["rotation"], level=config["logs"]["level"])


app = FastAPI()

# Define the Pydantic model to validate the input
class ImagePathSchema(BaseModel):
    image_path: str
    
    @field_validator('image_path')
    def check_non_empty(cls, v):
        if not v.strip():
            raise ValueError('Image path cannot be empty')
        return v

# Define the API route
@app.post("/extract-text/", status_code=status.HTTP_200_OK)
def extract_text(image_data: ImagePathSchema):
    logger.info(f"Extracting text from image: {image_data.image_path}")
    # Call the OCR function with the provided image path
    ocr_result = extract_text_from_image(image_data.image_path,config=config)
    joined_text = join_text_from_results(ocr_result)
    
    logger.info(f"Joined Extracted Text: {joined_text}")
    if not joined_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image is too blurry or unclear. Please provide a valid image."
        )
    
    llm = Descriptor(config=config)
    description = llm.generate(joined_text)
    logger.info(f"Description: {description}")
    # Return the extracted text with status code 200
    return {
        "Description": description,
        "status": status.HTTP_200_OK,
        "message": "Text extraction completed successfully."
    }
    
    #uvicorn app:app --host 0.0.0.0 --port 8000 --reload