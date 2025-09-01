#!/bin/bash

# Bevco Executive Dashboard - Automation Launcher for Mac/Linux

echo "========================================"
echo "Bevco Dashboard - Automation Launcher"
echo "========================================"
echo

echo "Choose your automation method:"
echo "1. Python Automation (Recommended)"
echo "2. Manual Setup Guide"
echo "3. Web-based Tools"
echo

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo
        echo "Starting Python automation..."
        echo "This will:"
        echo "- Generate sample data"
        echo "- Connect to Power BI Service"
        echo "- Create workspace and datasets"
        echo "- Build dashboards automatically"
        echo
        read -p "Press Enter to continue..."
        
        # Check if Python is installed
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
            exit 1
        fi
        
        # Install required packages
        echo "📦 Installing required packages..."
        pip3 install requests pandas openpyxl
        
        # Run automation
        python3 scripts/powerbi_automation.py
        ;;
    2)
        echo
        echo "Opening manual setup guides..."
        echo
        echo "Available guides:"
        echo "- ONLINE_POWERBI_SETUP.md (for app.powerbi.com)"
        echo "- QUICK_POWERBI_SETUP.md (15-minute setup)"
        echo "- POWERBI_IMPLEMENTATION_GUIDE.md (complete guide)"
        echo "- AUTOMATION_GUIDE.md (this automation guide)"
        echo
        echo "GitHub Repository: https://github.com/Reshigan/bevco-executive-dashboard"
        
        # Try to open browser
        if command -v open &> /dev/null; then
            open "https://github.com/Reshigan/bevco-executive-dashboard"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "https://github.com/Reshigan/bevco-executive-dashboard"
        else
            echo "Please manually open: https://github.com/Reshigan/bevco-executive-dashboard"
        fi
        ;;
    3)
        echo
        echo "Starting web-based tools server..."
        echo "This will open interactive tools in your browser."
        echo
        read -p "Press Enter to continue..."
        
        # Check if Python is installed
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
            exit 1
        fi
        
        # Start web server
        python3 scripts/serve_web_tools.py
        ;;
    *)
        echo "Invalid choice. Please run the script again and choose 1, 2, or 3."
        exit 1
        ;;
esac

echo
echo "Press Enter to exit..."
read