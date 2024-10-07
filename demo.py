import streamlit as st
import requests
from src.utils import load_config
import io
import time

config = load_config()
API_URL = config["FASTAPI_URL"]


# Streamlit App
def main():
    st.title("Image Description Generator")
    st.write("Upload an image, and get a descriptive text.")

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png", "bmp"]
    )

    if uploaded_file is not None:
        # Display the uploaded image
        image_bytes = uploaded_file.read()
        image = io.BytesIO(image_bytes)

        st.image(image, caption="Uploaded Image.", use_column_width=True)
        image.name = uploaded_file.name  # Retain the original file name
        files = [("file", (image.name, image, uploaded_file.type))]
        # files = {"file": uploaded_file.getvalue()}
        files = [("file", ("test.jpg", image, "image/jpeg"))]
        start_time = time.time()
        # Button to send the image to the API
        if st.button("Generate Description"):
            with st.spinner("Generating description..."):
                try:
                    # Send POST request to the FastAPI endpoint
                    response = requests.post(API_URL, files=files)

                    # Check if the request was successful
                    if response.status_code == 200:
                        data = response.json()
                        description = data.get("description", "No description found.")
                        st.success("Description Generated Successfully!")
                        st.write(description)
                        total_time = time.time() - start_time
                        st.write(total_time)
                    else:
                        # Handle errors returned by the API
                        error = response.json().get("detail", "An error occurred.")
                        st.error(
                            f"Error in posting request{response.status_code}: {error}"
                        )

                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")


if __name__ == "__main__":
    main()
