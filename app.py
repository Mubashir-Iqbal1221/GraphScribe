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
def extract_text(image_data: ImagePathSchema,fast_generate:bool):
    """
    Extracts text from the image provided through the image path, processes it, 
    and returns a generated description of the extracted text.

    Args:
        image_data (ImagePathSchema): A Pydantic schema containing the path to the image for text extraction.

    Returns:
        dict: A dictionary containing the generated description, status code, and a success message.

    Raises:
        HTTPException: If the text extraction fails due to the image being too blurry or unclear,
                       this exception is raised with a 400 Bad Request status code and an appropriate error message.
    
    Workflow:
        1. Logs the start of the text extraction process.
        2. Calls the OCR function to extract text from the image located at `image_data.image_path`.
        3. Joins the extracted text results.
        4. If no text is extracted (e.g., due to image clarity), raises an HTTPException with a 400 status.
        5. Generates a description of the extracted text using a descriptor.
        6. Logs the generated description.
        7. Returns the description, status code 200, and success message.
    """

    logger.info(f"Extracting text from image: {image_data.image_path}")
    # Call the OCR function with the provided image path
    ocr_result = extract_text_from_image(image_data.image_path,config=config["ocr"])
    joined_text = join_text_from_results(ocr_result)
    
    logger.info(f"Joined Extracted Text: {joined_text}")
    if not joined_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image is too blurry or unclear. Please provide a valid image."
        )
    
    descriptor = Descriptor(config=config["descriptor"])
    description = descriptor.generate(joined_text,fast_generate=fast_generate)
    logger.info(f"Description: {description}")
    # Return the extracted text with status code 200
    return {
        "Description": description,
        "status": status.HTTP_200_OK,
        "message": "Text extraction completed successfully."
    }
    
    #uvicorn app:api --host 0.0.0.0 --port 8000 --reload
    
# Allow the app to run with `python app.py` directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
