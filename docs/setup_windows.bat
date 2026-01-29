@echo off
REM Personalized Tutor Agent - Windows Setup Script
REM This script automates the setup process for Windows users

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   Personalized Tutor Agent - Automated Windows Setup            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found! Please install Python first from:
    echo   https://www.python.org/downloads/
    echo   Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo ✓ Python found!
python --version
echo.

REM Check if Git is installed
echo [2/5] Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Git not found! Please install Git first from:
    echo   https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✓ Git found!
git --version
echo.

REM Create virtual environment
echo [3/5] Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created!
)
echo.

REM Activate virtual environment
echo [4/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated!
echo.

REM Install requirements
echo [5/5] Installing Python dependencies...
echo This may take 5-10 minutes depending on your internet speed...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ All dependencies installed!
echo.

echo ╔════════════════════════════════════════════════════════════════╗
echo ║   ✓ SETUP COMPLETED SUCCESSFULLY!                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo   1. Run the pipeline: python run_pipeline.py
echo   2. Launch dashboard: streamlit run app.py
echo.
echo For detailed instructions, see INSTALLATION_GUIDE.md
echo.
pause
