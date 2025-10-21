@echo off
REM Run script for Monday.com Item Duplicator

echo ============================================================
echo Monday.com Item Duplicator
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist .venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please create a .env file with your MONDAY_API_KEY
    pause
    exit /b 1
)

echo Configuration:
echo   Source: Content Creation Machine ^(Board: 8891540298^)
echo   Group: group_mktas044 ^(Ready to Upload^)
echo   Destination: [TruLaw] - Workshop ^(Board: 5422445730^)
echo   Group: group_mknzndef ^(Requested^)
echo.
echo ============================================================
echo.

REM Prompt for item name
set /p ITEM_NAME="Enter item name to duplicate (or press Enter for ALL items): "

REM Run the script with the item name (or empty for batch mode)
echo.
echo Running Monday.com Item Duplicator...
echo.

if "%ITEM_NAME%"=="" (
    echo [BATCH MODE] Processing ALL items from source group...
    python monday_item_duplicator.py
) else (
    echo [SINGLE ITEM MODE] Duplicating: %ITEM_NAME%
    python monday_item_duplicator.py "%ITEM_NAME%"
)

echo.
echo ============================================================
echo.
pause
