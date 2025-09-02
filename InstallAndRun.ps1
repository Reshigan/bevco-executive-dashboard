# Bevco Executive Dashboard - PowerShell One-Click Installer
# Complete automated setup for Windows

param(
    [switch]$SkipDownload
)

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Cyan"
    White = "White"
}

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Show-Header {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor White
    Write-ColoredOutput "  BEVCO EXECUTIVE DASHBOARD - ONE CLICK INSTALL" "Green"
    Write-ColoredOutput "  Complete Business Intelligence Portal" "Blue"
    Write-Host "================================================================" -ForegroundColor White
    Write-Host ""
    Write-Host "This will automatically:"
    Write-Host "  1. Check Python installation"
    Write-Host "  2. Install required packages"
    Write-Host "  3. Download project files (if needed)"
    Write-Host "  4. Set up database with sample data"
    Write-Host "  5. Start the dashboard"
    Write-Host "  6. Open in your browser"
    Write-Host ""
    Write-ColoredOutput "Login: admin / admin123" "Green"
    Write-ColoredOutput "URL: http://localhost:5000" "Green"
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor White
    Write-Host ""
}

function Test-PythonInstallation {
    Write-ColoredOutput "🐍 Checking Python installation..." "Blue"
    
    $pythonCmd = $null
    
    # Try python3 first, then python
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        $pythonCmd = "python3"
        Write-ColoredOutput "✅ python3 found" "Green"
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonCmd = "python"
        Write-ColoredOutput "✅ python found" "Green"
    }
    else {
        Write-ColoredOutput "❌ Python not found!" "Red"
        Write-Host ""
        Write-Host "Please install Python 3.7+ from: https://python.org/downloads"
        Write-Host "Make sure to check 'Add Python to PATH' during installation"
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Check Python version
    try {
        $version = & $pythonCmd --version 2>&1
        Write-ColoredOutput "Python version: $version" "Green"
        return $pythonCmd
    }
    catch {
        Write-ColoredOutput "❌ Error checking Python version" "Red"
        exit 1
    }
}

function Install-RequiredPackages {
    param([string]$PythonCmd)
    
    Write-ColoredOutput "📦 Installing required packages..." "Blue"
    
    # Upgrade pip first
    try {
        & $PythonCmd -m pip install --upgrade pip --quiet 2>$null
    }
    catch {
        # Ignore pip upgrade errors
    }
    
    $packages = @(
        "flask==2.3.3",
        "flask-socketio==5.3.6",
        "pandas==2.1.1",
        "werkzeug==2.3.7",
        "python-socketio==5.8.0",
        "eventlet==0.33.3",
        "python-dotenv==1.0.0"
    )
    
    foreach ($package in $packages) {
        $packageName = $package.Split("==")[0]
        Write-ColoredOutput "   Installing $packageName..." "Blue"
        
        try {
            & $PythonCmd -m pip install $package --quiet
            Write-ColoredOutput "   ✅ $packageName" "Green"
        }
        catch {
            Write-ColoredOutput "   ⚠️  $packageName (may already be installed)" "Yellow"
        }
    }
    
    Write-ColoredOutput "✅ Package installation completed" "Green"
}

function Get-ProjectFiles {
    Write-ColoredOutput "📥 Checking project files..." "Blue"
    
    if ((Test-Path "dashboard_portal") -and (Test-Path "dashboard_portal\app.py")) {
        Write-ColoredOutput "✅ Project files found locally" "Green"
        return $true
    }
    
    if ($SkipDownload) {
        Write-ColoredOutput "❌ Project files not found and download skipped" "Red"
        return $false
    }
    
    Write-ColoredOutput "📥 Downloading project from GitHub..." "Blue"
    
    try {
        $url = "https://github.com/Reshigan/bevco-executive-dashboard/archive/refs/heads/main.zip"
        $zipPath = "project.zip"
        
        # Download using .NET WebClient
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($url, $zipPath)
        
        Write-ColoredOutput "📦 Extracting project files..." "Blue"
        
        # Extract ZIP file
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, ".")
        
        # Move files from extracted directory
        if (Test-Path "bevco-executive-dashboard-main") {
            Get-ChildItem "bevco-executive-dashboard-main" | ForEach-Object {
                Move-Item $_.FullName . -Force
            }
            Remove-Item "bevco-executive-dashboard-main" -Recurse -Force
        }
        
        Remove-Item $zipPath -Force
        Write-ColoredOutput "✅ Project downloaded successfully" "Green"
        return $true
    }
    catch {
        Write-ColoredOutput "❌ Failed to download project: $($_.Exception.Message)" "Red"
        Write-Host "Please manually download from: https://github.com/Reshigan/bevco-executive-dashboard"
        return $false
    }
}

