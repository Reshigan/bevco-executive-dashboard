@echo off
REM Bevco Executive Dashboard - Automation Launcher

echo ========================================
echo Bevco Dashboard - Automation Launcher
echo ========================================
echo.

echo Choose your automation method:
echo 1. Power BI Template Creator (Recommended - No Auth Issues)
echo 2. Web Browser Automation (Guided Process)
echo 3. PowerShell Automation (Advanced Users)
echo 4. Python API Automation (May have auth issues)
echo 5. Manual Setup Guide
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto template
if "%choice%"=="2" goto webautomation
if "%choice%"=="3" goto powershell
if "%choice%"=="4" goto python
if "%choice%"=="5" goto manual
goto invalid

:template
echo.
echo Creating Power BI Template File...
echo This will:
echo - Generate sample data
echo - Create BevcoTemplate.pbit file
echo - No authentication required
echo - Just double-click the .pbit file to use
echo.
pause
python powerbi_template_creator.py
goto end

:webautomation
echo.
echo Starting Web Browser Automation...
echo This will:
echo - Generate sample data
echo - Open Power BI Service in browser
echo - Guide you through manual login
echo - Automate workspace creation and file uploads
echo.
pause
python powerbi_web_automation.py
goto end

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
echo Invalid choice. Please run the script again and choose 1-5.
goto end

:end
echo.
echo Press any key to exit...
pause >nul