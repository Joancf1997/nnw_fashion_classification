# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install system dependencies for OpenCV and other required packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

EXPOSE 3000
CMD ["python", "server.py"]