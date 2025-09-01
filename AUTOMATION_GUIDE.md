# 🤖 Bevco Dashboard - Full Automation Guide

## 🚀 Automated Deployment to app.powerbi.com

This guide provides **three automated methods** to generate data, create dashboards, and publish everything to Power BI Service without manual intervention.

## 🎯 What the Automation Does

✅ **Generates 36,400+ sample transactions** with realistic business data  
✅ **Creates Power BI workspace** automatically  
✅ **Uploads datasets** with proper relationships  
✅ **Builds executive dashboards** with KPIs and visualizations  
✅ **Publishes to app.powerbi.com** ready for use  
✅ **Sets up data refresh** schedules  
✅ **Creates shareable apps** for distribution  

## 🛠️ Method 1: PowerShell Automation (Recommended for Windows)

### Prerequisites
- Windows 10/11 with PowerShell 5.1+
- Power BI Pro or Premium license
- Excel installed (for data conversion)
- Internet connection

### Quick Start
```powershell
# Navigate to project directory
cd C:\path\to\bevco-executive-dashboard

# Run full automation
powershell -ExecutionPolicy Bypass .\scripts\PowerBI_Full_Automation.ps1
```

### Advanced Options
```powershell
# Custom workspace name
.\scripts\PowerBI_Full_Automation.ps1 -WorkspaceName "My Custom Dashboard"

# Service Principal authentication (for enterprise)
.\scripts\PowerBI_Full_Automation.ps1 -UseServicePrincipal -TenantId "your-tenant-id" -ClientId "your-client-id" -ClientSecret "your-secret"

# Skip sample dashboard creation
.\scripts\PowerBI_Full_Automation.ps1 -CreateSampleDashboard:$false
```

### What It Does
1. **Installs Power BI PowerShell modules** automatically
2. **Generates sample data** (36,400 transactions)
3. **Creates Excel workbook** with all tables
4. **Connects to Power BI Service** (interactive login)
5. **Creates workspace** "Bevco Executive Dashboard"
6. **Uploads dataset** with relationships
7. **Creates dashboard** with sample tiles
8. **Creates report** with visualizations
9. **Sets up data refresh** (daily at 6 AM and 2 PM)
10. **Publishes app** for sharing

## 🐍 Method 2: Python Automation (Cross-platform)

### Prerequisites
- Python 3.8+
- Power BI Pro or Premium license
- Internet connection

### Installation
```bash
# Install required packages
pip install requests pandas openpyxl

# Navigate to project directory
cd /path/to/bevco-executive-dashboard
```

### Quick Start
```bash
# Run full automation with interactive login
python scripts/powerbi_automation.py

# Custom workspace name
python scripts/powerbi_automation.py --workspace "My Dashboard"
```

### Service Principal Authentication
```bash
# For enterprise automation
python scripts/powerbi_automation.py \
  --tenant-id "your-tenant-id" \
  --client-id "your-client-id" \
  --client-secret "your-secret" \
  --workspace "Bevco Executive Dashboard"
```

### What It Does
1. **Generates sample data** using standalone script
2. **Authenticates with Power BI** (device code or service principal)
3. **Creates workspace** automatically
4. **Creates push datasets** with schema
5. **Loads sample data** into Power BI
6. **Creates dashboard** and reports
7. **Provides direct URLs** to access everything

## 🖱️ Method 3: One-Click Launcher (Windows)

### Super Simple Setup
```batch
# Just double-click this file:
scripts\run_automation.bat
```

This launcher gives you options:
1. **PowerShell Automation** (full featured)
2. **Python Automation** (cross-platform)
3. **Manual Setup Guide** (step-by-step)

## 🔐 Authentication Options

### Option A: Interactive Login (Default)
- Browser opens automatically
- Sign in with your Power BI account
- Works with any Power BI Pro/Premium license

### Option B: Service Principal (Enterprise)
- Requires Azure AD app registration
- Fully automated (no user interaction)
- Perfect for CI/CD pipelines

#### Setting Up Service Principal
1. **Register Azure AD App**:
   - Go to Azure Portal → App Registrations
   - Create new registration
   - Note: Application (client) ID

