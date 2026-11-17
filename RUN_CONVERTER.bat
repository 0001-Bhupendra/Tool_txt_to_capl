@echo off
REM PDF Test Case Converter - Standalone Launcher
REM Double-click this file to run the application

setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo PDF TEST CASE CONVERTER - STANDALONE EDITION
echo ================================================================================
echo.
echo Starting application...
echo Opening browser to http://localhost:8501
echo.
echo Tip: Close the terminal window to stop the application
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or later from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Get the directory where this batch file is located
set APP_DIR=%~dp0

REM Install dependencies if needed
echo Checking dependencies...
python -m pip install streamlit PyPDF2 pandas -q

REM Launch the Streamlit app
echo.
cd /d "%APP_DIR%"
python -m streamlit run app.py --logger.level=error

pause
