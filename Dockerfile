
# Use Python 3.10 base image
FROM python:3.10-slim

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create directory for the app
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install pyinstaller
RUN pip install -r requirements.txt

# Copy application source code
COPY src/ ./src/

# Build standalone executable using PyInstaller
RUN pyinstaller --onefile --name "Filtro" src/app.py

# Move the executable to a known location
RUN mv dist/Filtro /app/Filtro

# Set the output directory
WORKDIR /output

# Copy the executable to output directory
RUN cp /app/Filtro /output/

# The resulting executable will be in /output/Filtro