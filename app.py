from fastapi import FastAPI
from fastapi.responses import FileResponse
import os,uvicorn

# Initialize FastAPI app
app = FastAPI()

# Define the folder where images are stored (same folder as the repo)
IMAGE_FOLDER = os.path.join(os.getcwd(), 'dataset')

# Route to serve images
@app.get("/image/{filename}")
async def serve_image(filename: str):
    # Define the path to the image
    file_path = os.path.join(IMAGE_FOLDER, filename)
    
    # Check if the file exists
    if os.path.isfile(file_path):
        # Serve the image file
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}

if __name__ == '__main__':
    # Start the FastAPI app using uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000)
