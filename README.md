# GraphScribe version: 2.0

GraphScribe is a multimodal project that transcribes handwritten flow graphs and generates meaningful text descriptions from images. It combines FastAPI for backend processing and Streamlit for an intuitive frontend interface. The core functionality is powered by the Moondream model, which provides high-quality image-to-text generation.

## Features

- **Image Upload**: Upload images through an intuitive Streamlit-based web interface.
- **Text Description**: Generates descriptive text from images using a multimodal model.
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
mkdir -p transformers_modules
cd transformers_modules
```

#### b. Download the Repo and Model

```bash
git clone https://huggingface.co/vikhyatk/moondream2
cd moondream2
```

Download the Moondream model using `wget`:

```bash
wget https://huggingface.co/vikhyatk/moondream2/resolve/main/model.safetensors
```

### 4. Run the FastAPI Backend

To start the backend server, run:

```bash
python app.py
```

The FastAPI server will run at `http://localhost:8000`. You can visit `/docs` to see the API documentation.

### 5. Run the Streamlit GUI

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
├── transformers_modules
│   └── moondream/            # Downloaded Moondream model files
├── configs/                  
│   └── config.yaml           # Configuration settings for the project
├── src/                      # Core source files for image processing and utilities
├── requirements.txt          # List of Python dependencies
└── README.md                 # This file
```

## Usage

Once the server and GUI are running, follow these steps to use the application:

1. **Open the Web Interface**: Open your browser and navigate to `http://localhost:8501`.
2. **Upload an Image**: Use the "Upload an image file" button to upload an image (supported formats: .jpg, .png, .jpeg).
3. **Generate Description**: After uploading the image, click the "Generate Description" button. The FastAPI backend will process the image and return a description.
4. **View Results**: The text description of the image will be displayed along with the image itself.

--