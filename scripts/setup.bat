@echo off
REM Bevco Executive Dashboard - Windows Setup Script

echo ==================================================
echo Bevco Executive Dashboard - Automated Setup
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed

REM Create virtual environment
echo.
echo Setting up Python environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Created virtual environment
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Activated virtual environment

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install pandas numpy openpyxl >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Installed Python packages

REM Generate master data
echo.
echo Generating sample data...
python scripts\etl\generate_master_data.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate master data
    pause
    exit /b 1
)
echo [OK] Generated master data files

REM Create Power BI workspace directories
echo.
echo Creating Power BI workspace...
if not exist "powerbi\reports\backups" mkdir powerbi\reports\backups
if not exist "powerbi\datasets\shared" mkdir powerbi\datasets\shared
echo [OK] Created Power BI directories

REM Run data quality check
echo.
echo Running data quality checks...
python scripts\etl\data_quality_check.py
if %errorlevel% neq 0 (
    echo WARNING: Data quality check failed or not found
)

REM Display summary
echo.
echo ==================================================
echo Setup completed successfully!
echo ==================================================
echo.
echo Next steps:
echo 1. Open Power BI Desktop
echo 2. Run: powershell -ExecutionPolicy Bypass .\scripts\import_to_powerbi.ps1
echo 3. Follow the deployment guide in \documentation\technical\
echo.
echo Sample data location: \data\master\
echo DAX measures: \powerbi\datasets\DAX_Measures.txt
echo.
pause