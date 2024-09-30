# GraphScribe (Version: 1.0)

GraphScribe is a project that extracts text from images using PaddleOCR and generates intelligent descriptions using quantized large language models (LLMs). It combines FastAPI for backend processing and Streamlit for an intuitive frontend interface.

## Features

- **PaddleOCR Integration**: Extracts text from images using PaddleOCR.
- **Quantized LLMs**: Generates descriptive text from the extracted OCR results using quantized large language models (e.g., LLaVA).
- **FastAPI Backend**: Processes images through a FastAPI-based backend for seamless API integration.
- **Streamlit GUI**: A simple and easy-to-use GUI to upload images and view text extraction results.

## Prerequisites

Make sure you have the following installed before running the project:

- Python 3.x
- `pip` (Python package manager)

## Setup Guide

### 1. Clone the Repository

Clone the repository from GitHub to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Download the Quantized Models

You need to download the quantized models to generate text descriptions from OCR results.

#### a. Create the Model Folder

```bash
mkdir -p models/llava
cd models/llava
```

#### b. Download the Quantized Model (LLaVA)

Download the quantized LLaVA model using `wget`:

```bash
wget https://huggingface.co/llava/llava-v1.6-mistral-7b.Q4_K_M.gguf
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project to store your environment variables (if needed). For example, you might store API keys here if required for image hosting services.

### 5. Run the FastAPI Backend

Start the FastAPI backend by running:

```bash
python app.py
```

The FastAPI server will run at `http://localhost:8000`.

### 6. Run the Streamlit GUI

In another terminal, navigate to the project directory and run:

```bash
streamlit run demo.py
```

This will open the Streamlit web interface in your browser at `http://localhost:8501`.

## Project Structure

```
.
├── app.py                     # FastAPI backend for handling OCR and text generation
├── demo.py                    # Streamlit frontend for uploading images and extracting text
├── configs/
│   └── config.yaml            # Configuration settings for OCR and LLMs
├── models/                    # Folder to store downloaded models
│   └── llava/
│       ├── llava-v1.6-mistral-7b.Q4_K_M.gguf  # Quantized model
├── src/                       # Core logic for OCR and description generation
│   ├── ocr_service.py         # Functions for OCR using PaddleOCR
│   ├── generate_description.py # Generates description using LLMs
│   └── utils.py               # Helper functions
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Usage

Once the FastAPI server and Streamlit GUI are running, follow these steps:

1. **Open the Web Interface**: Open your browser and navigate to `http://localhost:8501`.
2. **Upload an Image**: Use the "Upload an image file" button to upload an image (.jpg, .png, .jpeg).
3. **Generate Description**: Click the "Extract Text" button to start the OCR and text generation process.
4. **View Results**: The extracted text and generated description will be displayed on the web interface.

## Testing Other Quantized LLMs

If you want to test other quantized LLMs instead of LLaVA, follow these steps:

1. **Download the Model**: 
   - Download the desired quantized LLM and place it in the `models/<model_name>` folder.

2. **Update the Model Path**:
   - Modify the path to the model in the `configs/config.yaml` file to point to the newly downloaded model.

After making these changes, the system will use the new quantized model for generating descriptions from OCR results.

## Troubleshooting

- **Error: Cannot Connect to API**: Ensure that the FastAPI server is running on `http://localhost:8000`.
- **Blurry Image**: If the image is too blurry, PaddleOCR may fail to extract text. Ensure the image quality is clear.
- **Model Not Found**: Ensure the model files are correctly downloaded and placed in the `models` folder.

---