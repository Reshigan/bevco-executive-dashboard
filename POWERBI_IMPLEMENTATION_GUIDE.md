# Power BI Implementation Guide - Bevco Executive Dashboard

## 🚀 Complete Implementation Steps for app.powerbi.com

This guide provides step-by-step instructions to implement the Bevco Executive Dashboard in your Power BI Service environment.

## Prerequisites

1. **Power BI Pro or Premium License** (Required for sharing)
2. **Power BI Desktop** (Latest version)
3. **Admin access** to create workspaces in Power BI Service
4. **Python 3.8+** (for data generation)

## 📋 Implementation Checklist

- [ ] Download and prepare the project
- [ ] Generate sample data
- [ ] Create Power BI workspace
- [ ] Import data model
- [ ] Apply DAX measures
- [ ] Build visualizations
- [ ] Configure security
- [ ] Publish to Power BI Service
- [ ] Set up refresh schedule
- [ ] Share with users

## Step 1: Download and Prepare Project

### Option A: Clone from GitHub
```bash
git clone https://github.com/Reshigan/bevco-executive-dashboard.git
cd bevco-executive-dashboard
```

### Option B: Download ZIP
1. Go to https://github.com/Reshigan/bevco-executive-dashboard
2. Click "Code" → "Download ZIP"
3. Extract to your local drive (e.g., `C:\BevcoeDashboard`)

## Step 2: Generate Sample Data

### Windows
```batch
cd C:\BevcoeDashboard
scripts\setup.bat
```

### Mac/Linux
```bash
cd /path/to/bevco-executive-dashboard
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will create sample data files in the `data/master/` directory.

## Step 3: Create Power BI Workspace

1. **Log in to Power BI Service**
   - Go to https://app.powerbi.com
   - Sign in with your organizational account

2. **Create New Workspace**
   - Click "Workspaces" in the left navigation
   - Click "Create a workspace"
   - Name: "Bevco Executive Dashboard"
   - Description: "Executive analytics and KPI monitoring"
   - Advanced settings:
     - License mode: Pro or Premium
     - Develop a template app: No

3. **Configure Workspace Settings**
   - Go to Workspace settings
   - Members: Add team members
   - Admin: Assign workspace admins

## Step 4: Import Data in Power BI Desktop

### Automated Import Method

1. **Open Power BI Desktop**

2. **Run Import Script**
   ```powershell
   # In PowerShell (as Administrator)
   cd C:\BevcoeDashboard
   powershell -ExecutionPolicy Bypass .\scripts\import_to_powerbi.ps1
   ```

3. **Manual Import Steps**
   - Click "Get Data" → "Text/CSV"
   - Navigate to `data/master/` folder
   - Select all CSV files:
     - dim_date.csv
     - dim_product.csv
     - dim_customer.csv
     - dim_employee.csv
     - fact_sales.csv
     - fact_budget.csv
     - fact_inventory.csv
     - dim_kpi_targets.csv
   - Click "Load"

### Configure Data Types

Power Query Editor will open. For each table, ensure correct data types:

1. **Dim_Date**
   ```
   DateKey: Whole Number
   Date: Date
   Year, Quarter, Month: Whole Number
   MonthName, DayName: Text
   ```

2. **Dim_Product**
   ```
   ProductKey: Whole Number
   UnitCost, UnitPrice: Decimal Number
   LaunchDate: Date
   Other fields: Text
   ```

3. **Fact_Sales**
   ```
   All Key fields: Whole Number
   All amount fields: Decimal Number
   DiscountPercent: Decimal Number
   ```

## Step 5: Create Relationships

1. **Go to Model View** (icon on the left)

2. **Create these relationships** (drag and drop):
   ```
   Fact_Sales[DateKey] → Dim_Date[DateKey]
   Fact_Sales[ProductKey] → Dim_Product[ProductKey]
   Fact_Sales[CustomerKey] → Dim_Customer[CustomerKey]
   Fact_Sales[EmployeeKey] → Dim_Employee[EmployeeKey]
   Fact_Budget[DateKey] → Dim_Date[DateKey]
   Fact_Inventory[ProductKey] → Dim_Product[ProductKey]
   ```

3. **Configure Relationship Properties**:
   - All relationships: Single direction
   - Cross filter: Single
   - Cardinality: Many to One (*)

## Step 6: Import DAX Measures

### Automated DAX Import

1. **Install Tabular Editor** (Optional but recommended)
   - Download from: https://tabulareditor.com/
   - Install and restart Power BI Desktop

2. **Run DAX Import Script**
   - In Tabular Editor: File → Open → From DB
   - Connect to your Power BI model
   - Advanced Scripting → Run Script
   - Copy contents from `powerbi/datasets/ImportDAXMeasures.csx`

### Manual DAX Import

1. **Go to Data View**
2. **Select Fact_Sales table**
3. **Create New Measure** (right-click → New Measure)
4. **Copy measures from** `powerbi/datasets/DAX_Measures.txt`

Key measures to create first:
```dax
Total Net Sales = SUM(Fact_Sales[NetSales])

Total Sales LY = 
CALCULATE(
    [Total Net Sales],
    SAMEPERIODLASTYEAR(Dim_Date[Date])
)

Sales YoY Growth % = 
DIVIDE(
    [Total Net Sales] - [Total Sales LY],
    [Total Sales LY],
    0
)

