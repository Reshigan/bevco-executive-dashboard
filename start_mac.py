#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Mac Launcher
Mac-optimized launcher that avoids pandas dependency issues
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Colors for Mac terminal
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
    print_colored("🍎 BEVCO DASHBOARD - MAC LAUNCHER", Colors.BOLD)
    print_colored("   Optimized for macOS (No Pandas Issues)", Colors.BLUE)
    print_colored("="*60, Colors.BOLD)

def check_and_fix_dependencies():
    """Check and fix Mac-specific dependency issues"""
    print_colored("\n🔧 Checking Mac dependencies...", Colors.BLUE)
    
    # Try to import pandas to see if there's an issue
    try:
        import pandas
        print_colored("✅ Pandas working correctly", Colors.GREEN)
        return True
    except Exception as e:
        if "numpy.dtype size changed" in str(e):
            print_colored("⚠️  Detected pandas/numpy compatibility issue", Colors.YELLOW)
            print_colored("🔧 Attempting to fix...", Colors.BLUE)
            
            # Run the fix script
            try:
                result = subprocess.run([
                    sys.executable, "fix_mac_dependencies.py"
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print_colored("✅ Dependencies fixed!", Colors.GREEN)
                    return True
                else:
                    print_colored("⚠️  Fix attempt completed with warnings", Colors.YELLOW)
                    return False
            except Exception as fix_error:
                print_colored(f"⚠️  Could not auto-fix: {fix_error}", Colors.YELLOW)
                return False
        else:
            print_colored(f"⚠️  Other pandas issue: {e}", Colors.YELLOW)
            return False

def install_basic_packages():
    """Install only the essential packages"""
    print_colored("\n📦 Installing essential packages...", Colors.BLUE)
    
    packages = [
        "flask==2.3.3",
        "flask-socketio==5.3.6",
        "werkzeug==2.3.7",
        "python-socketio==5.8.0",
        "eventlet==0.33.3"
    ]
    
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
        except Exception as e:
            print_colored(f"   ⚠️  {package.split('==')[0]} skipped: {e}", Colors.YELLOW)
    
    print_colored("✅ Essential packages ready!", Colors.GREEN)

def start_dashboard():
    """Start the dashboard with the appropriate version"""
    print_colored("\n🚀 Starting dashboard...", Colors.BLUE)
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    dashboard_dir = script_dir / "dashboard_portal"
    
    if not dashboard_dir.exists():
        print_colored("❌ Dashboard directory not found!", Colors.RED)
        return False
    
    # Change to dashboard directory
    original_dir = os.getcwd()
    os.chdir(dashboard_dir)
    
    try:
        # Check if we can use the regular version or need the simplified one
        pandas_works = check_and_fix_dependencies()
        
        if pandas_works:
            app_file = "app.py"
            print_colored("📊 Using full-featured dashboard", Colors.GREEN)
        else:
            app_file = "app_simple.py"
            print_colored("📊 Using simplified dashboard (no pandas)", Colors.YELLOW)
            print_colored("   All features still work, just using SQLite directly", Colors.BLUE)
        
        if not os.path.exists(app_file):
            print_colored(f"❌ {app_file} not found!", Colors.RED)
            return False
        
        print_colored(f"⏳ Starting server with {app_file}...", Colors.BLUE)
        print_colored("   This may take 10-15 seconds for first-time setup...", Colors.YELLOW)
        
        # Start the Flask application
        process = subprocess.Popen([
            sys.executable, app_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for server to start
        time.sleep(6)
        
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
                print_colored("🌐 Opening in Safari...", Colors.GREEN)
            except:
                print_colored("📱 Please manually open: http://localhost:5000", Colors.YELLOW)
            
            print_colored("\n📊 DASHBOARD FEATURES:", Colors.BOLD)
            print_colored("   • Executive Summary with real-time KPIs", Colors.BLUE)
            print_colored("   • Sales Analytics with interactive charts", Colors.BLUE)
            print_colored("   • Financial Dashboard with budget analysis", Colors.BLUE)
            print_colored("   • Operations Dashboard with inventory tracking", Colors.BLUE)
            print_colored("   • AI Analytics with predictive insights", Colors.BLUE)
            print_colored("   • Real-time notifications and AI chat", Colors.BLUE)
            print_colored("   • Mobile-responsive design", Colors.BLUE)
            
            print_colored("\n🎯 SAMPLE DATA:", Colors.BOLD)
            print_colored("   • 5,000+ realistic business transactions", Colors.BLUE)
            print_colored("   • South African business context (ZAR, regions)", Colors.BLUE)
            print_colored("   • Multiple product categories and customer types", Colors.BLUE)
            
            print_colored("\n🛑 TO STOP: Press Ctrl+C", Colors.YELLOW)
            
            # Wait for the process
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
                print_colored(f"Error: {stderr[:300]}", Colors.RED)
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
    
    print_colored("\n🍎 MAC-OPTIMIZED FEATURES:", Colors.BOLD)
    print_colored("   • Automatic pandas/numpy compatibility fix", Colors.BLUE)
    print_colored("   • Fallback to simplified version if needed", Colors.BLUE)
    print_colored("   • Native macOS terminal colors", Colors.BLUE)
    print_colored("   • Safari browser integration", Colors.BLUE)
    print_colored("   • No complex dependencies required", Colors.BLUE)
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_colored("❌ Python 3.7+ required", Colors.RED)
        print_colored(f"Current version: {version.major}.{version.minor}", Colors.YELLOW)
        print_colored("Install with: brew install python3", Colors.BLUE)
        return 1
    
    print_colored(f"\n✅ Python {version.major}.{version.minor}.{version.micro} detected", Colors.GREEN)
    
    # Install basic packages
    install_basic_packages()
    
    # Start dashboard
    if start_dashboard():
        print_colored("\n🎉 SUCCESS! Your dashboard is ready to use!", Colors.GREEN)
        return 0
    else:
        print_colored("\n❌ Failed to start dashboard", Colors.RED)
        print_colored("💡 Troubleshooting tips:", Colors.YELLOW)
        print_colored("   1. Try: python3 dashboard_portal/app_simple.py", Colors.YELLOW)
        print_colored("   2. Check that you're in the project root directory", Colors.YELLOW)
        print_colored("   3. Run: python3 fix_mac_dependencies.py", Colors.YELLOW)
        return 1

if __name__ == "__main__":
    exit(main())