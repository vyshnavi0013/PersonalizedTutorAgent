#!/bin/bash
# Personalized Tutor Agent - Mac/Linux Setup Script
# This script automates the setup process for Mac and Linux users

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Personalized Tutor Agent - Automated Setup (Mac/Linux)        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python3 not found! Please install Python first:"
    echo "  Mac: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora/RHEL: sudo dnf install python3 python3-pip"
    exit 1
fi
echo "✓ Python found!"
python3 --version
echo ""

# Check if Git is installed
echo "[2/5] Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo "✗ Git not found! Please install Git first:"
    echo "  Mac: brew install git"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  Fedora/RHEL: sudo dnf install git"
    exit 1
fi
echo "✓ Git found!"
git --version
echo ""

# Create virtual environment
echo "[3/5] Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "✗ Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created!"
fi
echo ""

# Activate virtual environment
echo "[4/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "✗ Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated!"
echo ""

# Install requirements
echo "[5/5] Installing Python dependencies..."
echo "This may take 5-10 minutes depending on your internet speed..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "✗ Failed to install dependencies"
    exit 1
fi
echo "✓ All dependencies installed!"
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   ✓ SETUP COMPLETED SUCCESSFULLY!                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Run the pipeline: python3 run_pipeline.py"
echo "  2. Launch dashboard: streamlit run app.py"
echo ""
echo "For detailed instructions, see INSTALLATION_GUIDE.md"
echo ""
