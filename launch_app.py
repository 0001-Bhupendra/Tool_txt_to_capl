#!/usr/bin/env python3
"""
PDF Test Case Converter - Easy Launcher
Run this script to automatically set up and launch the web application.
Works on Windows, Mac, and Linux.
"""

import subprocess
import sys
import os
from pathlib import Path
import platform
import time

def print_header():
    print("\n" + "="*80)
    print("PDF TEST CASE CONVERTER - LAUNCHER")
    print("="*80 + "\n")

def check_python_version():
    """Verify Python 3.8+ is installed."""
    print("✓ Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"✗ ERROR: Python 3.8+ required (found {sys.version_info.major}.{sys.version_info.minor})")
        sys.exit(1)
    print(f"  Found Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def setup_venv():
    """Create or verify virtual environment."""
    print("\n✓ Setting up virtual environment...")
    
    # Determine OS and venv path
    if platform.system() == "Windows":
        venv_path = Path(".venv")
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        venv_path = Path(".venv")
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # Create venv if it doesn't exist
    if not venv_path.exists():
        print("  Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("  Virtual environment created!")
    else:
        print("  Using existing virtual environment")
    
    return python_exe, pip_exe

def install_dependencies(pip_exe):
    """Install required packages."""
    print("\n✓ Installing dependencies...")
    
    # Create requirements file if it doesn't exist
    requirements_file = Path("app_requirements.txt")
    if not requirements_file.exists():
        print("  Creating app_requirements.txt...")
        requirements_file.write_text(
            "streamlit==1.28.1\nPyPDF2==3.0.1\npandas==2.0.3\n"
        )
    
    # Install packages
    print("  Installing packages (this may take 1-2 minutes)...")
    subprocess.run(
        [str(pip_exe), "install", "-r", "app_requirements.txt", "-q"],
        check=False
    )
    print("  Dependencies installed!")

def launch_app(python_exe):
    """Launch the Streamlit application."""
    print("\n✓ Launching application...")
    print("  " + "="*76)
    print("  🌐 Web application starting at: http://localhost:8501")
    print("  💡 Tip: Press Ctrl+C in this terminal to stop the application")
    print("  " + "="*76 + "\n")
    
    # Give user a moment to read the message
    time.sleep(1)
    
    # Launch Streamlit
    try:
        subprocess.run(
            [str(python_exe), "-m", "streamlit", "run", "app.py"],
            check=False
        )
    except KeyboardInterrupt:
        print("\n\n✓ Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error launching application: {e}")
        sys.exit(1)

def main():
    """Main launcher flow."""
    print_header()
    
    try:
        # Check Python version
        check_python_version()
        
        # Setup venv
        python_exe, pip_exe = setup_venv()
        
        # Install dependencies
        install_dependencies(pip_exe)
        
        # Launch app
        launch_app(python_exe)
        
    except KeyboardInterrupt:
        print("\n\n✗ Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
