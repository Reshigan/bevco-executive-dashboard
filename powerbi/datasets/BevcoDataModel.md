# Bevco Executive Dashboard - Data Model

## Star Schema Design

### Fact Tables

#### 1. Fact_Sales
Primary transactional data for sales analysis.

**Columns:**
- SalesKey (Primary Key)
- DateKey (Foreign Key to Dim_Date)
- ProductKey (Foreign Key to Dim_Product)
- CustomerKey (Foreign Key to Dim_Customer)
- EmployeeKey (Foreign Key to Dim_Employee)
- InvoiceNumber
- Quantity
- UnitPrice
- GrossSales
- DiscountPercent
- DiscountAmount
- NetSales
- Cost
- GrossProfit

#### 2. Fact_Budget
Budget and forecast data for variance analysis.

**Columns:**
- BudgetKey (Primary Key)
- DateKey (Foreign Key to Dim_Date)
- Year
- Month
- Department
- BudgetAmount
- ForecastAmount
- ActualAmount

#### 3. Fact_Inventory
Current inventory levels and stock metrics.

**Columns:**
- InventoryKey (Primary Key)
- ProductKey (Foreign Key to Dim_Product)
- Warehouse
- StockOnHand
- ReorderPoint
- MaxStock
- StockValue
- DaysOnHand
- LastUpdated

### Dimension Tables

#### 1. Dim_Date
Time dimension for all date-based analysis.

**Columns:**
- DateKey (Primary Key)
- Date
- Year
- Quarter
- Month
- MonthName
- Week
- DayOfWeek
- DayName
- DayOfMonth
- DayOfYear
- IsWeekend
- IsHoliday
- FiscalYear
- FiscalQuarter
- FiscalMonth

#### 2. Dim_Product
Product master data with hierarchy.

**Columns:**
- ProductKey (Primary Key)
- SKU
- ProductName
- Vendor
- Category
- SubCategory
- Brand
- PackSize
- UnitCost
- UnitPrice
- LaunchDate
- Status

#### 3. Dim_Customer
Customer master data with geographic and channel information.

**Columns:**
- CustomerKey (Primary Key)
- CustomerCode
- CustomerName
- Channel
- CustomerType
- Region
- Province
- City
- CreditLimit
- PaymentTerms
- Status
- OnboardingDate

#### 4. Dim_Employee
Employee master data with organizational hierarchy.

**Columns:**
- EmployeeKey (Primary Key)
- EmployeeCode
- Name
- Position
- Department
- ReportsTo
- HireDate
- Salary
- EmploymentType

#### 5. Dim_KPI_Targets
KPI targets for performance measurement.

**Columns:**
- KPIName
- Target
- Unit
- Frequency

## Relationships

1. **Fact_Sales to Dim_Date**: DateKey (Many-to-One)
2. **Fact_Sales to Dim_Product**: ProductKey (Many-to-One)
3. **Fact_Sales to Dim_Customer**: CustomerKey (Many-to-One)
4. **Fact_Sales to Dim_Employee**: EmployeeKey (Many-to-One)
5. **Fact_Budget to Dim_Date**: DateKey (Many-to-One)
6. **Fact_Inventory to Dim_Product**: ProductKey (Many-to-One)

## Key Measures (DAX)

### Sales Measures
```dax
Total Sales = SUM(Fact_Sales[NetSales])

Total Sales LY = 
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR(Dim_Date[Date])
)

Sales Growth % = 
DIVIDE(
    [Total Sales] - [Total Sales LY],
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

### Budget Measures
```dax
Total Budget = SUM(Fact_Budget[BudgetAmount])

Total Actual = SUM(Fact_Budget[ActualAmount])

Budget Variance = [Total Actual] - [Total Budget]

Budget Variance % = 
DIVIDE(
    [Budget Variance],
    [Total Budget],
    0
)
```

### Inventory Measures
```dax
Total Stock Value = SUM(Fact_Inventory[StockValue])

Avg Days On Hand = AVERAGE(Fact_Inventory[DaysOnHand])

Stock Coverage Days = 
DIVIDE(
    [Total Stock Value],
    [Total Sales] / 365,
    0
)
```

### Customer Measures
```dax
Active Customers = 
CALCULATE(
    DISTINCTCOUNT(Fact_Sales[CustomerKey]),
    Dim_Customer[Status] = "Active"
)

Revenue per Customer = 
DIVIDE(
    [Total Sales],
    [Active Customers],
    0
)
```

## Row-Level Security (RLS)

### Regional Security
```dax
[Region] = USERNAME()
```

### Department Security
```dax
[Department] = USERPRINCIPALNAME()
```

## Performance Optimization

1. **Aggregations**: Create aggregated tables for commonly used summaries
2. **Partitioning**: Partition fact tables by year/month
3. **Indexing**: Create columnstore indexes on fact tables
4. **Incremental Refresh**: Set up incremental refresh for sales data