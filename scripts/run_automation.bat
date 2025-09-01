@echo off
REM Bevco Executive Dashboard - Automation Launcher

echo ========================================
echo Bevco Dashboard - Automation Launcher
echo ========================================
echo.

echo Choose your automation method:
echo 1. PowerShell Automation (Recommended for Windows)
echo 2. Python Automation (Cross-platform)
echo 3. Manual Setup Guide
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto powershell
if "%choice%"=="2" goto python
if "%choice%"=="3" goto manual
goto invalid

:powershell
echo.
echo Starting PowerShell automation...
echo This will:
echo - Generate sample data
echo - Create Power BI workspace
echo - Upload datasets
echo - Create dashboards and reports
echo - Publish to app.powerbi.com
echo.
pause
powershell -ExecutionPolicy Bypass -File "PowerBI_Full_Automation.ps1"
goto end

:python
echo.
echo Starting Python automation...
echo This will:
echo - Generate sample data
echo - Connect to Power BI Service
echo - Create workspace and datasets
echo - Build dashboards automatically
echo.
pause
python powerbi_automation.py
goto end

:manual
echo.
echo Opening manual setup guides...
start "" "https://github.com/Reshigan/bevco-executive-dashboard"
echo.
echo Available guides:
echo - ONLINE_POWERBI_SETUP.md (for app.powerbi.com)
echo - QUICK_POWERBI_SETUP.md (15-minute setup)
echo - POWERBI_IMPLEMENTATION_GUIDE.md (complete guide)
goto end

:invalid
echo Invalid choice. Please run the script again and choose 1, 2, or 3.
goto end

:end
echo.
echo Press any key to exit...
pause >nul