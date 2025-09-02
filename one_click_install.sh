#!/bin/bash

# Bevco Executive Dashboard - One Click Install Script
# Complete automated setup for Mac/Linux

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo "================================================================"
    echo -e "${BOLD}  BEVCO EXECUTIVE DASHBOARD - ONE CLICK INSTALL${NC}"
    echo -e "${BLUE}  Complete Business Intelligence Portal${NC}"
    echo "================================================================"
    echo ""
    echo "This will automatically:"
    echo "  1. Check Python installation"
    echo "  2. Install required packages"
    echo "  3. Download project files (if needed)"
    echo "  4. Set up database with sample data"
    echo "  5. Start the dashboard"
    echo "  6. Open in your browser"
    echo ""
    echo -e "${GREEN}Login: admin / admin123${NC}"
    echo -e "${GREEN}URL: http://localhost:5000${NC}"
    echo ""
    echo "================================================================"
    echo ""
}

check_python() {
    echo -e "${BLUE}🐍 Checking Python installation...${NC}"
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        echo -e "${GREEN}✅ python3 found${NC}"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        echo -e "${GREEN}✅ python found${NC}"
    else
        echo -e "${RED}❌ Python not found!${NC}"
        echo ""
        echo "Please install Python 3.7+ first:"
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "  brew install python3"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "  sudo apt update && sudo apt install python3 python3-pip"
        fi
        
        echo "Or download from: https://python.org/downloads"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"
}

install_packages() {
    echo -e "${BLUE}📦 Installing required packages...${NC}"
    
    # Upgrade pip first
    $PYTHON_CMD -m pip install --upgrade pip --quiet 2>/dev/null || true
    
    # Install packages
    packages=(
        "flask==2.3.3"
        "flask-socketio==5.3.6"
        "pandas==2.1.1"
        "werkzeug==2.3.7"
        "python-socketio==5.8.0"
        "eventlet==0.33.3"
        "python-dotenv==1.0.0"
    )
    
    for package in "${packages[@]}"; do
        echo -e "${BLUE}   Installing ${package%==*}...${NC}"
        if $PYTHON_CMD -m pip install "$package" --quiet; then
            echo -e "${GREEN}   ✅ ${package%==*}${NC}"
        else
            echo -e "${YELLOW}   ⚠️  ${package%==*} (may already be installed)${NC}"
        fi
    done
    
    echo -e "${GREEN}✅ Package installation completed${NC}"
}

