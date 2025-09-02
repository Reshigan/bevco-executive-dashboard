@echo off
title Bevco Executive Dashboard - One Click Install

echo.
echo ================================================================
echo   BEVCO EXECUTIVE DASHBOARD - ONE CLICK INSTALL
echo   Complete Business Intelligence Portal
echo ================================================================
echo.
echo This will automatically:
echo   1. Check Python installation
echo   2. Install required packages
echo   3. Download project files (if needed)
echo   4. Set up database with sample data
echo   5. Start the dashboard
echo   6. Open in your browser
echo.
echo Login: admin / admin123
echo URL: http://localhost:5000
echo.
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://python.org/downloads
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Starting automated setup...
echo.

REM Run the automated setup script
python auto_setup.py

if %errorlevel% neq 0 (
    echo.
    echo ================================================================
    echo   SETUP FAILED - TRYING ALTERNATIVE METHOD
    echo ================================================================
    echo.
    echo Trying direct launch...
    
    REM Try alternative launch methods
    if exist "dashboard_portal\app.py" (
        echo Found dashboard files, starting directly...
        cd dashboard_portal
        python app.py
    ) else if exist "start_here.py" (
        echo Using start_here.py...
        python start_here.py
    ) else (
        echo No dashboard files found. Please download the complete project.
        echo Download from: https://github.com/Reshigan/bevco-executive-dashboard
    )
)

echo.
echo ================================================================
echo   DASHBOARD SESSION ENDED
echo ================================================================
echo.
pause