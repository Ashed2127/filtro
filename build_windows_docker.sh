#!/bin/bash
# Build Windows .exe using Docker and Wine

echo "========================================="
echo "  Building Windows .exe via Docker/Wine"
echo "========================================="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed or not in PATH"
    exit 1
fi

echo "Building Docker image for Windows executable..."
echo "This may take 10-20 minutes on first run..."
echo ""

# Build the Docker image
docker build -f Dockerfile.windows -t filtro-windows-build .

if [ $? -ne 0 ]; then
    echo "ERROR: Docker build failed"
    exit 1
fi

echo ""
echo "Extracting Windows executable from container..."
echo ""

# Create a container to copy the executable
CONTAINER_ID=$(docker create filtro-windows-build)

# Copy the executable from the container
docker cp $CONTAINER_ID:/app/Filtro.exe ./dist/Filtro.exe 2>/dev/null || \
docker cp $CONTAINER_ID:/app/dist/Filtro.exe ./dist/Filtro.exe 2>/dev/null || \
docker cp $CONTAINER_ID:/dist/Filtro.exe ./dist/Filtro.exe 2>/dev/null

# Clean up the container
docker rm $CONTAINER_ID

# Check if executable was created
if [ -f "./dist/Filtro.exe" ]; then
    echo ""
    echo "========================================="
    echo "  Build successful!"
    echo "========================================="
    echo ""
    echo "Windows executable created: dist/Filtro.exe"
    echo "File size: $(du -h ./dist/Filtro.exe | cut -f1)"
    echo ""
    echo "You can now copy this file to a Windows 10 machine and run it!"
else
    echo ""
    echo "ERROR: Executable not found after build"
    echo "Checking container contents..."
    docker run --rm filtro-windows-build ls -la /app/
    docker run --rm filtro-windows-build ls -la /app/dist/ 2>/dev/null || true
    exit 1
fi
