#!/usr/bin/env python3
"""
Main entry point for Filtro application.
This script handles the imports properly for PyInstaller packaging.
"""

import sys
import os

# Add src directory to path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = os.path.dirname(sys.executable)
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(application_path, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import and run the app
from app import main

if __name__ == "__main__":
    main()
