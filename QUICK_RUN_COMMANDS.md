# 🚀 Quick Run Commands - One-Liners

Run the Bevco Executive Dashboard directly from GitHub with a single command!

## 🎯 **Copy & Paste Commands**

### **🐍 Python (All Platforms)**
```bash
curl -s https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/run_from_github.py | python3
```

### **🍎 Mac/Linux (Shell)**
```bash
curl -s https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/quick_start.sh | bash
```

### **🪟 Windows (PowerShell)**
```powershell
iwr -useb https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/run_from_github.py | python
```

### **📥 Download & Run (Alternative)**
```bash
# Mac/Linux
wget -qO- https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/run_from_github.py | python3

# Or with curl
curl -L https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/run_from_github.py | python3
```

---

## 🎯 **What These Commands Do**

1. **Download** the latest dashboard from GitHub
2. **Install** all required dependencies automatically
3. **Set up** the database with 5,000+ sample transactions
4. **Start** the web server on http://localhost:5000
5. **Open** your browser automatically
6. **Provide** login credentials (admin/admin123)

---

## 🍎 **Mac Users - Special Command**

If you're on Mac and having pandas/numpy issues:

```bash
# This uses the Mac-optimized version
curl -s https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/start_mac.py > start_mac.py && python3 start_mac.py
```

---

## 🚀 **Step-by-Step Instructions**

### **Option 1: Direct Run (Recommended)**

1. **Open Terminal** (Mac/Linux) or **Command Prompt** (Windows)
2. **Copy and paste** one of the commands above
3. **Press Enter** and wait 2-3 minutes
4. **Dashboard opens** automatically in your browser
5. **Login** with admin/admin123

### **Option 2: Download First**

```bash
# Download the project
git clone https://github.com/Reshigan/bevco-executive-dashboard.git
cd bevco-executive-dashboard

# Run the appropriate launcher
python3 auto_setup.py          # Universal
python3 start_mac.py           # Mac-optimized
python3 start_here.py          # Simple launcher
./one_click_install.sh         # Shell script
```

### **Option 3: Manual Download**

1. Go to https://github.com/Reshigan/bevco-executive-dashboard
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open Terminal in that folder
5. Run: `python3 auto_setup.py`

---

## 📊 **What You Get**

### **Complete Dashboard System:**
- ✅ **5 Dashboard Modules** (Executive, Sales, Finance, Operations, AI)
- ✅ **AI Chat Assistant** for business insights
- ✅ **Real-time Updates** via WebSockets
- ✅ **Interactive Charts** with Chart.js
- ✅ **Mobile Responsive** design
- ✅ **5,000+ Sample Transactions**
- ✅ **Professional UI** (Salesforce-style)

### **Login Credentials:**
- **URL**: http://localhost:5000
- **Username**: `admin`
- **Password**: `admin123`

---

## 🛠 **Troubleshooting**

### **"Python not found"**
Install Python 3.7+ from https://python.org/downloads

### **"curl: command not found" (Windows)**
Use PowerShell instead of Command Prompt, or install Git Bash

### **Mac pandas/numpy error**
Use the Mac-specific command above

### **"Permission denied"**
```bash
# Add execute permission
chmod +x quick_start.sh
./quick_start.sh
```

### **Port 5000 in use**
The scripts automatically try ports 5001, 5002, etc.

---

## 🎯 **Even Simpler: Browser Bookmarks**

Save these as bookmarks for instant access:

### **Run Dashboard (Python)**
```
javascript:(function(){fetch('https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/run_from_github.py').then(r=>r.text()).then(s=>{const b=new Blob([s],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='run_dashboard.py';a.click();alert('Downloaded! Run with: python3 run_dashboard.py');});})();
```

### **Quick Instructions**
```
javascript:(function(){window.open('https://github.com/Reshigan/bevco-executive-dashboard#quick-start','_blank');})();
```

---

## 🚀 **Fastest Method by Platform**

### **🍎 macOS**
```bash
curl -s https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/start_mac.py | python3
```

### **🐧 Linux**
```bash
curl -s https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/run_from_github.py | python3
```

### **🪟 Windows**
```powershell
iwr -useb https://raw.githubusercontent.com/Reshigan/bevco-executive-dashboard/main/run_from_github.py | python
```

---

## 📱 **Mobile Access**

Once running, access from your phone/tablet:

1. Find your computer's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. On your mobile device, go to: `http://YOUR_IP:5000`
3. Login with admin/admin123

---

## 🎉 **That's It!**

With just one command, you get a complete executive dashboard with:
- Real-time business intelligence
- AI-powered insights
- Professional visualizations
- Mobile-responsive design
- 5,000+ sample transactions

**Copy any command above and paste it in your terminal to start!** 🚀📊✨