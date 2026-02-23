@echo off
REM PyTestGenie Authentication System - Quick Setup Script for Windows

echo ============================================================
echo   PyTestGenie Authentication System - Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed
echo.

echo [3/4] Checking MongoDB connection...
echo NOTE: Make sure MongoDB is running on localhost:27017
echo If not installed, download from: https://www.mongodb.com/try/download/community
echo.

echo [4/4] Setup Complete!
echo.
echo ============================================================
echo   Next Steps:
echo ============================================================
echo   1. Start MongoDB (if not running):
echo      - Windows Service: net start MongoDB
echo      - Manual: mongod --dbpath C:\data\db
echo.
echo   2. Start the Flask application:
echo      cd backend
echo      python app_unified.py
echo.
echo   3. Create admin user:
echo      python test_auth_system.py
echo      OR use curl/Postman with the API
echo.
echo   4. Read documentation:
echo      - AUTH_SYSTEM_GUIDE.md
echo      - AUTH_API_REFERENCE.md
echo ============================================================
echo.

pause
