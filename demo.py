import os
import streamlit as st
import requests
from PIL import Image

# Project branding and customization
st.set_page_config(page_title="GraphScribe - OCR & Description Generator", page_icon="📝", layout="centered")

# Sidebar with settings and options
with st.sidebar:
    st.title("GraphScribe")
    st.markdown("### Convert your images into meaningful text and descriptions with ease.")

    # File upload for the image
    uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "png", "jpeg"])

    # Fast Generate Option
    fast_generate = st.checkbox("Fast Generate", value=False)
    show_result_image = st.checkbox("Display Detected Text", value=False)
    
    st.markdown("---")

# Main content area
st.markdown("<h1 style='text-align: center; color: #333;'>OCR & Text Description Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Upload an image and extract meaningful descriptions</h4>", unsafe_allow_html=True)

# Define the FastAPI endpoint
FASTAPI_URL = "http://localhost:8000/extract-text/"

# If an image is uploaded, display it and process
if uploaded_file:
    # Extract the file name and extension from the uploaded file
    file_name, file_extension = os.path.splitext(uploaded_file.name)

    # Display the uploaded image in a smaller size
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)  # Display the uploaded image with a smaller width
    
    # Specify directory to save the uploaded image
    save_directory = os.path.join(os.getcwd(), "dataset")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Save uploaded image to the specified folder
    image_path = os.path.join(save_directory, f"{file_name}{file_extension}")
    
    # Save image
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process button
    st.markdown("---")
    process_button = st.button("Extract Text", key="process_button", use_container_width=True)
    
    if process_button:
        with st.spinner("Processing... please wait"):
            # Create the URL with the query parameter for fast_generate
            api_url = f"{FASTAPI_URL}?fast_generate={fast_generate}"

            # Create payload for the image path
            payload = {
                "image_path": image_path
            }

            try:
                # Send the request to the FastAPI endpoint
                response = requests.post(api_url, json=payload)
                
                response_data = response.json()

                if response.status_code == 200:
                    st.success("Text extraction completed successfully!")
                    st.markdown("### Generated Description")
                    st.write(response_data.get("Description", "No description available"))

                    # Remove initial image once text is processed
                    st.empty()  # Clear the space for the initial image

                    # Automatically show the processed image after text extraction
                    if show_result_image:
                        # Construct the processed image path dynamically
                        processed_image_path = f"outputs/test/{file_name}{file_extension}"

                        # Debug: Print the processed image path
                        st.write("Processed Image Path: ", processed_image_path)

                        # Check if the processed image path exists and display the image
                        if os.path.exists(processed_image_path):
                            st.image(processed_image_path, caption="Processed Image", use_column_width=True)
                        else:
                            current_directory = os.getcwd()
                            # Construct the path to the outputs folder
                            final_image_path = os.path.join(current_directory, processed_image_path)
                            st.warning(f"The processed image path '{final_image_path}' does not exist. Please check the path.")
                
                elif response.status_code == 400:
                    st.write(" Provided image is not clear, upload clean image.")
                else:
                    st.error(f"Error: {response_data.get('detail', 'Unknown error occurred')}")
            except Exception as e:
                st.error(f"Failed to connect to API: {str(e)}")

# Footer for the app
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>© 2024 GraphScribe. All Rights Reserved.</p>", unsafe_allow_html=True)
