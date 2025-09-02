#!/bin/bash
# Bevco Dashboard - Quick Start from GitHub
# One-line installer that downloads and runs the dashboard

set -e

echo "🚀 Bevco Executive Dashboard - Quick Start"
echo "=========================================="
echo ""

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "📥 Downloading dashboard from GitHub..."
curl -L https://github.com/Reshigan/bevco-executive-dashboard/archive/refs/heads/main.zip -o dashboard.zip

echo "📦 Extracting files..."
unzip -q dashboard.zip

echo "📁 Setting up dashboard..."
cd bevco-executive-dashboard-main

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found! Please install Python 3.7+"
    exit 1
fi

echo "✅ Using $PYTHON_CMD"

# Run the appropriate launcher based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🍎 Detected macOS - using Mac-optimized launcher"
    $PYTHON_CMD start_mac.py
else
    # Linux or other
    echo "🐧 Using universal launcher"
    $PYTHON_CMD auto_setup.py
fi