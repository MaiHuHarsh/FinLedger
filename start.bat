@echo off
title ExpenseTracker - CRED Inspired Expense Manager
color 0A
echo.
echo ========================================================
echo 💰 ExpenseTracker - CRED Inspired Expense Manager
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if database exists, if not initialize it
if not exist "expense_manager.db" (
    echo 📁 Initializing database...
    python database.py
    if %errorlevel% neq 0 (
        echo ❌ Failed to initialize database
        echo.
        pause
        exit /b 1
    )
    echo ✅ Database initialized successfully!
    echo.
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📦 Installing/Checking dependencies...
    python -m pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo ⚠️ Some dependencies might not have installed correctly
    ) else (
        echo ✅ Dependencies are ready!
    )
    echo.
)

echo 🚀 Starting ExpenseTracker...
echo.
echo 🌐 Open your browser and navigate to: http://localhost:5000
echo 🔐 Demo Login Credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo ⚡ Press Ctrl+C to stop the server
echo ========================================================
echo.

REM Start the Flask application
python app.py

echo.
echo 👋 Server stopped. Thanks for using ExpenseTracker!
echo.
pause
