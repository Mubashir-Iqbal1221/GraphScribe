# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app
COPY start.sh /app/

# Make ports 8000 and 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV NAME graphscribe

# Make the start script executable and run it
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
