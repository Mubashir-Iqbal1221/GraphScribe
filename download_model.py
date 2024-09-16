import os
import requests

def download_model(url, dest_path):
    print(f"Downloading model from {url}")
    
    # Send the GET request to download the file
    response = requests.get(url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Write the file content to the destination
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Model downloaded successfully and saved to {dest_path}")
    else:
        print(f"Failed to download model, status code: {response.status_code}")

if __name__ == "__main__":
    # Hugging Face model URL
    hf_model_url = "https://huggingface.co/cjpais/llava-1.6-mistral-7b-gguf/resolve/main/llava-v1.6-mistral-7b.Q4_K_M.gguf"
    
    # Destination path where the model will be saved
    model_path = "models/llava-v1.6-mistral-7b.Q4_K_M.gguf"
    
    # Download the model from Hugging Face
    download_model(hf_model_url, model_path)
