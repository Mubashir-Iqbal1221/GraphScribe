import io
from fastapi import FastAPI, HTTPException, status, UploadFile, File
from src.utils import load_config
from src.moondream_describer import FlowgraphDescriber
from loguru import logger
from PIL import Image


config = load_config()
logger.add(
    config["logs"]["log_file_path"],
    rotation=config["logs"]["rotation"],
    retention=config["logs"]["retention"],
)

app = FastAPI()


# Health Check Endpoint
@app.get("/health")
def health_status():
    return {"status": "healthy"}


# Define maximum file size (e.g., 10MB)
MAX_FILE_SIZE = config["MAX_IMAGE_SIZE"]


@app.post("/describe", status_code=status.HTTP_200_OK)
async def extract_text_original(file: UploadFile = File(...)):
    """
    Extract a text description from an uploaded image.

    Parameters:
        - file: An image file uploaded by the user.

    Returns:
        - A JSON response with the description of the image or an error message
          if the image processing fails.
    """
    try:
        print(f"Received file: {file.filename}")

        # Validate content type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is not an image.",
            )

        # Read file content
        contents = await file.read()

        # Validate file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds the 10MB limit.",
            )

        # Open image
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Generate description
        path = config["original_model"]
        logger.info(f"Model Path:{path}")
        descriptor = FlowgraphDescriber(model_path=config["original_model"])
        description = descriptor.generate(image)

        logger.info(f"Description: {description}")
        return {
            "description": description,
            "message": "Text extraction completed successfully.",
        }

    except HTTPException as he:
        # Re-raise HTTP exceptions
        logger.error(f"HTTP error: {he.detail}")
        raise he

    except Exception as e:
        # Handle unexpected errors
        error_message = (
            "An error occurred during description generation using moondream. "
            f"{str(e)}"
        )
        logger.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message,
        )


# Allow the app to run with `python app.py` directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
