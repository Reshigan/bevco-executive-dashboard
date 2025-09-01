# 🍎 Bevco Dashboard - Mac Setup Guide

## 🚀 Complete Mac-to-Power BI Import Solution

This guide provides a **web-based import mechanism** specifically optimized for Mac users to upload data directly to your Power BI tenant at app.powerbi.com.

## 🎯 What You'll Get

✅ **Web-based data generator** - Create 36,400+ sample transactions  
✅ **CSV to Excel converter** - Drag & drop file conversion  
✅ **Power BI upload guide** - Step-by-step instructions  
✅ **Mac-optimized interface** - Native macOS design and shortcuts  
✅ **No authentication issues** - Bypasses all API problems  
✅ **Works in any browser** - Safari, Chrome, Firefox, Edge  

## 🌐 Method 1: Web Import Tool (Recommended)

### Quick Start
```bash
# 1. Download the project
git clone https://github.com/Reshigan/bevco-executive-dashboard.git
cd bevco-executive-dashboard

# 2. Start the Mac web server
python3 scripts/mac_web_server.py
```

**What happens:**
- Web server starts on http://localhost:8080
- Browser opens automatically
- Mac-optimized interface loads
- Ready to generate data and upload to Power BI

### Features Available

#### 📊 Data Generator Tab
- **Generate Sample Data**: Creates realistic South African business data
- **36,400+ Transactions**: 6 months of sales data
- **8 Data Files**: Complete star schema model
- **Download Options**: Individual CSV files or combined Excel workbook

#### 🔄 File Converter Tab
- **Drag & Drop**: Drop CSV files directly from Finder
- **Multi-file Selection**: Use ⌘+Click to select multiple files
- **Excel Output**: Single workbook ready for Power BI
- **Progress Tracking**: Visual conversion progress

#### ☁️ Upload Guide Tab
- **Step-by-step Instructions**: Detailed Power BI upload process
- **Direct Links**: One-click access to app.powerbi.com
- **Mac Tips**: Browser compatibility and file handling
- **Troubleshooting**: Common issues and solutions

## 🖥️ Method 2: Terminal-Based Automation

### Python Automation
```bash
# Install dependencies
pip3 install requests pandas openpyxl selenium webdriver-manager

# Run template creator (no authentication needed)
python3 scripts/powerbi_template_creator.py

# Or run web automation (guided browser process)
python3 scripts/powerbi_web_automation.py
```

### Shell Script Launcher
```bash
# Make executable and run
chmod +x scripts/run_automation.sh
./scripts/run_automation.sh
```

**Options available:**
1. **Power BI Template Creator** (No auth issues)
2. **Web Browser Automation** (Guided process)
3. **Python API Automation** (May have auth issues)
4. **Manual Setup Guide**
5. **Web-based Tools**

## 📋 Step-by-Step Process

### Step 1: Generate Data
1. **Start Web Server**: `python3 scripts/mac_web_server.py`
2. **Open Browser**: Goes to http://localhost:8080 automatically
3. **Generate Data**: Click "Generate Sample Data" button
4. **Download Files**: Get CSV files or Excel workbook

### Step 2: Upload to Power BI
1. **Open Power BI**: Click "Open Power BI Service" button
2. **Sign In**: Use your organizational Microsoft account
3. **Create Workspace**: 
   - Click "Workspaces" in left navigation
   - Click "Create a workspace"
   - Name: "Bevco Executive Dashboard"
4. **Upload Files**:
   - Click "New" → "Upload a file" → "Local File"
   - Select your Excel file or CSV files
   - Wait for upload to complete

### Step 3: Create Dashboard
1. **Create Report**: Click on uploaded dataset → "Create report"
2. **Add Visualizations**:
   - **KPI Cards**: Drag NetSales, GrossProfit to card visuals
   - **Line Chart**: Date on axis, NetSales on values
   - **Map**: Region on location, NetSales on size
   - **Bar Chart**: Category on axis, NetSales on values
3. **Save Report**: Click "Save" and name your report
4. **Create Dashboard**: Pin visuals to new dashboard

## 🍎 Mac-Specific Features

### Browser Optimization
- **Safari**: Best performance and integration
- **Chrome**: Full feature support
- **Firefox**: Good compatibility
- **Edge**: Microsoft-optimized for Power BI

### File Handling
- **Downloads**: Files save to `~/Downloads` by default
- **Drag & Drop**: Works directly from Finder
- **Multi-select**: Use `⌘ + Click` for multiple files
- **Quick Look**: Press Space to preview files

