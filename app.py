from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from src.ocr_service import extract_text_from_image

app = FastAPI()

# Define the Pydantic model to validate the input
class ImagePathSchema(BaseModel):
    image_path: str

# Define the API route
@app.post("/extract-text/", status_code=status.HTTP_200_OK)
def extract_text(image_data: ImagePathSchema):
    # Call the OCR function with the provided image path
    result = extract_text_from_image(image_data.image_path)
    
    # Handle cases where OCR fails (e.g., blurry images)
    if result is None:
        # Raise an HTTPException with status code 400 for a bad request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image is too blurry or unclear. Please provide a valid image."
        )
    
    # Return the extracted text with status code 200
    return {
        "ocr_results": result,
        "status": status.HTTP_200_OK,
        "message": "Text extraction completed successfully."
    }
    
    #uvicorn app:app --host 0.0.0.0 --port 8000 --reload