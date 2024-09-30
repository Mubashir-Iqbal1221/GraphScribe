# GraphScribe version:2.0

GraphScribe is a multimodal project that transcribes handwritten flow graphs and generates meaningful text descriptions from images. It combines FastAPI for backend processing and Streamlit for an intuitive frontend interface. The core functionality is powered by the Moondream model, which provides high-quality image-to-text generation.

## Features

- **Image Upload**: Upload images through an intuitive Streamlit-based web interface.
- **Text Description**: Generates descriptive text from images using quantized multimodal.
- **FastAPI Backend**: Processes images through a FastAPI-based backend for seamless API integration.
- **Streamlit GUI**: A simple and easy-to-use GUI to upload and visualize results in real-time.

## Setup Guide

Follow these steps to set up and run the project on your local machine:

### 1. Clone the Repository

Open your terminal and clone the repository from GitHub (replace `<repository-url>` with your project link):

```bash
git clone https://github.com/Mubashir-Iqbal1221/GraphScribe.git
cd GraphScribe
```

### 2. Install Dependencies

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

This will install FastAPI, Streamlit, and other necessary libraries.

### 3. Download the Model Files

You need to download the quantized Moondream model files to generate image descriptions.

#### a. Create the Model Folder

Run the following command to create the necessary folder structure:

```bash
mkdir -p models/moondream
cd models/moondream
```

#### b. Download the Image Encoder

Download the quantized Moondream image encoder using `wget`:

```bash
wget https://huggingface.co/moondream/moondream2-gguf/resolve/main/moondream2-mmproj-f16.gguf
```

#### c. Download the Text Decoder

Download the quantized Moondream text decoder:

```bash
wget https://huggingface.co/moondream/moondream2-gguf/blob/main/moondream2-text-model-f16.gguf
```

Ensure both files are saved inside the `models/moondream` folder.

### 4. Configure Environment Variables

Create a `.env` file in the root of the project directory to store your environment variables. This file will include your API key for the image upload service (IMGBB).

```bash
touch .env
```

Inside the `.env` file, add the following line (replace `your_api_key_here` with your actual IMGBB API key):

```
IMGBB_API_KEY=your_api_key_here
```

### 5. Run the FastAPI Backend

To start the backend server, run:

```bash
python app.py
```

The FastAPI server will run at `http://localhost:8000`. You can visit `/docs` to see the automatically generated API documentation.

### 6. Run the Streamlit GUI

In a **new terminal window**, navigate back to the project directory and start the Streamlit interface:

```bash
streamlit run demo.py
```

Streamlit will open a web interface in your default browser at `http://localhost:8501`. You can upload images, and the system will generate text descriptions.

## Project Structure

Here is an overview of the project directory structure:

```
.
├── app.py                    # FastAPI backend for handling image processing
├── demo.py                   # Streamlit frontend for image uploading and description generation
├── models/                   # Folder for storing the downloaded Moondream model files
│   └── moondream/            
│       ├── moondream2-mmproj-f16.gguf   # Quantized image encoder
│       └── moondream2-text-model-f16.gguf  # Quantized text decoder
├── configs/                  
│   └── config.yaml           # Configuration settings for the project
├── src/                      # Core source files for image processing and utilities
├── requirements.txt          # List of Python dependencies
├── .env                      # Environment variables (API keys, etc.)
└── README.md                 # This file
```

## Usage

Once the server and GUI are running, follow these steps to use the application:

1. **Open the Web Interface**: Open your browser and navigate to `http://localhost:8501`.
2. **Upload an Image**: Use the "Upload an image file" button to upload an image (supported formats: .jpg, .png, .jpeg).
3. **Generate Description**: After uploading the image, click the "Generate Description" button. The FastAPI backend will process the image and return a description.
4. **View Results**: The text description of the image will be displayed along with the image itself.

## Testing Other Quantized Models

If you'd like to test a different quantized model instead of Moondream, follow these steps:

1. **Download the Model**: 
   - Download the desired quantized model and place it in the `models/<model_name>` folder.

2. **Update the Model Handler**:
   - Open `src/image_description_generator.py` and replace the `MoondreamChatHandler` in the `ChatHandler` section with the appropriate handler for the new model. You can find a list of handlers [here](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#multi-modal-models).

3. **Update the Model Path**:
   - Update the model paths in the `configs/config.yaml` file to point to the newly downloaded model files.

After making these changes, the system will use the new model for generating image descriptions.
---