Gross Profit Margin % = 
DIVIDE(
    SUM(Fact_Sales[GrossProfit]),
    SUM(Fact_Sales[NetSales]),
    0
)
```

## Step 7: Build Dashboards

### Page 1: Executive Summary

1. **Add KPI Cards** (Insert → Card Visual)
   - Total Net Sales
   - Gross Profit Margin %
   - Sales YoY Growth %
   - Total Customers

2. **Add Line Chart** (Sales Trend)
   - Axis: Dim_Date[Date]
   - Values: Total Net Sales
   - Add Average Line

3. **Add Map Visual** (Regional Performance)
   - Location: Dim_Customer[Region]
   - Size: Total Net Sales

4. **Add Slicers**
   - Date Range (Dim_Date[Date])
   - Product Category (Dim_Product[Category])
   - Region (Dim_Customer[Region])

### Page 2: Sales Analytics

Follow the structure in `powerbi/reports/Dashboard_Structure.md`

## Step 8: Apply Formatting

### Color Theme
```json
{
  "name": "Bevco Theme",
  "dataColors": ["#003366", "#0066CC", "#3399FF", "#66B2FF", "#99CCFF"],
  "background": "#FFFFFF",
  "foreground": "#003366",
  "tableAccent": "#003366"
}
```

1. View → Themes → Browse for themes
2. Save above as `BevcoTheme.json`
3. Apply to report

## Step 9: Configure Security

### Set Up Row-Level Security (RLS)

1. **Modeling → Manage Roles**

2. **Create Roles**:
   ```dax
   // Regional Manager Role
   [Region] = USERNAME()
   
   // Department Head Role
   [Department] = USERPRINCIPALNAME()
   ```

3. **Test Roles**:
   - Modeling → View as
   - Select role to test
   - Verify data filtering

## Step 10: Publish to Power BI Service

1. **Save your .pbix file**
   - File → Save As
   - Name: "Bevco_Executive_Dashboard_v1.pbix"

2. **Publish to Service**
   - Home → Publish
   - Select "Bevco Executive Dashboard" workspace
   - Click "Select"

3. **Open in Service**
   - Click "Open in Power BI" after publishing
   - Or go to app.powerbi.com

## Step 11: Configure in Power BI Service

### Dataset Settings

1. **Go to Workspace**
2. **Find your dataset** → Settings (⚙️)
3. **Configure**:

#### Data Source Credentials
- Edit credentials
- Privacy level: Organizational

#### Scheduled Refresh
- Scheduled refresh: On
- Frequency: Daily
- Time: 6:00 AM, 2:00 PM
- Send refresh failure notifications: Yes

#### Featured Tables
- Select key tables for Excel integration

### Report Settings

1. **Persistent Filters**: Enable
2. **Export Options**: Allow
3. **Comments**: Enable

## Step 12: Create App for Distribution

1. **In Workspace** → Create app

2. **Setup Tab**:
   - App name: "Bevco Executive Dashboard"
   - Description: "Real-time business analytics"
   - App logo: Upload logo
   - App theme color: #003366

3. **Navigation Tab**:
   - New navigation builder
   - Add sections for each dashboard area

4. **Permissions Tab**:
   - Entire organization or specific users/groups
   - Build permissions as needed

5. **Publish App**

## Step 13: Set Up Mobile Access

1. **Download Power BI Mobile App**
   - iOS: App Store
   - Android: Google Play

2. **Configure Mobile Layout** (in Desktop):
   - View → Mobile Layout
   - Arrange visuals for mobile
   - Publish updates

## Step 14: Configure Alerts

In Power BI Service:

1. **Pin visual to dashboard**
2. **Click "..." → Manage alerts**
3. **Set conditions**:
   - Alert if Total Sales < 140M
   - Alert if Gross Margin < 30%
   - Check hourly

## 🔧 Troubleshooting

### Common Issues

1. **"Dataset not found" error**
   - Ensure all CSV files are loaded
   - Check file paths in Power Query

2. **Relationships not working**
   - Verify key columns have matching data types
   - Check for duplicate keys

3. **Measures showing errors**
   - Ensure all referenced columns exist
   - Check DAX syntax

4. **Refresh failures**
   - Verify gateway is installed (for on-premises data)
   - Check credentials

### Performance Optimization

1. **Reduce data volume**:
   ```powerquery
   // In Power Query, filter to last 2 years
   = Table.SelectRows(Source, each [Date] >= Date.AddYears(DateTime.Date(DateTime.LocalNow()), -2))
   ```

2. **Create aggregation tables**
3. **Use incremental refresh** for large datasets

## 📊 Quick Test

After implementation, verify:

1. **KPIs calculate correctly**
   - Total Sales should show ~R27M for 6 months
   - 724 active customers
   - 339 products

2. **Filters work**
   - Date slicers update all visuals
   - Cross-filtering between charts

3. **Mobile view loads**
   - Test on phone/tablet

## 🎯 Next Steps

1. **Training**:
   - Schedule user training sessions
   - Create custom training materials

2. **Customization**:
   - Add company logo
   - Adjust color scheme
   - Add custom visuals

3. **Integration**:
   - Connect to live data sources
   - Set up real-time streaming
   - Integrate with Teams

## 📞 Support Resources

- **Documentation**: `/documentation/` folder
- **DAX Reference**: `/powerbi/datasets/DAX_Measures.txt`
- **User Guide**: `/documentation/user-guides/`
- **GitHub Issues**: https://github.com/Reshigan/bevco-executive-dashboard/issues

---

**Need help?** Create an issue on GitHub or refer to the comprehensive documentation included in the project.