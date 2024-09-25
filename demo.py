import os
import time
import streamlit as st
import requests
from src.utils import upload_image_to_imgbb,load_config
from dotenv import load_dotenv
from PIL import Image
from loguru import logger


# Load environment variables
load_dotenv()
api_key = os.getenv("IMGBB_API_KEY")
config = load_config()

# Project branding and customization
st.set_page_config(page_title="GraphScribe - OCR & Description Generator", page_icon="📝", layout="centered")

# Sidebar with settings and options
with st.sidebar:
    st.title("GraphScribe")
    st.markdown("### Convert your images into meaningful text and descriptions with ease.")

    # File upload for the image
    uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")

# Main content area
st.markdown("<h1 style='text-align: center; color: #333;'>OCR & Text Description Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Upload an image and extract meaningful descriptions</h4>", unsafe_allow_html=True)

# Define the FastAPI endpoint
FASTAPI_URL = config["FASTAPI_URL"]

# If an image is uploaded, display it and process
if uploaded_file:
    # Extract the file name and extension from the uploaded file
    file_name, file_extension = os.path.splitext(uploaded_file.name)

    # Display the uploaded image in a smaller size
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)  # Display the uploaded image with a smaller width
    
    # Upload the image to imgbb and get the URL
    url = upload_image_to_imgbb(api_key, image,config["imgbb"])["data"]["url"]
    logger.info(f"Image Link: {url}")

    # Show the button only after the image is uploaded and URL is obtained
    if url:
        # Process button to extract the description
        st.markdown("---")
        process_button = st.button("Generate Description", key="process_button", use_container_width=True)
        
        if process_button:
            with st.spinner("Processing... please wait"):
                start_time = time.time()
                # Create payload for the image path
                payload = {
                    "image_url": url
                }

                try:
                    # Send the request to the FastAPI endpoint
                    response = requests.post(FASTAPI_URL, json=payload)
                    response_data = response.json()

                    if response.status_code == 200:
                        st.success("Text extraction completed successfully!")
                        st.markdown("### Generated Description")
                        st.write(response_data.get("Description", "No description available"))
                        
                        end_time = time.time()
                        time_taken = end_time - start_time
                        st.write(f"Time taken: {time_taken:.2f} seconds")
                        
                        # Remove initial image once text is processed
                        st.empty()  # Clear the space for the initial image

                    elif response.status_code == 400:
                        st.write("Provided image is not clear, please upload a clean image.")
                    else:
                        st.error(f"Error: {response_data.get('detail', 'Unknown error occurred')}")

                except Exception as e:
                    st.error(f"Failed to connect to API: {str(e)}")

# Footer for the app
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>© 2024 GraphScribe. All Rights Reserved.</p>", unsafe_allow_html=True)
