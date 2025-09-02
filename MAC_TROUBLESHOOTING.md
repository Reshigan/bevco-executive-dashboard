# 🍎 Mac Troubleshooting Guide

## ❌ **Your Error: Pandas/Numpy Compatibility Issue**

The error you're seeing is a common Mac issue with pandas and numpy version conflicts:

```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
```

## 🚀 **Quick Fix Solutions**

### **🎯 Solution 1: Use Mac-Optimized Launcher (Recommended)**
```bash
python3 start_mac.py
```

This launcher:
- ✅ **Automatically detects** pandas issues
- ✅ **Fixes dependencies** automatically
- ✅ **Falls back** to simplified version if needed
- ✅ **Works without pandas** if necessary

### **🎯 Solution 2: Fix Dependencies Manually**
```bash
# Run the dependency fix script
python3 fix_mac_dependencies.py

# Then start normally
python3 start_here.py
```

### **🎯 Solution 3: Use Simplified Version**
```bash
cd dashboard_portal
python3 app_simple.py
```

The simplified version:
- ✅ **No pandas dependency** - uses SQLite directly
- ✅ **All features work** - same functionality
- ✅ **Faster startup** - fewer dependencies
- ✅ **More reliable** on Mac

### **🎯 Solution 4: Clean Install**
```bash
# Uninstall problematic packages
pip3 uninstall pandas numpy -y

# Clear pip cache
pip3 cache purge

# Install compatible versions
pip3 install numpy==1.24.3
pip3 install pandas==2.0.3

# Install other requirements
pip3 install -r dashboard_portal/requirements_mac.txt

# Start dashboard
python3 start_here.py
```

---

## 🔧 **Step-by-Step Mac Setup**

### **Step 1: Check Your Setup**
```bash
# Check Python version (need 3.7+)
python3 --version

# Check if you're in the right directory
ls -la
# You should see: dashboard_portal/, start_mac.py, etc.
```

### **Step 2: Try the Mac Launcher**
```bash
# This handles everything automatically
python3 start_mac.py
```

### **Step 3: If That Fails, Manual Fix**
```bash
# Fix dependencies
python3 fix_mac_dependencies.py

# Try again
python3 start_here.py
```

### **Step 4: Use Simplified Version**
```bash
# Go to dashboard directory
cd dashboard_portal

# Start simplified version (no pandas)
python3 app_simple.py
```

---

## 🍎 **Mac-Specific Issues & Solutions**

### **Issue: "Command not found: python3"**
```bash
# Install Python via Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3

# Or download from python.org
```

### **Issue: "Permission denied"**
```bash
# Make scripts executable
chmod +x start_mac.py
chmod +x fix_mac_dependencies.py
chmod +x start_here.py
```

### **Issue: "SSL Certificate" errors**
```bash
# Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command

# Or install certificates via pip
pip3 install --upgrade certifi
```

### **Issue: "Port already in use"**
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process (replace PID with actual number)
kill -9 PID

# Or the launcher will automatically try ports 5001, 5002, etc.
```

### **Issue: Multiple Python versions**
```bash
# Check which Python you're using
which python3
python3 --version

