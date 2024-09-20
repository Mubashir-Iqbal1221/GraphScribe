import os
from src.utils import upload_image_to_imgbb
from dotenv import load_dotenv
load_dotenv()

# Access the API key
api_key = os.getenv("IMGBB_API_KEY")