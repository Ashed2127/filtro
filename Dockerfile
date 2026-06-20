# Use Ubuntu with Wine for cross-platform Windows executable building
FROM ubuntu:22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wine64 \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up Wine
RUN wine64 --version

# Create directory for the app
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies in Wine environment
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pyinstaller
RUN python3 -m pip install -r requirements.txt

# Copy application source code
COPY src/ ./src/

# Build Windows executable using PyInstaller with Wine
RUN wine pyinstaller --onefile --windowed --name "Filtro" --icon=NONE src/app.py

# Move the executable to a known location
RUN mv dist/Filtro.exe /app/Filtro.exe

# Set the output directory
WORKDIR /output

# Copy the executable to output directory
RUN cp /app/Filtro.exe /output/

# The resulting .exe will be in /output/Filtro.exe