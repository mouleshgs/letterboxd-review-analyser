#!/bin/bash
# Quick Start Script for Mac/Linux
# Letterboxd Review Analytics

echo ""
echo "========================================"
echo " Letterboxd Review Analytics - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[OK] Python is installed: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "[OK] Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Success message
echo ""
echo "========================================"
echo " Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  python app.py"
echo ""
echo "Then open your browser and go to:"
echo "  http://localhost:5000"
echo ""
