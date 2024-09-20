from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel,field_validator
from src.image_description_generator import ImageDescriptionGenerator 
from src.constants import image_encoder_path,decoder_model_path
from loguru import logger

# config = load_config()
# logger.add(LOG_FILE_PATH, rotation=config["logs"]["rotation"], level=config["logs"]["level"])

model = ImageDescriptionGenerator(image_encoder_path=image_encoder_path,
                                  decoder_model_path= decoder_model_path
                                  )
app = FastAPI()

# Define the Pydantic model to validate the input
class ImagePathSchema(BaseModel):
    image_url: str
    
    @field_validator('image_url')
    def check_non_empty(cls, v):
        if not v.strip():
            raise ValueError('Image url cannot be empty')
        return v


# Health Check Endpoint
@app.get("/health")
def health_status():
    return {"status": "healthy"}

# Define the API route
@app.post("/extract-text/", status_code=status.HTTP_200_OK)
def extract_text(image_data: ImagePathSchema):

    logger.info(f"Extracting text from image: {image_data.image_url}")
    # Call the OCR function with the provided image path
    description = model.generate_image_description(image_data.image_url)
    
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
    