### Keyboard Shortcuts
- **Copy**: `⌘ + C`
- **Paste**: `⌘ + V`
- **Select All**: `⌘ + A`
- **New Tab**: `⌘ + T`
- **Refresh**: `⌘ + R`

## 🔧 Troubleshooting

### "Port already in use"
The web server automatically tries alternative ports (8081, 8082, 8083, 3000, 5000).

### "Python not found"
macOS 10.15+ includes Python 3. If missing:
```bash
# Install via Homebrew
brew install python3

# Or download from python.org
```

### "Permission denied"
```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### "Browser won't open"
Manually navigate to the URL shown in terminal (usually http://localhost:8080).

### "Files won't download"
- Check Safari → Preferences → General → File download location
- Try right-click → "Download Linked File"

### "Power BI upload fails"
- Verify you have Power BI Pro/Premium license
- Check file size (Excel files should be < 1GB)
- Try uploading CSV files individually

## 📊 Sample Data Details

### What's Generated
- **36,400 sales transactions** (Jan-Jun 2024)
- **724 customers** across 9 South African regions
- **339 products** from 5 major beverage vendors
- **319 employees** across 6 departments
- **Complete business model** with relationships

### File Structure
```
data/master/
├── dim_date.csv          # 1,461 rows (4 years)
├── dim_product.csv       # 339 rows
├── dim_customer.csv      # 724 rows
├── dim_employee.csv      # 319 rows
├── fact_sales.csv        # 36,400 rows
├── fact_budget.csv       # 72 rows
├── fact_inventory.csv    # 339 rows
└── dim_kpi_targets.csv   # 6 rows
```

### Business Context
- **South African regions**: Gauteng, Western Cape, KwaZulu-Natal, etc.
- **Beverage categories**: Beer, Wine, Spirits, Soft Drinks, Water
- **Major vendors**: SAB Miller, Distell, Coca-Cola, Pepsi, Local Brands
- **Realistic pricing**: ZAR currency with market-appropriate prices
- **Business relationships**: Proper star schema with fact and dimension tables

## 🎨 Dashboard Examples

### Executive Summary
- **Total Sales**: R 45.2M (vs R 42M target)
- **Gross Margin**: 34.5% (vs 35% target)
- **Top Region**: Gauteng (R 12.8M)
- **Growth Rate**: +8.2% YoY

### Regional Performance
- **Gauteng**: R 12.8M (28.4%)
- **Western Cape**: R 9.6M (21.3%)
- **KwaZulu-Natal**: R 7.2M (15.9%)
- **Other Regions**: R 15.6M (34.4%)

### Product Mix
- **Beer**: R 18.1M (40.0%)
- **Soft Drinks**: R 11.3M (25.0%)
- **Wine**: R 9.0M (20.0%)
- **Spirits**: R 4.5M (10.0%)
- **Water**: R 2.3M (5.0%)

## 🚀 Advanced Features

### Custom Branding
- Replace logos and colors in Power BI
- Use Bevco brand colors: #003366 (primary), #FF6B35 (accent)
- Add company-specific KPIs and targets

### Data Refresh
- Set up scheduled refresh in Power BI Service
- Configure data gateway for live connections
- Enable incremental refresh for large datasets

### Sharing & Collaboration
- Create Power BI Apps for distribution
- Set up row-level security for different user groups
- Configure email subscriptions and alerts

### Mobile Access
- Download Power BI mobile app from App Store
- Dashboards automatically optimize for iPhone/iPad
- Enable push notifications for KPI alerts

## 📞 Support & Resources

### Documentation
- **Quick Setup**: `QUICK_POWERBI_SETUP.md`
- **Online Guide**: `ONLINE_POWERBI_SETUP.md`
- **Full Implementation**: `POWERBI_IMPLEMENTATION_GUIDE.md`
- **Authentication Solutions**: `AUTHENTICATION_SOLUTIONS.md`

### Community
- **GitHub Repository**: https://github.com/Reshigan/bevco-executive-dashboard
- **Power BI Community**: https://community.powerbi.com
- **Microsoft Docs**: https://docs.microsoft.com/power-bi/

### Getting Help
1. Check the troubleshooting section above
2. Review the comprehensive guides in the repository
3. Create an issue on GitHub for bugs or feature requests
4. Ask questions in the Power BI Community forums

---

**🎉 Ready to build your executive dashboard on Mac?**

Start with the web import tool for the easiest experience, or choose the automation method that fits your workflow. All approaches are designed to work seamlessly with macOS and get you to a working Power BI dashboard quickly!

**Happy dashboard building!** 🚀