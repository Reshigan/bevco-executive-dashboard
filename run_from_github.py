#!/usr/bin/env python3
"""
Bevco Dashboard - Run Directly from GitHub
Downloads and runs the dashboard with one command
"""

import os
import sys
import urllib.request
import zipfile
import tempfile
import shutil
import subprocess
import platform

def download_and_run():
    print("🚀 Bevco Executive Dashboard - Direct from GitHub")
    print("=" * 50)
    print()
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Working directory: {temp_dir}")
    
    try:
        # Download from GitHub
        print("📥 Downloading dashboard from GitHub...")
        zip_url = "https://github.com/Reshigan/bevco-executive-dashboard/archive/refs/heads/main.zip"
        zip_path = os.path.join(temp_dir, "dashboard.zip")
        
        urllib.request.urlretrieve(zip_url, zip_path)
        print("✅ Download complete")
        
        # Extract files
        print("📦 Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        print("✅ Extraction complete")
        
        # Navigate to extracted directory
        project_dir = os.path.join(temp_dir, "bevco-executive-dashboard-main")
        os.chdir(project_dir)
        
        # Determine which launcher to use
        if platform.system() == "Darwin":  # macOS
            print("🍎 Detected macOS - using Mac-optimized launcher")
            launcher = "start_mac.py"
        else:
            print("🐧 Using universal launcher")
            launcher = "auto_setup.py"
        
        # Ensure templates exist
        if not os.path.exists("dashboard_portal/templates"):
            print("📝 Creating template files...")
            try:
                subprocess.run([sys.executable, "create_templates.py"], check=True, capture_output=True)
                print("✅ Templates created!")
            except:
                print("⚠️  Templates will be created by launcher")
        
        # Run the launcher
        print(f"🚀 Starting dashboard with {launcher}...")
        print("=" * 50)
        
        subprocess.run([sys.executable, launcher])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        # Cleanup is handled by system on exit
        pass
    
    return 0

if __name__ == "__main__":
    exit(download_and_run())