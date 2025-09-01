#!/bin/bash

# Bevco Dashboard - Mac Launcher
# One-click solution for Mac users

echo "🍎 Bevco Dashboard - Mac Launcher"
echo "================================="
echo

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  This launcher is optimized for macOS"
    echo "   For other systems, use: ./scripts/run_automation.sh"
    echo
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    echo "💡 Install Python 3 from:"
    echo "   • Homebrew: brew install python3"
    echo "   • Official: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo

# Show options
echo "Choose your preferred method:"
echo
echo "1. 🌐 Web Import Tool (Recommended)"
echo "   • Mac-optimized web interface"
echo "   • Generate data in browser"
echo "   • Drag & drop file conversion"
echo "   • Step-by-step upload guide"
echo
echo "2. 🤖 Automated Scripts"
echo "   • Terminal-based automation"
echo "   • Multiple automation options"
echo "   • Template file generation"
echo
echo "3. 📖 Manual Setup"
echo "   • Detailed documentation"
echo "   • Step-by-step guides"
echo "   • Troubleshooting help"
echo

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo
        echo "🌐 Starting Mac Web Import Tool..."
        echo "This will:"
        echo "• Start a local web server"
        echo "• Open your browser automatically"
        echo "• Provide a Mac-optimized interface"
        echo "• Guide you through the entire process"
        echo
        read -p "Press Enter to continue..."
        
        # Start the web server
        python3 scripts/mac_web_server.py
        ;;
    2)
        echo
        echo "🤖 Starting Automation Menu..."
        echo
        ./scripts/run_automation.sh
        ;;
    3)
        echo
        echo "📖 Opening Documentation..."
        echo
        echo "Available guides:"
        echo "• MAC_SETUP_GUIDE.md - Complete Mac setup guide"
        echo "• ONLINE_POWERBI_SETUP.md - Online Power BI setup"
        echo "• QUICK_POWERBI_SETUP.md - 15-minute quick start"
        echo "• AUTHENTICATION_SOLUTIONS.md - Auth troubleshooting"
        echo
        echo "GitHub Repository: https://github.com/Reshigan/bevco-executive-dashboard"
        
        # Try to open documentation
        if command -v open &> /dev/null; then
            echo "Opening Mac setup guide..."
            open MAC_SETUP_GUIDE.md
            echo "Opening GitHub repository..."
            open "https://github.com/Reshigan/bevco-executive-dashboard"
        else
            echo "Please manually open MAC_SETUP_GUIDE.md and visit the GitHub repository"
        fi
        ;;
    *)
        echo "Invalid choice. Please run the script again and choose 1, 2, or 3."
        exit 1
        ;;
esac

echo
echo "🍎 Thanks for using Bevco Dashboard!"
echo "For support, visit: https://github.com/Reshigan/bevco-executive-dashboard"