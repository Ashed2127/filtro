@echo off
REM Filtro Windows Build Script
REM This script builds a standalone Windows executable using PyInstaller

setlocal enabledelayedexpansion

echo ========================================
echo    Filtro Windows Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create output directory
if not exist dist mkdir dist

REM Build executable using PyInstaller spec file
echo.
echo ========================================
echo Building Windows executable...
echo ========================================
echo.

pyinstaller Filtro.spec --clean

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed
    pause
    exit /b 1
)

REM Move executable to dist folder if needed
if exist dist\Filtro.exe (
    echo.
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo Executable location: dist\Filtro.exe
    echo.
    echo You can now run the executable on Windows 10!
    echo.
) else (
    echo.
    echo WARNING: Expected executable not found in dist folder
    echo Checking alternative locations...
    dir /s /b *.exe 2>nul
)

pause
