#!/bin/bash

# Filtro Build Script
# This script builds a standalone executable using Docker and PyInstaller

set -e

IMAGE_NAME="filtro-builder"
CONTAINER_NAME="filtro-build-container"
OUTPUT_DIR="./dist"

echo "🚀 Starting Filtro build process..."

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t "$IMAGE_NAME" .

# Run the container to build the executable
echo "🔨 Building standalone executable..."
docker run --name "$CONTAINER_NAME" "$IMAGE_NAME"

# Copy the executable from the container
echo "📋 Copying executable to output directory..."
docker cp "$CONTAINER_NAME:/output/Filtro" "$OUTPUT_DIR/"

# Clean up the container
echo "🧹 Cleaning up..."
docker rm "$CONTAINER_NAME"

echo "✅ Build complete! Executable available at: $OUTPUT_DIR/Filtro"
echo "🎉 You can now run the executable!"