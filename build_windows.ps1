# Filtro Windows Build Script (PowerShell)
# This script builds a standalone Windows executable using PyInstaller

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Filtro Windows Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10 or higher from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Gray
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "Virtual environment created successfully." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install PyInstaller
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create output directory
if (-not (Test-Path "dist")) {
    New-Item -ItemType Directory -Path "dist" | Out-Null
}

# Build executable using PyInstaller spec file
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building Windows executable..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

pyinstaller Filtro.spec --clean

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if executable was created
if (Test-Path "dist\Filtro.exe") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: dist\Filtro.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now run the executable on Windows 10!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "WARNING: Expected executable not found in dist folder" -ForegroundColor Yellow
    Write-Host "Checking alternative locations..." -ForegroundColor Yellow
    Get-ChildItem -Recurse -Filter "*.exe"
}

Read-Host "Press Enter to exit"
