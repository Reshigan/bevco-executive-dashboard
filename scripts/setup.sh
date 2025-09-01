#!/bin/bash

# Bevco Executive Dashboard - Automated Setup Script
# This script sets up the development environment and generates initial data

echo "=================================================="
echo "Bevco Executive Dashboard - Automated Setup"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
        exit 1
    fi
}

# Check if Python is installed
echo "Checking prerequisites..."
python3 --version >/dev/null 2>&1
print_status $? "Python 3 is installed"

# Create virtual environment
echo -e "\n${YELLOW}Setting up Python environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status $? "Created virtual environment"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate
print_status $? "Activated virtual environment"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip >/dev/null 2>&1
pip install pandas numpy openpyxl >/dev/null 2>&1
print_status $? "Installed Python packages"

# Generate master data
echo -e "\n${YELLOW}Generating sample data...${NC}"
python scripts/etl/generate_master_data.py
print_status $? "Generated master data files"

# Create Power BI workspace directories
echo -e "\n${YELLOW}Creating Power BI workspace...${NC}"
mkdir -p powerbi/reports/backups
mkdir -p powerbi/datasets/shared
print_status $? "Created Power BI directories"

# Generate data quality report
echo -e "\n${YELLOW}Running data quality checks...${NC}"
python scripts/etl/data_quality_check.py
print_status $? "Data quality check completed"

# Display summary
echo -e "\n${GREEN}=================================================="
echo "Setup completed successfully!"
echo "=================================================="
echo -e "${NC}"
echo "Next steps:"
echo "1. Open Power BI Desktop"
echo "2. Run: ./scripts/import_to_powerbi.ps1"
echo "3. Follow the deployment guide in /documentation/technical/"
echo ""
echo "Sample data location: /data/master/"
echo "DAX measures: /powerbi/datasets/DAX_Measures.txt"
echo ""
echo -e "${YELLOW}For Windows users, run: scripts\\setup.bat${NC}"