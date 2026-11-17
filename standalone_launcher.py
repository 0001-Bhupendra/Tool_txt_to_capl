#!/usr/bin/env python3
"""
PDF Test Case Converter - Standalone Launcher
Runs Streamlit app as an executable
"""

import subprocess
import sys
import os
from pathlib import Path
import webbrowser
import time

def main():
    """Launch the Streamlit web app."""
    
    # Get the directory where this script is located
    app_dir = Path(__file__).parent.absolute()
    app_py = app_dir / "app.py"
    
    # Check if app.py exists
    if not app_py.exists():
        print(f"ERROR: app.py not found in {app_dir}")
        print("Make sure all files are extracted correctly.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Print startup message
    print("\n" + "="*80)
    print("PDF TEST CASE CONVERTER - STANDALONE EDITION")
    print("="*80)
    print("\n✓ Starting web application...")
    print("  Opening browser to http://localhost:8501\n")
    print("  Tip: Press Ctrl+C to stop the application\n")
    
    # Launch Streamlit
    try:
        # Start Streamlit
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_py), "--logger.level=error"],
            cwd=str(app_dir)
        )
    except KeyboardInterrupt:
        print("\n\n✓ Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
