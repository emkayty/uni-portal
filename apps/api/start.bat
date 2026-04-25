@echo off
echo Starting UniPortal API Server...
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    echo OR use: py manage.py runserver 8001
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start server
echo Starting server on http://localhost:8001
python manage.py runserver 8001
pause
