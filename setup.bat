::========================================
:: Quick Start Script for Windows PowerShell
:: Letterboxd Review Analytics
::========================================

@echo off
cls
echo.
echo ========================================
echo  Letterboxd Review Analytics - Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python is installed

:: Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
)

:: Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

:: Success message
echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   python app.py
echo.
echo Then open your browser and go to:
echo   http://localhost:5000
echo.
pause
