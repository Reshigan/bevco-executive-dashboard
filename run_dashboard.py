#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Simple Launcher
Direct launcher that can be run from anywhere
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def find_project_root():
    """Find the project root directory"""
    current = Path.cwd()
    
    # Check if we're already in the right place
    if (current / "dashboard_portal" / "app.py").exists():
        return current
    
    # Check if we're in the dashboard_portal directory
    if (current / "app.py").exists() and current.name == "dashboard_portal":
        return current.parent
    
    # Look for the project in common locations
    possible_locations = [
        current / "bevco-executive-dashboard",
        current.parent / "bevco-executive-dashboard", 
        Path.home() / "bevco-executive-dashboard",
        Path.home() / "Downloads" / "bevco-executive-dashboard",
        Path.home() / "Desktop" / "bevco-executive-dashboard"
    ]
    
    for location in possible_locations:
        if (location / "dashboard_portal" / "app.py").exists():
            return location
    
    return None

def main():
    print("🚀 Bevco Executive Dashboard Launcher")
    print("=" * 45)
    
    # Find project root
    project_root = find_project_root()
    if not project_root:
        print("❌ Could not find the dashboard project.")
        print("\nPlease ensure you have the complete project structure:")
        print("  bevco-executive-dashboard/")
        print("  ├── dashboard_portal/")
        print("  │   ├── app.py")
        print("  │   ├── requirements.txt")
        print("  │   └── templates/")
        print("  └── run_dashboard.py")
        print("\nTry running this script from the project root directory.")
        return 1
    
    print(f"✅ Found project at: {project_root}")
    
    # Change to project directory
    os.chdir(project_root)
    dashboard_dir = project_root / "dashboard_portal"
    
    print("📦 Installing dependencies...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", 
            str(dashboard_dir / "requirements.txt")
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"⚠️  Warning: Some packages may not have installed: {result.stderr}")
        else:
            print("✅ Dependencies installed successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not install dependencies: {e}")
    
    print("🚀 Starting dashboard...")
    
    # Start the dashboard
    try:
        # Change to dashboard directory and start app
        os.chdir(dashboard_dir)
        
        print("📊 Dashboard is starting...")
        print("🌐 URL: http://localhost:5000")
        print("👤 Login: admin / admin123")
        print("🤖 AI Chat: Click the chat button in bottom-right")
        print("\n⏳ Please wait while the server starts...")
        
        # Start the Flask app
        process = subprocess.Popen([sys.executable, "app.py"])
        
        # Wait a moment then open browser
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:5000")
            print("🌐 Opening dashboard in your browser...")
        except:
            print("📱 Please manually open: http://localhost:5000")
        
        print("\n" + "="*50)
        print("🎉 DASHBOARD IS RUNNING!")
        print("="*50)
        print("📊 Access your dashboard at: http://localhost:5000")
        print("👤 Username: admin")
        print("🔑 Password: admin123")
        print("\n🛑 To stop the dashboard: Press Ctrl+C")
        print("="*50)
        
        # Wait for the process
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping dashboard...")
            process.terminate()
            print("✅ Dashboard stopped successfully")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return 1

if __name__ == "__main__":
    exit(main())