function Start-Dashboard {
    param([string]$PythonCmd)
    
    Write-ColoredOutput "🚀 Starting dashboard server..." "Blue"
    
    if (-not (Test-Path "dashboard_portal\app.py")) {
        Write-ColoredOutput "❌ Dashboard app.py not found!" "Red"
        return $false
    }
    
    Write-ColoredOutput "   Starting Flask server..." "Blue"
    Write-ColoredOutput "   This may take 10-15 seconds for first-time setup..." "Yellow"
    
    try {
        # Change to dashboard directory
        Push-Location "dashboard_portal"
        
        # Start the dashboard
        $process = Start-Process -FilePath $PythonCmd -ArgumentList "app.py" -PassThru -WindowStyle Hidden
        
        # Wait for server to start
        Start-Sleep -Seconds 8
        
        # Check if process is still running
        if (-not $process.HasExited) {
            Write-Host ""
            Write-Host "================================================================" -ForegroundColor Green
            Write-ColoredOutput "🎉 DASHBOARD IS RUNNING SUCCESSFULLY!" "Green"
            Write-Host "================================================================" -ForegroundColor Green
            Write-ColoredOutput "🌐 URL: http://localhost:5000" "White"
            Write-ColoredOutput "👤 Username: admin" "Blue"
            Write-ColoredOutput "🔑 Password: admin123" "Blue"
            Write-ColoredOutput "🤖 AI Chat: Click chat button (bottom-right)" "Blue"
            Write-Host "================================================================" -ForegroundColor Green
            
            # Open browser
            try {
                Start-Process "http://localhost:5000"
                Write-ColoredOutput "🌐 Opening dashboard in your browser..." "Green"
            }
            catch {
                Write-ColoredOutput "📱 Please manually open: http://localhost:5000" "Yellow"
            }
            
            Write-Host ""
            Write-ColoredOutput "📊 DASHBOARD FEATURES:" "White"
            Write-ColoredOutput "   • Executive Summary with real-time KPIs" "Blue"
            Write-ColoredOutput "   • Sales Analytics with interactive charts" "Blue"
            Write-ColoredOutput "   • Financial Dashboard with budget analysis" "Blue"
            Write-ColoredOutput "   • Operations Dashboard with inventory tracking" "Blue"
            Write-ColoredOutput "   • AI Analytics with predictive insights" "Blue"
            Write-ColoredOutput "   • Real-time notifications and updates" "Blue"
            Write-ColoredOutput "   • Mobile-responsive design" "Blue"
            
            Write-Host ""
            Write-ColoredOutput "🎯 SAMPLE DATA INCLUDED:" "White"
            Write-ColoredOutput "   • 5,000+ realistic business transactions" "Blue"
            Write-ColoredOutput "   • South African business context (ZAR, regions)" "Blue"
            Write-ColoredOutput "   • Multiple product categories and customer types" "Blue"
            
            Write-Host ""
            Write-ColoredOutput "🛑 TO STOP: Close this PowerShell window or press Ctrl+C" "Yellow"
            Write-ColoredOutput "📖 HELP: See DASHBOARD_README.md for full documentation" "Blue"
            
            # Wait for user to stop
            try {
                $process.WaitForExit()
            }
            catch {
                Write-ColoredOutput "🛑 Dashboard stopped" "Yellow"
            }
            
            return $true
        }
        else {
            Write-ColoredOutput "❌ Dashboard failed to start" "Red"
            return $false
        }
    }
    catch {
        Write-ColoredOutput "❌ Error starting dashboard: $($_.Exception.Message)" "Red"
        return $false
    }
    finally {
        Pop-Location
    }
}

# Main execution
function Main {
    Show-Header
    
    Write-ColoredOutput "🎯 AUTOMATED SETUP STARTING..." "White"
    Write-Host ""
    
    # Step 1: Check Python
    $pythonCmd = Test-PythonInstallation
    
    # Step 2: Install packages
    Install-RequiredPackages -PythonCmd $pythonCmd
    
    # Step 3: Get project files
    if (-not (Get-ProjectFiles)) {
        Write-ColoredOutput "❌ SETUP FAILED - Could not get project files" "Red"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Step 4: Start dashboard
    if (-not (Start-Dashboard -PythonCmd $pythonCmd)) {
        Write-ColoredOutput "❌ SETUP FAILED - Could not start dashboard" "Red"
        Write-Host ""
        Write-Host "💡 Try running manually:"
        Write-Host "   cd dashboard_portal"
        Write-Host "   $pythonCmd app.py"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host ""
    Write-ColoredOutput "🎉 AUTOMATED SETUP COMPLETED SUCCESSFULLY!" "Green"
}

# Handle Ctrl+C gracefully
try {
    Main
}
catch {
    Write-ColoredOutput "🛑 Setup interrupted" "Yellow"
    exit 0
}