#!/bin/bash

# Start the FastAPI app in the background
uvicorn app:app --host 0.0.0.0 --port 8000 --reload &

# Start the Streamlit app
streamlit run demo.py --server.port 8501 --server.address 0.0.0.0
