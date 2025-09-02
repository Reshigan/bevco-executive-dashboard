#!/usr/bin/env python3
"""
Mac Dependency Fix for Bevco Dashboard
Fixes pandas/numpy compatibility issues on macOS
"""

import subprocess
import sys
import os

def print_status(message, status="info"):
    colors = {
        "info": "\033[96m",
        "success": "\033[92m", 
        "warning": "\033[93m",
        "error": "\033[91m",
        "reset": "\033[0m"
    }
    
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    print(f"{colors.get(status, '')}{icons.get(status, '')} {message}{colors['reset']}")

def fix_mac_dependencies():
    """Fix Mac-specific dependency issues"""
    print_status("🍎 Fixing Mac dependency issues...", "info")
    
    commands = [
        # Uninstall problematic packages
        [sys.executable, "-m", "pip", "uninstall", "pandas", "numpy", "-y"],
        
        # Clear pip cache
        [sys.executable, "-m", "pip", "cache", "purge"],
        
        # Reinstall with specific versions that work on Mac
        [sys.executable, "-m", "pip", "install", "numpy==1.24.3"],
        [sys.executable, "-m", "pip", "install", "pandas==2.0.3"],
        
        # Reinstall other packages
        [sys.executable, "-m", "pip", "install", "flask==2.3.3"],
        [sys.executable, "-m", "pip", "install", "flask-socketio==5.3.6"],
        [sys.executable, "-m", "pip", "install", "werkzeug==2.3.7"],
        [sys.executable, "-m", "pip", "install", "python-socketio==5.8.0"],
        [sys.executable, "-m", "pip", "install", "eventlet==0.33.3"],
    ]
    
    for cmd in commands:
        try:
            print_status(f"Running: {' '.join(cmd[3:])}", "info")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print_status(f"✅ Success", "success")
            else:
                print_status(f"⚠️ Warning: {result.stderr[:100]}", "warning")
        except Exception as e:
            print_status(f"⚠️ Skipped: {e}", "warning")
    
    print_status("🍎 Mac dependency fix completed!", "success")

if __name__ == "__main__":
    fix_mac_dependencies()