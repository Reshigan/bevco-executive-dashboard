# PowerShell script to set up Power BI data connections
# Run this script in Power BI Desktop's External Tools or PowerShell

# Set working directory
$WorkingDir = "C:\BevcoExecutiveDashboard"
$DataDir = "$WorkingDir\data\master"

# Create M Query for data import
$MQuery = @"
let
    // Date Dimension
    DateDimension = Csv.Document(
        File.Contents("$DataDir\dim_date.csv"),
        [Delimiter=",", Columns=16, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    DateHeaders = Table.PromoteHeaders(DateDimension, [PromoteAllScalars=true]),
    DateTyped = Table.TransformColumnTypes(DateHeaders,{
        {"DateKey", Int64.Type}, 
        {"Date", type date},
        {"Year", Int64.Type},
        {"Quarter", Int64.Type},
        {"Month", Int64.Type},
        {"MonthName", type text},
        {"Week", Int64.Type},
        {"DayOfWeek", Int64.Type},
        {"DayName", type text},
        {"DayOfMonth", Int64.Type},
        {"DayOfYear", Int64.Type},
        {"IsWeekend", Int64.Type},
        {"IsHoliday", Int64.Type},
        {"FiscalYear", Int64.Type},
        {"FiscalQuarter", Int64.Type},
        {"FiscalMonth", Int64.Type}
    }),

    // Product Dimension
    ProductDimension = Csv.Document(
        File.Contents("$DataDir\dim_product.csv"),
        [Delimiter=",", Columns=12, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    ProductHeaders = Table.PromoteHeaders(ProductDimension, [PromoteAllScalars=true]),
    ProductTyped = Table.TransformColumnTypes(ProductHeaders,{
        {"ProductKey", Int64.Type},
        {"SKU", type text},
        {"ProductName", type text},
        {"Vendor", type text},
        {"Category", type text},
        {"SubCategory", type text},
        {"Brand", type text},
        {"PackSize", type text},
        {"UnitCost", type number},
        {"UnitPrice", type number},
        {"LaunchDate", type date},
        {"Status", type text}
    }),

    // Customer Dimension
    CustomerDimension = Csv.Document(
        File.Contents("$DataDir\dim_customer.csv"),
        [Delimiter=",", Columns=12, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    CustomerHeaders = Table.PromoteHeaders(CustomerDimension, [PromoteAllScalars=true]),
    CustomerTyped = Table.TransformColumnTypes(CustomerHeaders,{
        {"CustomerKey", Int64.Type},
        {"CustomerCode", type text},
        {"CustomerName", type text},
        {"Channel", type text},
        {"CustomerType", type text},
        {"Region", type text},
        {"Province", type text},
        {"City", type text},
        {"CreditLimit", Int64.Type},
        {"PaymentTerms", Int64.Type},
        {"Status", type text},
        {"OnboardingDate", type date}
    }),

    // Employee Dimension
    EmployeeDimension = Csv.Document(
        File.Contents("$DataDir\dim_employee.csv"),
        [Delimiter=",", Columns=9, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    EmployeeHeaders = Table.PromoteHeaders(EmployeeDimension, [PromoteAllScalars=true]),
    EmployeeTyped = Table.TransformColumnTypes(EmployeeHeaders,{
        {"EmployeeKey", Int64.Type},
        {"EmployeeCode", type text},
        {"Name", type text},
        {"Position", type text},
        {"Department", type text},
        {"ReportsTo", Int64.Type},
        {"HireDate", type date},
        {"Salary", Int64.Type},
        {"EmploymentType", type text}
    }),

    // Sales Fact
    SalesFact = Csv.Document(
        File.Contents("$DataDir\fact_sales.csv"),
        [Delimiter=",", Columns=14, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    SalesHeaders = Table.PromoteHeaders(SalesFact, [PromoteAllScalars=true]),
    SalesTyped = Table.TransformColumnTypes(SalesHeaders,{
        {"SalesKey", Int64.Type},
        {"DateKey", Int64.Type},
        {"ProductKey", Int64.Type},
        {"CustomerKey", Int64.Type},
        {"EmployeeKey", Int64.Type},
        {"InvoiceNumber", type text},
        {"Quantity", Int64.Type},
        {"UnitPrice", type number},
        {"GrossSales", type number},
        {"DiscountPercent", type number},
        {"DiscountAmount", type number},
        {"NetSales", type number},
        {"Cost", type number},
        {"GrossProfit", type number}
    }),

    // Budget Fact
    BudgetFact = Csv.Document(
        File.Contents("$DataDir\fact_budget.csv"),
        [Delimiter=",", Columns=8, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    BudgetHeaders = Table.PromoteHeaders(BudgetFact, [PromoteAllScalars=true]),
    BudgetTyped = Table.TransformColumnTypes(BudgetHeaders,{
        {"BudgetKey", Int64.Type},
        {"DateKey", Int64.Type},
        {"Year", Int64.Type},
        {"Month", Int64.Type},
        {"Department", type text},
        {"BudgetAmount", type number},
        {"ForecastAmount", type number},
        {"ActualAmount", type number}
    }),

    // Inventory Fact
    InventoryFact = Csv.Document(
        File.Contents("$DataDir\fact_inventory.csv"),
        [Delimiter=",", Columns=9, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    InventoryHeaders = Table.PromoteHeaders(InventoryFact, [PromoteAllScalars=true]),
    InventoryTyped = Table.TransformColumnTypes(InventoryHeaders,{
        {"InventoryKey", Int64.Type},
        {"ProductKey", Int64.Type},
        {"Warehouse", type text},
        {"StockOnHand", Int64.Type},
        {"ReorderPoint", Int64.Type},
        {"MaxStock", Int64.Type},
        {"StockValue", type number},
        {"DaysOnHand", Int64.Type},
        {"LastUpdated", type datetime}
    })
in
    DateTyped
"@

Write-Host "Power BI Setup Script for Bevco Executive Dashboard" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green

# Check if data files exist
if (Test-Path $DataDir) {
    Write-Host "✓ Data directory found: $DataDir" -ForegroundColor Green
    
    $files = @(
        "dim_date.csv",
        "dim_product.csv", 
        "dim_customer.csv",
        "dim_employee.csv",
        "fact_sales.csv",
        "fact_budget.csv",
        "fact_inventory.csv"
    )
    
    foreach ($file in $files) {
        if (Test-Path "$DataDir\$file") {
            Write-Host "✓ Found: $file" -ForegroundColor Green
        } else {
            Write-Host "✗ Missing: $file" -ForegroundColor Red
        }
    }
} else {
    Write-Host "✗ Data directory not found: $DataDir" -ForegroundColor Red
    Write-Host "Please ensure the data files are in the correct location." -ForegroundColor Yellow
}

Write-Host "`nSetup Instructions:" -ForegroundColor Yellow
Write-Host "1. Open Power BI Desktop"
Write-Host "2. Click 'Get Data' > 'Blank Query'"
Write-Host "3. Open Advanced Editor"
Write-Host "4. Copy the M Query from this script"
Write-Host "5. Update file paths to match your environment"
Write-Host "6. Load all tables"
Write-Host "7. Create relationships as defined in the data model"
Write-Host "8. Import DAX measures from DAX_Measures.txt"

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")