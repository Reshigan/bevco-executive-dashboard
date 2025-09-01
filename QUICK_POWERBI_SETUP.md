# 🚀 Quick Power BI Setup - 15 Minutes to Dashboard

## Fastest Path to Implementation

### 1️⃣ Download & Generate Data (2 minutes)
```bash
# Option A: Clone from GitHub
git clone https://github.com/Reshigan/bevco-executive-dashboard.git
cd bevco-executive-dashboard

# Option B: Download ZIP from GitHub and extract

# Generate sample data
# Windows: 
scripts\setup.bat
# Mac/Linux: 
./scripts/setup.sh
```

### 2️⃣ Open Power BI Desktop (1 minute)
- Launch Power BI Desktop
- Sign in with your organizational account

### 3️⃣ Import All Data at Once (3 minutes)
1. Click **Get Data** → **Folder**
2. Browse to `bevco-executive-dashboard/data/master/`
3. Click **Combine & Transform Data**
4. In the preview window, click **OK**
5. Click **Close & Apply**

### 4️⃣ Quick Model Setup (2 minutes)
1. Go to **Model View** (icon on left)
2. Power BI should auto-detect most relationships
3. Verify these key relationships exist:
   - Fact_Sales → Dim_Date (DateKey)
   - Fact_Sales → Dim_Product (ProductKey)
   - Fact_Sales → Dim_Customer (CustomerKey)

### 5️⃣ Create Essential Measures (3 minutes)
1. Go to **Data View**
2. Select **Fact_Sales** table
3. Click **New Measure** and paste:

```dax
Total Sales = SUM(Fact_Sales[NetSales])
```

4. Create another measure:
```dax
Sales YoY % = 
VAR CurrentSales = [Total Sales]
VAR PriorSales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Dim_Date[Date]))
RETURN DIVIDE(CurrentSales - PriorSales, PriorSales, 0)
```

5. One more measure:
```dax
Profit Margin % = DIVIDE(SUM(Fact_Sales[GrossProfit]), SUM(Fact_Sales[NetSales]), 0)
```

### 6️⃣ Build Quick Dashboard (3 minutes)
1. Go to **Report View**
2. Add visualizations:
   - **Card**: Drag Total Sales
   - **Card**: Drag Profit Margin %
   - **Line Chart**: Date on Axis, Total Sales on Values
   - **Map**: Customer[Region] on Location, Total Sales on Size
   - **Slicer**: Add Date[Year]

### 7️⃣ Publish to Power BI Service (1 minute)
1. Click **Publish** (Home ribbon)
2. Select or create workspace "Bevco Dashboard"
3. Click **Select**
4. Click **Open in Power BI** when complete

## 🎯 You're Done! 

Your dashboard is now live at: https://app.powerbi.com

## 📊 What You Get

✅ **Working Dashboard** with real sample data
✅ **36,400 sales transactions** across 6 months
✅ **Interactive visualizations** with filters
✅ **Mobile-ready** design
✅ **Shareable** with your team

## 🔥 Next Steps (Optional)

### Add More Visualizations
- Sales by Product Category (Pie Chart)
- Top 10 Customers (Bar Chart)
- Monthly Trend Analysis (Area Chart)

### Import All 60+ Measures
Copy from `powerbi/datasets/DAX_Measures.txt`

### Configure Refresh
1. In Power BI Service, go to dataset settings
2. Set up daily refresh schedule
3. Configure gateway if needed

### Create Mobile Layout
1. In Power BI Desktop: View → Mobile Layout
2. Arrange visuals for phone screens
3. Republish

## 💡 Pro Tips

1. **Performance**: If slow, reduce date range in slicers
2. **Sharing**: Create an app for easy distribution
3. **Alerts**: Set up data alerts on KPI cards
4. **Export**: Enable export to Excel for users

## 🆘 Quick Troubleshooting

**"Can't see data"**
- Check if relationships are active in Model view
- Verify date format in Dim_Date table

**"Measures show errors"**
- Ensure column names match exactly
- Check for typos in DAX formulas

**"Can't publish"**
- Verify Power BI Pro license
- Check workspace permissions

## 📱 Access Your Dashboard

**Web**: https://app.powerbi.com
**Mobile**: Download Power BI app
**Teams**: Add as a tab in Microsoft Teams

---

**Need the full implementation guide?** See [POWERBI_IMPLEMENTATION_GUIDE.md](POWERBI_IMPLEMENTATION_GUIDE.md)

**Questions?** Check our [GitHub Issues](https://github.com/Reshigan/bevco-executive-dashboard/issues)