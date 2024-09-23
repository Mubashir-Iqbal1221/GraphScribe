#!/bin/bash
# Start the FastAPI application in the background
python app.py &

# Start the Streamlit application in the foreground
streamlit run demo.py
