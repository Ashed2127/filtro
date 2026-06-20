# Filtro 📊🖨️

Filtro is a lightweight Windows 10 desktop application designed to eliminate manual spreadsheet filtering and hand-written reporting[cite: 60, 62]. [cite_start]It automatically scans raw daily transaction Excel files, extracts items with active sales, formats them perfectly for **A5 paper size**, and prints directly to the default desk printer[cite: 63, 64].

## 🏗️ Project Structure

```text
filtro/
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── app.py          # Main GUI Application (CustomTkinter)
│   └── processor.py    # Data extraction logic (Pandas)
└── build.sh            # Script to compile app to standalone executable via Docker
```

## 🚀 Building the Application

To build the standalone executable:

```bash
./build.sh
```

This will:
1. Build a Docker image with Python 3.10 and all dependencies
2. Use PyInstaller to create a standalone executable
3. Output the executable to `./dist/Filtro`

## 📋 Requirements

- Docker
- Bash shell

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