download_project() {
    echo -e "${BLUE}📥 Checking project files...${NC}"
    
    if [[ -d "dashboard_portal" && -f "dashboard_portal/app.py" ]]; then
        echo -e "${GREEN}✅ Project files found locally${NC}"
        return 0
    fi
    
    echo -e "${BLUE}📥 Downloading project from GitHub...${NC}"
    
    if command -v curl &> /dev/null; then
        curl -L "https://github.com/Reshigan/bevco-executive-dashboard/archive/refs/heads/main.zip" -o project.zip
    elif command -v wget &> /dev/null; then
        wget "https://github.com/Reshigan/bevco-executive-dashboard/archive/refs/heads/main.zip" -O project.zip
    else
        echo -e "${RED}❌ Neither curl nor wget found. Cannot download project.${NC}"
        echo "Please manually download from: https://github.com/Reshigan/bevco-executive-dashboard"
        exit 1
    fi
    
    if [[ -f "project.zip" ]]; then
        echo -e "${BLUE}📦 Extracting project files...${NC}"
        unzip -q project.zip
        
        if [[ -d "bevco-executive-dashboard-main" ]]; then
            # Move files from extracted directory to current directory
            mv bevco-executive-dashboard-main/* ./ 2>/dev/null || true
            mv bevco-executive-dashboard-main/.* ./ 2>/dev/null || true
            rmdir bevco-executive-dashboard-main 2>/dev/null || true
        fi
        
        rm project.zip
        echo -e "${GREEN}✅ Project downloaded successfully${NC}"
    else
        echo -e "${RED}❌ Failed to download project${NC}"
        exit 1
    fi
}

start_dashboard() {
    echo -e "${BLUE}🚀 Starting dashboard server...${NC}"
    
    if [[ ! -f "dashboard_portal/app.py" ]]; then
        echo -e "${RED}❌ Dashboard app.py not found!${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}   Starting Flask server...${NC}"
    echo -e "${YELLOW}   This may take 10-15 seconds for first-time setup...${NC}"
    
    cd dashboard_portal
    
    # Start the dashboard in background to check if it starts successfully
    $PYTHON_CMD app.py &
    DASHBOARD_PID=$!
    
    # Wait for server to start
    sleep 8
    
    # Check if process is still running
    if kill -0 $DASHBOARD_PID 2>/dev/null; then
        echo ""
        echo "================================================================"
        echo -e "${GREEN}🎉 DASHBOARD IS RUNNING SUCCESSFULLY!${NC}"
        echo "================================================================"
        echo -e "${BOLD}🌐 URL: http://localhost:5000${NC}"
        echo -e "${BLUE}👤 Username: admin${NC}"
        echo -e "${BLUE}🔑 Password: admin123${NC}"
        echo -e "${BLUE}🤖 AI Chat: Click chat button (bottom-right)${NC}"
        echo "================================================================"
        
        # Try to open browser
        if command -v open &> /dev/null; then
            open "http://localhost:5000"
            echo -e "${GREEN}🌐 Opening dashboard in your browser...${NC}"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "http://localhost:5000"
            echo -e "${GREEN}🌐 Opening dashboard in your browser...${NC}"
        else
            echo -e "${YELLOW}📱 Please manually open: http://localhost:5000${NC}"
        fi
        
        echo ""
        echo -e "${BOLD}📊 DASHBOARD FEATURES:${NC}"
        echo -e "${BLUE}   • Executive Summary with real-time KPIs${NC}"
        echo -e "${BLUE}   • Sales Analytics with interactive charts${NC}"
        echo -e "${BLUE}   • Financial Dashboard with budget analysis${NC}"
        echo -e "${BLUE}   • Operations Dashboard with inventory tracking${NC}"
        echo -e "${BLUE}   • AI Analytics with predictive insights${NC}"
        echo -e "${BLUE}   • Real-time notifications and updates${NC}"
        echo -e "${BLUE}   • Mobile-responsive design${NC}"
        
        echo ""
        echo -e "${BOLD}🎯 SAMPLE DATA INCLUDED:${NC}"
        echo -e "${BLUE}   • 5,000+ realistic business transactions${NC}"
        echo -e "${BLUE}   • South African business context (ZAR, regions)${NC}"
        echo -e "${BLUE}   • Multiple product categories and customer types${NC}"
        
        echo ""
        echo -e "${YELLOW}🛑 TO STOP: Press Ctrl+C${NC}"
        echo -e "${BLUE}📖 HELP: See DASHBOARD_README.md for full documentation${NC}"
        
        # Wait for the dashboard process
        wait $DASHBOARD_PID
        
    else
        echo -e "${RED}❌ Dashboard failed to start${NC}"
        echo "💡 Try running manually:"
        echo "   cd dashboard_portal"
        echo "   $PYTHON_CMD app.py"
        exit 1
    fi
}

# Main execution
main() {
    print_header
    
    echo -e "${BOLD}🎯 AUTOMATED SETUP STARTING...${NC}"
    echo ""
    
    # Step 1: Check Python
    check_python
    
    # Step 2: Install packages
    install_packages
    
    # Step 3: Download project if needed
    download_project
    
    # Step 4: Start dashboard
    start_dashboard
    
    echo ""
    echo -e "${GREEN}🎉 AUTOMATED SETUP COMPLETED SUCCESSFULLY!${NC}"
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n${YELLOW}🛑 Setup cancelled by user${NC}"; exit 0' INT

# Run main function
main