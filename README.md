# Filtro 📊🖨️

Filtro is a lightweight Windows 10 desktop application designed to eliminate manual spreadsheet filtering and hand-written reporting[cite: 60, 62]. [cite_start]It automatically scans raw daily transaction Excel files, extracts items with active sales, formats them perfectly for **A5 paper size**, and prints directly to the default desk printer[cite: 63, 64].

## 🏗️ Project Structure

```text
filtro/
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── Filtro.spec         # PyInstaller spec file for Windows build
├── build.sh            # Script to compile app to standalone executable via Docker (Linux)
├── build_windows.bat   # Windows batch build script
├── build_windows.ps1   # Windows PowerShell build script
├── src/
│   ├── __init__.py
│   ├── app.py          # Main GUI Application (CustomTkinter)
│   └── processor.py    # Data extraction logic (Pandas)
```

## 🚀 Building the Application

### Linux/Ubuntu Build

To build the standalone executable on Linux/Ubuntu:

```bash
./build.sh
```

This will:
1. Build a Docker image with Python 3.10 and all dependencies
2. Use PyInstaller to create a standalone executable
3. Output the executable to `./dist/Filtro`

### Windows 10 Build

To build the standalone executable on Windows 10, you have two options:

#### Option 1: Using Batch Script (Recommended)

1. Double-click `build_windows.bat` OR run from Command Prompt:
   ```cmd
   build_windows.bat
   ```

#### Option 2: Using PowerShell Script

1. Right-click `build_windows.ps1` and select "Run with PowerShell" OR run from PowerShell:
   ```powershell
   .\build_windows.ps1
   ```
   
   *Note: If you get execution policy errors, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`*

The Windows build will:
1. Check for Python installation (requires Python 3.10+)
2. Create a virtual environment
3. Install PyInstaller and all dependencies
4. Build the executable using the PyInstaller spec file
5. Output the executable to `dist\Filtro.exe`

#### Windows Prerequisites

- Python 3.10 or higher from https://www.python.org/downloads/
- During Python installation, check "Add Python to PATH"
- Administrator rights (for some systems)

## 📋 Requirements

### For Linux/Ubuntu Build
- Docker
- Bash shell

### For Windows 10 Build
- Python 3.10 or higher
- Windows 10 or later
- Administrator rights (recommended)

The application bundles:
- CustomTkinter (modern GUI framework)
- Pandas (Excel data processing)
- OpenPyXL (Excel file support)
- Pillow (image handling)

## 🎯 Features

- Excel file selection and processing
- Configurable filtering options (status column, active value)
- Data preview in the GUI
- Export to Excel for A5 printing
- **NEW**: Automatic business column detection
- **NEW**: Compact business report generation with transaction details and summary sections
- **NEW**: Category-based grouping with counts and amounts
- **NEW**: Print-ready A4 formatting for business reports

## 🔄 Auto-Commit Monitor

The project includes an automatic git commit and push monitor that tracks file changes and automatically commits them to the repository.

### Running the Auto-Commit Monitor

To start the automatic change monitoring:

```bash
python3 auto_commit.py
```

The monitor will:
- Watch the current directory and all subdirectories for file changes
- Automatically commit changes with the message "Auto-commit: Project changes detected"
- Push commits to the remote repository immediately
- Ignore temporary files and directories (.git, __pycache__, .devin, venv, dist, etc.)

**Note**: The monitor requires the `watchdog` library, which is included in requirements.txt.

### Stopping the Monitor

Press `Ctrl+C` to stop the file watcher gracefully.

### Background Operation

To run the monitor in the background:

```bash
python3 auto_commit.py &
```

Or using nohup to keep it running after terminal closure:

```bash
nohup python3 auto_commit.py > auto_commit.log 2>&1 &
```

## 🔧 Troubleshooting

### Windows Build Issues

**Python not found:**
- Ensure Python 3.10+ is installed from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart Command Prompt/PowerShell after installation

**PowerShell execution policy error:**
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Build fails with missing dependencies:**
- Ensure virtual environment is created successfully
- Manually install dependencies: `pip install -r requirements.txt`

**Antivirus blocking the executable:**
- Some antivirus software may flag PyInstaller executables
- Add exception for the `dist` folder during build
- The built executable is safe - it's your own application

### Linux Build Issues

**Docker not running:**
- Start Docker service: `sudo systemctl start docker`
- Ensure you have proper Docker permissions

**Build fails with container errors:**
- Clean Docker system: `docker system prune -a`
- Rebuild the image: `docker build --no-cache -t filtro-builder .`