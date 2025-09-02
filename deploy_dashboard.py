#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Local Deployment Script
Deploy the complete modern dashboard system locally with all functionality
"""

import os
import sys
import subprocess
import platform
import time
import webbrowser
from pathlib import Path

def print_status(message, status="info"):
    """Print colored status messages"""
    colors = {
        "info": "\033[96m",      # Cyan
        "success": "\033[92m",   # Green
        "warning": "\033[93m",   # Yellow
        "error": "\033[91m",     # Red
        "reset": "\033[0m"       # Reset
    }
    
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    print(f"{colors.get(status, '')}{icons.get(status, '')} {message}{colors['reset']}")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_status("Python 3.8 or higher is required", "error")
        return False
    
    print_status(f"Python {version.major}.{version.minor}.{version.micro} detected", "success")
    return True

def install_requirements():
    """Install required Python packages"""
    print_status("Installing required packages...", "info")
    
    requirements_path = Path("dashboard_portal/requirements.txt")
    if not requirements_path.exists():
        print_status("Requirements file not found", "error")
        return False
    
    try:
        # Install packages
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print_status(f"Package installation failed: {result.stderr}", "error")
            return False
        
        print_status("All packages installed successfully", "success")
        return True
        
    except Exception as e:
        print_status(f"Error installing packages: {e}", "error")
        return False

def setup_environment():
    """Set up environment variables and configuration"""
    print_status("Setting up environment...", "info")
    
    # Create .env file if it doesn't exist
    env_path = Path("dashboard_portal/.env")
    if not env_path.exists():
        env_content = """# Bevco Dashboard Environment Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here

# Database Configuration
DATABASE_URL=sqlite:///data/bevco_dashboard.db

# Server Configuration
HOST=0.0.0.0
PORT=5000
"""
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print_status("Environment file created", "success")
    
    return True

def check_port_availability(port=5000):
    """Check if the port is available"""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def start_dashboard():
    """Start the dashboard application"""
    print_status("Starting Bevco Executive Dashboard...", "info")
    
    # Change to dashboard directory
    dashboard_dir = Path("dashboard_portal")
    if not dashboard_dir.exists():
        print_status("Dashboard directory not found", "error")
        return False
    
    # Check if port is available
    if not check_port_availability(5000):
        print_status("Port 5000 is already in use. Please close other applications using this port.", "warning")
        
        # Try alternative ports
        for port in [5001, 5002, 5003, 8000, 8080]:
            if check_port_availability(port):
                print_status(f"Using alternative port {port}", "info")
                os.environ['PORT'] = str(port)
                break
        else:
            print_status("No available ports found", "error")
            return False
    
    try:
        # Start the Flask application
        app_path = dashboard_dir / "app.py"
        
        print_status("Dashboard is starting up...", "info")
        print_status("This may take a few moments to initialize the database and load sample data", "info")
        
        # Start the application
        process = subprocess.Popen([
            sys.executable, str(app_path)
        ], cwd=str(dashboard_dir))
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            port = os.environ.get('PORT', '5000')
            url = f"http://localhost:{port}"
            
            print_status("Dashboard started successfully!", "success")
            print_status(f"Dashboard URL: {url}", "info")
            print_status("Default Login: admin / admin123", "info")
            
            # Open browser
            try:
                webbrowser.open(url)
                print_status("Opening dashboard in your default browser...", "info")
            except:
                print_status("Please manually open the URL in your browser", "warning")
            
            return True
        else:
            print_status("Dashboard failed to start", "error")
            return False
            
    except Exception as e:
        print_status(f"Error starting dashboard: {e}", "error")
        return False

def show_dashboard_info():
    """Show information about the dashboard"""
    print("\n" + "="*60)
    print("🚀 BEVCO EXECUTIVE DASHBOARD - LOCAL DEPLOYMENT")
    print("="*60)
    print()
    print("📊 DASHBOARD FEATURES:")
    print("   • Executive Summary with real-time KPIs")
    print("   • Sales Analytics with interactive charts")
    print("   • Financial Dashboard with budget analysis")
    print("   • Operations Dashboard with inventory tracking")
    print("   • AI Analytics with predictive insights")
    print("   • Real-time notifications and alerts")
    print("   • AI-powered chat assistant")
    print("   • Mobile-responsive design")
    print()
    print("🎯 SAMPLE DATA INCLUDED:")
    print("   • 5,000 realistic sales transactions")
    print("   • South African business context")
    print("   • Multiple regions, products, and customers")
    print("   • Financial and operational metrics")
    print()
    print("🔐 DEFAULT LOGIN CREDENTIALS:")
    print("   • Username: admin")
    print("   • Password: admin123")
    print()
    print("🤖 AI CHAT ASSISTANT:")
    print("   • Click the chat button in the bottom-right corner")
    print("   • Ask questions about your business data")
    print("   • Get insights and recommendations")
    print()

def main():
    """Main deployment function"""
    show_dashboard_info()
    
    print("🚀 STARTING DEPLOYMENT...")
    print("-" * 40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Setup environment
    if not setup_environment():
        return 1
    
    # Start dashboard
    if not start_dashboard():
        return 1
    
    print()
    print("="*60)
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print("="*60)
    print()
    print("Your Bevco Executive Dashboard is now running locally!")
    print()
    print("📱 NEXT STEPS:")
    print("1. The dashboard should open automatically in your browser")
    print("2. Login with: admin / admin123")
    print("3. Explore the different dashboard sections")
    print("4. Try the AI chat assistant")
    print("5. View real-time updates and notifications")
    print()
    print("🛑 TO STOP THE DASHBOARD:")
    print("   Press Ctrl+C in this terminal window")
    print()
    print("📞 SUPPORT:")
    print("   If you encounter any issues, check the terminal output")
    print("   for error messages and troubleshooting information.")
    print()
    
    try:
        print("Dashboard is running... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print_status("\nShutting down dashboard...", "info")
        print_status("Dashboard stopped successfully", "success")
        return 0

if __name__ == "__main__":
    exit(main())