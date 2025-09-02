#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Fully Automated Setup
One-click automated installation and launch script
"""

import os
import sys
import subprocess
import platform
import time
import webbrowser
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Colors for cross-platform terminal output
class Colors:
    if platform.system() == "Windows":
        # Windows doesn't support ANSI colors by default
        BLUE = GREEN = YELLOW = RED = BOLD = END = ""
    else:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        END = '\033[0m'

def print_colored(message, color=Colors.BLUE):
    print(f"{color}{message}{Colors.END}")

def print_header():
    print_colored("\n" + "="*70, Colors.BOLD)
    print_colored("🚀 BEVCO EXECUTIVE DASHBOARD - AUTOMATED SETUP", Colors.BOLD)
    print_colored("   Complete Business Intelligence Portal", Colors.BLUE)
    print_colored("="*70, Colors.BOLD)

def check_python():
    """Check Python version and installation"""
    print_colored("\n🐍 Checking Python installation...", Colors.BLUE)
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_colored("❌ Python 3.7+ required", Colors.RED)
        print_colored(f"Current version: {version.major}.{version.minor}", Colors.YELLOW)
        
        # Offer to install Python
        if platform.system() == "Darwin":  # macOS
            print_colored("💡 Install Python with: brew install python3", Colors.YELLOW)
        elif platform.system() == "Windows":
            print_colored("💡 Download Python from: https://python.org/downloads", Colors.YELLOW)
        else:  # Linux
            print_colored("💡 Install Python with: sudo apt install python3 python3-pip", Colors.YELLOW)
        
        return False
    
    print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} detected", Colors.GREEN)
    return True

def install_pip_packages():
    """Install required Python packages"""
    print_colored("\n📦 Installing required packages...", Colors.BLUE)
    
    packages = [
        "flask==2.3.3",
        "flask-socketio==5.3.6",
        "pandas==2.1.1",
        "werkzeug==2.3.7",
        "python-socketio==5.8.0",
        "eventlet==0.33.3",
        "python-dotenv==1.0.0"
    ]
    
    # Upgrade pip first
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      capture_output=True, check=False)
    except:
        pass
    
    failed_packages = []
    for package in packages:
        try:
            print_colored(f"   Installing {package.split('==')[0]}...", Colors.BLUE)
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--quiet"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print_colored(f"   ✅ {package.split('==')[0]}", Colors.GREEN)
            else:
                print_colored(f"   ⚠️  {package.split('==')[0]} (may already be installed)", Colors.YELLOW)
                failed_packages.append(package)
        except Exception as e:
            print_colored(f"   ❌ {package.split('==')[0]} failed: {e}", Colors.RED)
            failed_packages.append(package)
    
    if failed_packages:
        print_colored(f"\n⚠️  Some packages had issues: {len(failed_packages)}", Colors.YELLOW)
        print_colored("Dashboard may still work with existing packages", Colors.YELLOW)
    else:
        print_colored("\n✅ All packages installed successfully!", Colors.GREEN)
    
    return True

def download_project():
    """Download project from GitHub if not present"""
    print_colored("\n📥 Checking project files...", Colors.BLUE)
    
    current_dir = Path.cwd()
    dashboard_dir = current_dir / "dashboard_portal"
    
    # Check if we already have the project
    if dashboard_dir.exists() and (dashboard_dir / "app.py").exists():
        print_colored("✅ Project files found locally", Colors.GREEN)
        return current_dir
    
    # Try to download from GitHub
    print_colored("📥 Downloading project from GitHub...", Colors.BLUE)
    
    try:
        # Create temporary directory
        temp_dir = Path.cwd() / "temp_download"
        temp_dir.mkdir(exist_ok=True)
        
        # Download ZIP file
        zip_url = "https://github.com/Reshigan/bevco-executive-dashboard/archive/refs/heads/main.zip"
        zip_path = temp_dir / "project.zip"
        
        print_colored("   Downloading ZIP file...", Colors.BLUE)
        urllib.request.urlretrieve(zip_url, zip_path)
        
        # Extract ZIP file
        print_colored("   Extracting files...", Colors.BLUE)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Move files to current directory
        extracted_dir = temp_dir / "bevco-executive-dashboard-main"
        if extracted_dir.exists():
            for item in extracted_dir.iterdir():
                dest = current_dir / item.name
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                shutil.move(str(item), str(dest))
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        print_colored("✅ Project downloaded successfully!", Colors.GREEN)
        return current_dir
        
    except Exception as e:
        print_colored(f"❌ Failed to download project: {e}", Colors.RED)
        print_colored("💡 Please manually download from: https://github.com/Reshigan/bevco-executive-dashboard", Colors.YELLOW)
        return None

def setup_database():
    """Set up the database and sample data"""
    print_colored("\n🗄️  Setting up database...", Colors.BLUE)
    
    dashboard_dir = Path.cwd() / "dashboard_portal"
    data_dir = dashboard_dir / "data"
    
    # Create data directory
    data_dir.mkdir(exist_ok=True)
    
    # Database will be created automatically by the Flask app
    print_colored("✅ Database setup ready", Colors.GREEN)
    return True

def start_dashboard():
    """Start the dashboard application"""
    print_colored("\n🚀 Starting dashboard server...", Colors.BLUE)
    
    dashboard_dir = Path.cwd() / "dashboard_portal"
    app_file = dashboard_dir / "app.py"
    
    if not app_file.exists():
        print_colored("❌ Dashboard app.py not found!", Colors.RED)
        return False
    
    # Change to dashboard directory
    original_dir = os.getcwd()
    os.chdir(dashboard_dir)
    
    try:
        print_colored("   Starting Flask server...", Colors.BLUE)
        print_colored("   This may take 10-15 seconds for first-time setup...", Colors.YELLOW)
        
        # Start the Flask application
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for server to start
        print_colored("   Waiting for server to initialize...", Colors.BLUE)
        time.sleep(8)
        
        # Check if process is still running
        if process.poll() is None:
            print_colored("\n" + "="*70, Colors.GREEN)
            print_colored("🎉 DASHBOARD IS RUNNING SUCCESSFULLY!", Colors.GREEN)
            print_colored("="*70, Colors.GREEN)
            print_colored("🌐 URL: http://localhost:5000", Colors.BOLD)
            print_colored("👤 Username: admin", Colors.BLUE)
            print_colored("🔑 Password: admin123", Colors.BLUE)
            print_colored("🤖 AI Chat: Click chat button (bottom-right)", Colors.BLUE)
            print_colored("="*70, Colors.GREEN)
            
            # Open browser
            try:
                webbrowser.open("http://localhost:5000")
                print_colored("🌐 Opening dashboard in your browser...", Colors.GREEN)
            except:
                print_colored("📱 Please manually open: http://localhost:5000", Colors.YELLOW)
            
            print_colored("\n📊 DASHBOARD FEATURES:", Colors.BOLD)
            print_colored("   • Executive Summary with real-time KPIs", Colors.BLUE)
            print_colored("   • Sales Analytics with interactive charts", Colors.BLUE)
            print_colored("   • Financial Dashboard with budget analysis", Colors.BLUE)
            print_colored("   • Operations Dashboard with inventory tracking", Colors.BLUE)
            print_colored("   • AI Analytics with predictive insights", Colors.BLUE)
            print_colored("   • Real-time notifications and updates", Colors.BLUE)
            print_colored("   • Mobile-responsive design", Colors.BLUE)
            
            print_colored("\n🎯 SAMPLE DATA INCLUDED:", Colors.BOLD)
            print_colored("   • 5,000+ realistic business transactions", Colors.BLUE)
            print_colored("   • South African business context (ZAR, regions)", Colors.BLUE)
            print_colored("   • Multiple product categories and customer types", Colors.BLUE)
            
            print_colored("\n🛑 TO STOP: Press Ctrl+C in this terminal", Colors.YELLOW)
            print_colored("📖 HELP: See DASHBOARD_README.md for full documentation", Colors.BLUE)
            
            # Wait for user to stop
            try:
                process.wait()
            except KeyboardInterrupt:
                print_colored("\n🛑 Stopping dashboard...", Colors.YELLOW)
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print_colored("✅ Dashboard stopped successfully", Colors.GREEN)
            
            return True
        else:
            # Process failed to start
            stdout, stderr = process.communicate()
            print_colored("❌ Dashboard failed to start", Colors.RED)
            if stderr:
                print_colored(f"Error details: {stderr[:500]}", Colors.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Error starting dashboard: {e}", Colors.RED)
        return False
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def check_port_available(port=5000):
    """Check if port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def main():
    """Main automated setup function"""
    print_header()
    
    print_colored("\n🎯 AUTOMATED SETUP STARTING...", Colors.BOLD)
    print_colored("This script will:", Colors.BLUE)
    print_colored("   1. Check Python installation", Colors.BLUE)
    print_colored("   2. Install required packages", Colors.BLUE)
    print_colored("   3. Download project files (if needed)", Colors.BLUE)
    print_colored("   4. Set up database", Colors.BLUE)
    print_colored("   5. Start the dashboard", Colors.BLUE)
    print_colored("   6. Open in your browser", Colors.BLUE)
    
    # Step 1: Check Python
    if not check_python():
        return 1
    
    # Step 2: Install packages
    if not install_pip_packages():
        print_colored("⚠️  Continuing despite package issues...", Colors.YELLOW)
    
    # Step 3: Download project if needed
    project_dir = download_project()
    if not project_dir:
        return 1
    
    # Step 4: Setup database
    if not setup_database():
        return 1
    
    # Step 5: Check port availability
    if not check_port_available(5000):
        print_colored("⚠️  Port 5000 is in use. Dashboard will try alternative ports.", Colors.YELLOW)
    
    # Step 6: Start dashboard
    if not start_dashboard():
        print_colored("\n❌ SETUP FAILED", Colors.RED)
        print_colored("💡 Try running manually:", Colors.YELLOW)
        print_colored("   cd dashboard_portal", Colors.YELLOW)
        print_colored("   python3 app.py", Colors.YELLOW)
        return 1
    
    print_colored("\n🎉 AUTOMATED SETUP COMPLETED SUCCESSFULLY!", Colors.GREEN)
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print_colored("\n🛑 Setup cancelled by user", Colors.YELLOW)
        exit(0)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", Colors.RED)
        exit(1)