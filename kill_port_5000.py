#!/usr/bin/env python3
"""
Kill any process using port 5000
"""

import subprocess
import sys
import platform

def kill_port_5000():
    """Kill process using port 5000"""
    system = platform.system()
    
    print("🔍 Looking for processes using port 5000...")
    
    try:
        if system == "Darwin":  # macOS
            # Find process using port 5000
            result = subprocess.run(
                ["lsof", "-ti", ":5000"],
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    print(f"🛑 Killing process {pid} using port 5000...")
                    subprocess.run(["kill", "-9", pid])
                print("✅ Port 5000 is now free!")
            else:
                print("✅ Port 5000 is already free!")
                
        elif system == "Linux":
            # Similar for Linux
            result = subprocess.run(
                ["lsof", "-ti", ":5000"],
                capture_output=True,
                text=True
            )
            
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    print(f"🛑 Killing process {pid} using port 5000...")
                    subprocess.run(["kill", "-9", pid])
                print("✅ Port 5000 is now free!")
            else:
                print("✅ Port 5000 is already free!")
                
        elif system == "Windows":
            # Windows command
            result = subprocess.run(
                ["netstat", "-ano", "|", "findstr", ":5000"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    parts = line.split()
                    if len(parts) > 4:
                        pid = parts[-1]
                        print(f"🛑 Killing process {pid} using port 5000...")
                        subprocess.run(["taskkill", "/F", "/PID", pid])
                print("✅ Port 5000 is now free!")
            else:
                print("✅ Port 5000 is already free!")
                
    except Exception as e:
        print(f"⚠️  Could not check/kill port: {e}")
        print("💡 Try manually: lsof -ti :5000 | xargs kill -9")

if __name__ == "__main__":
    kill_port_5000()