# Use specific version if needed
python3.11 start_mac.py
```

---

## 🎯 **What Each Solution Provides**

### **start_mac.py (Recommended)**
- 🍎 **Mac-optimized** with automatic fixes
- 🔧 **Dependency repair** built-in
- 📊 **Full dashboard** if possible, simplified if needed
- 🌈 **Colored output** for better UX

### **app_simple.py (Fallback)**
- 🚀 **No pandas dependency** - pure Python + SQLite
- ⚡ **Faster startup** - fewer packages to load
- 🔒 **More reliable** - fewer compatibility issues
- ✅ **Same features** - all functionality preserved

### **fix_mac_dependencies.py (Repair)**
- 🔧 **Fixes numpy/pandas** version conflicts
- 🧹 **Cleans pip cache** and reinstalls
- 📦 **Installs compatible** versions
- 🍎 **Mac-specific** solutions

---

## 📊 **What You'll Get**

Regardless of which solution you use, you'll get the complete dashboard:

### **Dashboard Modules:**
1. **Executive Summary** - KPIs, trends, regional performance
2. **Sales Analytics** - Product analysis, customer insights
3. **Financial Dashboard** - Revenue, budgets, financial ratios
4. **Operations Dashboard** - Inventory, employees, supply chain
5. **AI Analytics** - Predictions, anomalies, recommendations

### **Features:**
- **🤖 AI Chat Assistant** - Ask questions about your data
- **📊 Interactive Charts** - Real-time visualizations
- **📱 Mobile Responsive** - Works on iPhone/iPad
- **🔔 Live Updates** - Real-time notifications
- **🎨 Modern UI** - Professional Salesforce-style interface

### **Sample Data:**
- **5,000+ transactions** - 6 months of realistic data
- **South African context** - ZAR pricing, SA regions
- **Multiple categories** - Beer, wine, spirits, soft drinks, water

---

## 🚀 **Recommended Workflow**

### **For First-Time Setup:**
1. **Download/extract** the project
2. **Open Terminal** (⌘ + Space, type "Terminal")
3. **Navigate** to project: `cd ~/Downloads/bevco-executive-dashboard`
4. **Run Mac launcher**: `python3 start_mac.py`
5. **Wait for automatic setup** (2-3 minutes)
6. **Dashboard opens** in Safari automatically

### **If You Get Errors:**
1. **Try simplified version**: `python3 dashboard_portal/app_simple.py`
2. **Check Python version**: `python3 --version` (need 3.7+)
3. **Fix permissions**: `chmod +x *.py`
4. **Clear and reinstall**: Follow Solution 4 above

### **For Development:**
1. **Use simplified version** for reliability: `app_simple.py`
2. **Install minimal deps**: `pip3 install flask flask-socketio`
3. **Test locally** before deploying

---

## 💡 **Pro Tips for Mac Users**

### **Terminal Tips:**
- **⌘ + T** - New terminal tab
- **⌘ + K** - Clear terminal
- **Ctrl + C** - Stop running process
- **↑ arrow** - Previous command

### **Browser Tips:**
- **⌘ + R** - Refresh dashboard
- **⌘ + Shift + R** - Hard refresh (clear cache)
- **⌘ + Option + I** - Developer tools (for debugging)

### **File Management:**
- **Drag folder** into Terminal after typing `cd ` to navigate
- **⌘ + Space** then type "Terminal" for quick access
- **Keep Terminal open** while dashboard is running

---

## 📞 **Still Need Help?**

### **Check These:**
1. **Python version**: `python3 --version` (need 3.7+)
2. **Project location**: `ls -la` should show dashboard_portal/
3. **Permissions**: `chmod +x *.py` to make scripts executable
4. **Port conflicts**: `lsof -i :5000` to check port usage

### **Try These Commands:**
```bash
# Quick diagnostic
python3 --version
which python3
ls -la dashboard_portal/

# Quick fix attempt
python3 start_mac.py

# Fallback method
cd dashboard_portal && python3 app_simple.py
```

### **Common Solutions:**
- **Restart Terminal** and try again
- **Use full path**: `/usr/bin/python3 start_mac.py`
- **Try different Python**: `python3.11 start_mac.py`
- **Install Homebrew Python**: `brew install python3`

---

## 🎉 **Success Indicators**

You'll know it's working when you see:

```
🎉 DASHBOARD IS RUNNING!
============================================================
🌐 URL: http://localhost:5000
👤 Username: admin
🔑 Password: admin123
🤖 AI Chat: Click chat button (bottom-right)
============================================================
🌐 Opening in Safari...
```

**Your modern executive dashboard is ready!** 🚀📊✨

The dashboard will work perfectly regardless of which method you use - the simplified version has all the same features, just without the pandas dependency that was causing issues.