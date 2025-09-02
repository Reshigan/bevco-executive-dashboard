#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Start Here
The simplest way to start your dashboard - just run this file!
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Colors for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message, color=Colors.BLUE):
    print(f"{color}{message}{Colors.END}")

def print_header():
    print_colored("\n" + "="*60, Colors.BOLD)
    print_colored("🚀 BEVCO EXECUTIVE DASHBOARD", Colors.BOLD)
    print_colored("   Modern Business Intelligence Portal", Colors.BLUE)
    print_colored("="*60, Colors.BOLD)

def check_and_install_packages():
    """Install required packages"""
    print_colored("\n📦 Setting up dependencies...", Colors.BLUE)
    
    packages = [
        "flask==2.3.3",
        "flask-socketio==5.3.6", 
        "pandas==2.1.1",
        "werkzeug==2.3.7",
        "python-socketio==5.8.0",
        "eventlet==0.33.3"
    ]
    
    for package in packages:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print_colored(f"✅ {package.split('==')[0]}", Colors.GREEN)
            else:
                print_colored(f"⚠️  {package.split('==')[0]} (may already be installed)", Colors.YELLOW)
        except:
            print_colored(f"⚠️  {package.split('==')[0]} (skipped)", Colors.YELLOW)
    
    print_colored("✅ Dependencies ready!", Colors.GREEN)

def start_dashboard():
    """Start the dashboard application"""
    print_colored("\n🚀 Starting your dashboard...", Colors.BLUE)
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    dashboard_dir = script_dir / "dashboard_portal"
    
    # Check if dashboard directory exists
    if not dashboard_dir.exists():
        print_colored("❌ Dashboard files not found!", Colors.RED)
        print_colored(f"Expected location: {dashboard_dir}", Colors.YELLOW)
        print_colored("\nPlease ensure you have the complete project structure.", Colors.YELLOW)
        return False
    
    # Check if app.py exists
    app_file = dashboard_dir / "app.py"
    if not app_file.exists():
        print_colored("❌ Dashboard app.py not found!", Colors.RED)
        print_colored(f"Expected location: {app_file}", Colors.YELLOW)
        return False
    
    print_colored(f"📁 Dashboard found at: {dashboard_dir}", Colors.GREEN)
    
    # Change to dashboard directory
    original_dir = os.getcwd()
    os.chdir(dashboard_dir)
    
    try:
        print_colored("\n⏳ Starting server (this may take a moment)...", Colors.BLUE)
        
        # Start the Flask application
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for server to start
        time.sleep(4)
        
        # Check if process is still running
        if process.poll() is None:
            print_colored("\n" + "="*60, Colors.GREEN)
            print_colored("🎉 DASHBOARD IS RUNNING!", Colors.GREEN)
            print_colored("="*60, Colors.GREEN)
            print_colored("🌐 URL: http://localhost:5000", Colors.BOLD)
            print_colored("👤 Username: admin", Colors.BLUE)
            print_colored("🔑 Password: admin123", Colors.BLUE)
            print_colored("🤖 AI Chat: Click chat button (bottom-right)", Colors.BLUE)
            print_colored("="*60, Colors.GREEN)
            
            # Try to open browser
            try:
                webbrowser.open("http://localhost:5000")
                print_colored("🌐 Opening in your default browser...", Colors.GREEN)
            except:
                print_colored("📱 Please manually open: http://localhost:5000", Colors.YELLOW)
            
            print_colored("\n🛑 To stop: Press Ctrl+C in this terminal", Colors.YELLOW)
            print_colored("📊 Enjoy your executive dashboard!", Colors.GREEN)
            
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
                print_colored(f"Error: {stderr}", Colors.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Error starting dashboard: {e}", Colors.RED)
        return False
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def main():
    """Main function"""
    print_header()
    
    print_colored("\n📊 DASHBOARD FEATURES:", Colors.BOLD)
    print_colored("   • Executive Summary with real-time KPIs", Colors.BLUE)
    print_colored("   • Sales Analytics with interactive charts", Colors.BLUE)
    print_colored("   • Financial Dashboard with budget analysis", Colors.BLUE)
    print_colored("   • Operations Dashboard with inventory tracking", Colors.BLUE)
    print_colored("   • AI Analytics with predictive insights", Colors.BLUE)
    print_colored("   • Real-time notifications and AI chat assistant", Colors.BLUE)
    
    print_colored("\n🎯 SAMPLE DATA:", Colors.BOLD)
    print_colored("   • 5,000+ realistic business transactions", Colors.BLUE)
    print_colored("   • South African business context (ZAR, regions)", Colors.BLUE)
    print_colored("   • Multiple product categories and customer types", Colors.BLUE)
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored("❌ Python 3.8+ required", Colors.RED)
        print_colored(f"Current version: {version.major}.{version.minor}", Colors.YELLOW)
        return 1
    
    print_colored(f"\n✅ Python {version.major}.{version.minor}.{version.micro} detected", Colors.GREEN)
    
    # Install packages
    check_and_install_packages()
    
    # Start dashboard
    if start_dashboard():
        return 0
    else:
        print_colored("\n❌ Failed to start dashboard", Colors.RED)
        print_colored("💡 Troubleshooting tips:", Colors.YELLOW)
        print_colored("   1. Make sure you're in the project root directory", Colors.YELLOW)
        print_colored("   2. Check that dashboard_portal/app.py exists", Colors.YELLOW)
        print_colored("   3. Try running: python3 dashboard_portal/app.py", Colors.YELLOW)
        return 1

if __name__ == "__main__":
    exit(main())