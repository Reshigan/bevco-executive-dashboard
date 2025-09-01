# 📊 Power BI Template Files (.pbit) - Usage Guide

## 🎯 Ready-to-Use PBIT Templates

The following Power BI Template files have been created and are ready for use:


### 1. BevcoExecutiveDashboard.pbit
**Type:** Executive Dashboard
**Description:** Complete executive dashboard with all KPIs and visualizations
**File Size:** 2.7 KB
**Location:** `pbit_templates/BevcoExecutiveDashboard.pbit`


### 2. BevcoSalesAnalysis.pbit
**Type:** Sales Dashboard
**Description:** Sales-focused dashboard for sales teams and managers
**File Size:** 2.2 KB
**Location:** `pbit_templates/BevcoSalesAnalysis.pbit`


### 3. BevcoFinancialReporting.pbit
**Type:** Financial Dashboard
**Description:** Financial dashboard with budget vs actual analysis
**File Size:** 2.4 KB
**Location:** `pbit_templates/BevcoFinancialReporting.pbit`


### 4. BevcoOperationalMetrics.pbit
**Type:** Operational Dashboard
**Description:** Operational dashboard with inventory and employee metrics
**File Size:** 2.6 KB
**Location:** `pbit_templates/BevcoOperationalMetrics.pbit`


## 🚀 How to Use PBIT Templates

### Step 1: Double-Click to Open
1. **Locate the .pbit file** in the `pbit_templates` folder
2. **Double-click the file** - Power BI Desktop will open automatically
3. **Power BI will prompt** for data source location

### Step 2: Point to Your Data
When Power BI opens the template, it will ask for the data source:

1. **Browse to your CSV files** location:
   - `data/master/` folder (if using project structure)
   - Your Downloads folder (if downloaded separately)
   - Any folder containing the CSV files

2. **Select the folder** containing these files:
   - `dim_date.csv`
   - `dim_product.csv`
   - `dim_customer.csv`
   - `dim_employee.csv` (for executive/operational templates)
   - `fact_sales.csv`
   - `fact_budget.csv` (for executive/financial templates)
   - `fact_inventory.csv` (for executive/operational templates)
   - `dim_kpi_targets.csv`

3. **Click "Load"** - Power BI will import all the data

### Step 3: Customize and Publish
1. **Review the data model** - All relationships are pre-configured
2. **Add visualizations** - Use the pre-built DAX measures
3. **Customize branding** - Add your company colors and logos
4. **Save your work** - File → Save As → Choose location
5. **Publish to Service** - File → Publish → Select workspace

## 📊 What's Included in Each Template

### BevcoExecutiveDashboard.pbit
**Complete executive dashboard with:**
- ✅ All 8 data tables with relationships
- ✅ 20+ DAX measures for KPIs
- ✅ Sales, financial, and operational metrics
- ✅ Time intelligence calculations
- ✅ Budget vs actual analysis
- ✅ Inventory and employee metrics

**Perfect for:** C-level executives, general managers

### BevcoSalesAnalysis.pbit
**Sales-focused dashboard with:**
- ✅ Core sales tables (date, product, customer, sales)
- ✅ Sales performance measures
- ✅ Product and customer analysis
- ✅ Time-based comparisons
- ✅ Growth and trend calculations

**Perfect for:** Sales directors, sales managers, account managers

### BevcoFinancialReporting.pbit
**Financial dashboard with:**
- ✅ Sales and budget tables
- ✅ Financial KPIs and ratios
- ✅ Budget vs actual analysis
- ✅ Variance calculations
- ✅ P&L components

**Perfect for:** CFOs, finance managers, financial analysts

### BevcoOperationalMetrics.pbit
**Operational dashboard with:**
- ✅ Sales, inventory, and employee tables
- ✅ Operational efficiency metrics
- ✅ Inventory management KPIs
- ✅ Employee productivity measures
- ✅ Supply chain indicators

**Perfect for:** Operations directors, warehouse managers, HR managers

## 🎨 Pre-Built DAX Measures

All templates include these calculated measures:

### Sales Metrics
- **Total Sales:** `SUM(fact_sales[NetSales])`
- **Total Profit:** `SUM(fact_sales[GrossProfit])`
- **Profit Margin %:** `DIVIDE([Total Profit], [Total Sales], 0)`
- **Average Order Value:** `DIVIDE([Total Sales], DISTINCTCOUNT(fact_sales[InvoiceNumber]), 0)`

### Time Intelligence
- **Total Sales LY:** `CALCULATE([Total Sales], SAMEPERIODLASTYEAR(dim_date[Date]))`
- **Sales Growth %:** `DIVIDE([Total Sales] - [Total Sales LY], [Total Sales LY], 0)`
- **YTD Sales:** `TOTALYTD([Total Sales], dim_date[Date])`

### Budget Metrics (Executive/Financial)
- **Budget Amount:** `SUM(fact_budget[BudgetAmount])`
- **Budget Variance %:** `DIVIDE([Actual Amount] - [Budget Amount], [Budget Amount], 0)`

### Inventory Metrics (Executive/Operational)
- **Total Stock Value:** `SUMX(fact_inventory, fact_inventory[StockOnHand] * RELATED(dim_product[UnitCost]))`

## 🔧 Troubleshooting

### "Can't find data files"
1. **Check file location:** Ensure CSV files are in the folder you selected
2. **File names match:** Verify CSV file names are exactly as expected
3. **Try different folder:** Browse to the correct data folder

### "Data not loading"
1. **Check CSV format:** Ensure files are properly formatted
2. **File permissions:** Make sure Power BI can read the files
3. **Try refresh:** Click "Refresh" in Power BI Desktop

### "Relationships not working"
1. **Data types:** Key columns should be integers (DateKey, ProductKey, etc.)
2. **Missing data:** Check for null values in key columns
3. **Reload template:** Close and reopen the .pbit file

### "Measures showing errors"
1. **Tables loaded:** Confirm all required tables have data
2. **Column names:** Verify column names match exactly
3. **Data types:** Ensure numeric columns are properly typed

## 📱 Mobile Optimization

All templates are designed to work well on mobile devices:
- **Responsive layouts:** Adapt to different screen sizes
- **Touch-friendly:** Large buttons and touch targets
- **Power BI Mobile:** Works with iOS and Android apps
- **Offline capability:** View cached data without internet

## 🔄 Data Refresh

### Manual Refresh
1. **Open template** in Power BI Desktop
2. **Click "Refresh"** to update data
3. **Save and republish** to Power BI Service

### Scheduled Refresh (Power BI Service)
1. **Publish template** to Power BI Service
2. **Configure data source** in workspace settings
3. **Set refresh schedule** (daily, weekly, etc.)
4. **Monitor refresh status** in refresh history

## 🎯 Next Steps

1. **Choose the right template** for your role and needs
2. **Double-click to open** in Power BI Desktop
3. **Point to your CSV data** when prompted
4. **Customize visuals** and branding as needed
5. **Publish to Power BI Service** for sharing
6. **Set up refresh schedules** for automatic updates

## 📞 Support

For help with PBIT templates:
- **Check troubleshooting** section above
- **Review Power BI documentation** at docs.microsoft.com
- **Visit Power BI Community** at community.powerbi.com
- **Create GitHub issue** for bugs or feature requests

---

**🎉 Your Power BI templates are ready to use!**

Simply double-click any .pbit file to get started with your executive dashboard in minutes.

**Pro Tip:** Start with BevcoExecutiveDashboard.pbit for the complete experience, then create specialized dashboards using the other templates.
