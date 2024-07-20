# Use an official NVIDIA CUDA runtime as a parent image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:${PATH}"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget git curl vim python3-pip python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu118

# Copy the rest of the application code
COPY . .

# Expose the port your FastApi app runs on
EXPOSE 8080

# Set up environment for running the scripts in order
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["python3 fetchAndOrganizeData.py && python3 ingest.py && exec python3 api.py"]
