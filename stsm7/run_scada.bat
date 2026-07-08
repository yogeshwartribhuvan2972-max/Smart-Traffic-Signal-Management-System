@echo off
cls
title AI Traffic SCADA System

echo ============================================
echo         AI TRAFFIC SCADA SYSTEM
echo ============================================
echo.

where python >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Python not found.
    echo.
    echo Please install Python 3.10 or higher.
    echo IMPORTANT:
    echo [x] Add Python to PATH
    echo.
    pause
    exit /b
)

echo Python Found:
python --version
echo.

python -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)"

if errorlevel 1 (
    echo.
    echo ERROR: Python 3.10 or higher required.
    echo Current Version:
    python --version
    echo.
    pause
    exit /b
)

echo Installing Requirements...
python -m pip install --quiet -r requirements.txt

echo.
echo Starting AI Traffic SCADA System...
echo.

python app.py

pause