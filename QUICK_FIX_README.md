# 🔧 Quick Fix for Data Generation Issue

## Problem
The setup script failed with a "Read-only file system" error when trying to create directories.

## ✅ Solution - Use the Standalone Data Generator

### Option 1: Run the Standalone Script (Recommended)
```bash
# Navigate to your project directory
cd /path/to/bevco-executive-dashboard

# Run the standalone data generator
python3 generate_data_standalone.py
```

This script will:
- ✅ Create data directories automatically
- ✅ Generate all 8 CSV files with sample data
- ✅ Work from any directory location
- ✅ Handle path issues gracefully

### Option 2: Manual Directory Creation
```bash
# Create directories first
mkdir -p data/master
mkdir -p data/processed

# Then run the original script
python3 scripts/etl/generate_master_data.py
```

### Option 3: Use Current Directory
If you're still having issues, the standalone script will create a `master_data` folder in your current directory with all the files.

## 📊 What You'll Get

After running the standalone script:
- **36,400 sales transactions** across 6 months
- **724 customers** across 9 South African regions  
- **339 products** from 5 major vendors
- **319 employees** across 6 departments
- **Complete data model** ready for Power BI

## 🚀 Next Steps for Power BI Online

1. **Go to app.powerbi.com**
2. **Create a workspace** called "Bevco Executive Dashboard"
3. **Upload CSV files** one by one using "New" → "Upload a file"
4. **Create report** by clicking on any dataset
5. **Build your dashboard** with the sample data

## 📁 Files Generated

- `dim_date.csv` - Date dimension (4 years)
- `dim_product.csv` - Product catalog
- `dim_customer.csv` - Customer master data
- `dim_employee.csv` - Employee directory
- `fact_sales.csv` - Sales transactions (main data)
- `fact_budget.csv` - Budget vs actual data
- `fact_inventory.csv` - Stock levels
- `dim_kpi_targets.csv` - Performance targets

## 💡 Pro Tips

- **For Excel conversion**: Use the PowerShell script `scripts/PowerBI_Online_Setup.ps1`
- **For web tools**: Run `python3 scripts/serve_web_tools.py` for interactive tools
- **For quick setup**: Follow `ONLINE_POWERBI_SETUP.md` for step-by-step guide

## 🆘 Still Having Issues?

1. Make sure you have Python 3.8+ installed
2. Install required packages: `pip3 install pandas numpy openpyxl`
3. Run from the project root directory
4. Check that you have write permissions in the directory

The standalone script is designed to work in any environment and will find the best location for your data files.

---

**Ready to build your executive dashboard!** 🎉