2. **Create Client Secret**:
   - Go to Certificates & secrets
   - Create new client secret
   - Copy the secret value

3. **Grant Power BI Permissions**:
   - Go to API permissions
   - Add Power BI Service permissions
   - Grant admin consent

4. **Enable Service Principal in Power BI**:
   - Power BI Admin Portal → Tenant settings
   - Enable "Service principals can use Power BI APIs"

## 📊 Generated Dashboard Features

### Executive Summary Page
- **Total Sales KPI** with trend indicators
- **Regional Performance Map** of South Africa
- **Monthly Sales Trend** line chart
- **Product Category Analysis** bar chart
- **Customer Channel Mix** pie chart

### Sales Analytics Page
- **Top 10 Customers** table
- **Sales by Region** heat map
- **Product Performance** matrix
- **Sales Rep Leaderboard** 
- **Channel Comparison** charts

### Financial Management Page
- **P&L Summary** cards
- **Budget vs Actual** variance analysis
- **Cash Flow Trends** 
- **Profitability Analysis** by segment
- **Cost Structure** breakdown

### Operational Metrics Page
- **Inventory Levels** by warehouse
- **Stock Coverage** analysis
- **Supply Chain KPIs**
- **Quality Metrics** dashboard

## 🔄 Data Refresh Setup

The automation automatically configures:
- **Daily refresh** at 6 AM and 2 PM (South Africa time)
- **Email notifications** on refresh failures
- **Incremental refresh** for large datasets
- **Gateway configuration** prompts (if needed)

## 📱 Mobile & Sharing

### Automatic App Creation
- **Published app** ready for distribution
- **Mobile-optimized** layouts
- **Role-based security** configured
- **Sharing permissions** set up

### Access URLs
After automation completes, you'll get:
- **Workspace URL**: Direct access to edit
- **Dashboard URL**: View the executive dashboard
- **Report URL**: Interactive report access
- **App URL**: End-user friendly app

## 🆘 Troubleshooting

### Common Issues

#### "PowerShell execution policy error"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### "Python module not found"
```bash
pip install --upgrade requests pandas openpyxl
```

#### "Power BI authentication failed"
- Check your Power BI Pro/Premium license
- Verify you have workspace creation permissions
- Try clearing browser cache and re-authenticate

#### "Dataset upload failed"
- Check file sizes (Excel files should be < 1GB)
- Verify data format and column names
- Ensure no special characters in data

### Getting Help

1. **Check the logs** - Both scripts provide detailed error messages
2. **Verify prerequisites** - Ensure all requirements are met
3. **Test manually** - Try the ONLINE_POWERBI_SETUP.md guide first
4. **GitHub Issues** - Report problems at the repository

## 🎉 Success Indicators

When automation completes successfully, you should see:

✅ **"Automation Complete!"** message  
✅ **Workspace URL** provided  
✅ **Dashboard accessible** at app.powerbi.com  
✅ **Sample data loaded** (36,400+ records)  
✅ **Visualizations working** with real data  
✅ **Mobile app access** enabled  

## 🚀 Next Steps After Automation

1. **Customize Dashboards**
   - Add your company logo
   - Adjust color schemes
   - Modify KPI targets

2. **Connect Real Data**
   - Replace sample data with live connections
   - Set up data gateways
   - Configure incremental refresh

3. **Share with Team**
   - Add users to workspace
   - Distribute app to organization
   - Set up email subscriptions

4. **Monitor Usage**
   - Check usage metrics
   - Set up alerts
   - Gather user feedback

## 💡 Pro Tips

- **Run during off-hours** - Initial setup takes 10-15 minutes
- **Use service principal** for production deployments
- **Test with sample data first** before connecting live systems
- **Document customizations** for future updates
- **Set up backup schedules** for important dashboards

---

**🎯 Ready to automate your Power BI deployment?**

Choose your method above and get your executive dashboard live in minutes!

For questions or issues, check our [GitHub repository](https://github.com/Reshigan/bevco-executive-dashboard) or create an issue.