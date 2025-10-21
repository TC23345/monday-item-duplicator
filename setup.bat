@echo off
REM Setup script for Monday.com Item Duplicator using UV
REM Run this script to set up the project

echo ============================================================
echo Monday.com Item Duplicator - Setup Script (UV)
echo ============================================================
echo.

REM Check if UV is installed
uv --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] UV is not installed or not in PATH
    echo.
    echo Please install UV using one of these methods:
    echo   - Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo   - Or with pip: pip install uv
    echo.
    echo After installing, restart this script.
    pause
    exit /b 1
)

echo [1/4] UV detected
uv --version
echo.

REM Create virtual environment with UV
echo [2/4] Creating virtual environment with UV...
if exist .venv (
    echo Virtual environment already exists, skipping...
) else (
    uv venv .venv
    echo Virtual environment created successfully!
)
echo.

REM Install dependencies with UV
echo [3/4] Installing dependencies with UV...
uv pip install -r requirements.txt
echo.

REM Check if .env file exists
echo [4/4] Checking configuration...
if exist .env (
    echo [OK] .env file found
    findstr /C:"MONDAY_API_KEY=" .env >nul
    if errorlevel 1 (
        echo [WARNING] MONDAY_API_KEY not found in .env
        echo Please add your API key to the .env file
    ) else (
        echo [OK] MONDAY_API_KEY found in .env
    )
) else (
    echo [ERROR] .env file not found!
    echo Please create a .env file with your MONDAY_API_KEY
)
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Make sure your API key is in the .env file
echo 2. Run: run.bat
echo 3. Enter an item name to duplicate, or press Enter for batch mode
echo.
echo The virtual environment will be automatically activated when you run.bat
echo.
pause
