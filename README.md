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
└── build.sh            # Script to compile app to .exe via Docker