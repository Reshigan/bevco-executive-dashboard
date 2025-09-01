# Enhanced Power BI Import Script for Bevco Executive Dashboard
# This script automates the data import process and creates initial visualizations

param(
    [string]$WorkingDirectory = (Get-Location).Path,
    [switch]$CreateSampleReport = $false,
    [switch]$ValidateOnly = $false
)

# Set colors for output
$host.UI.RawUI.ForegroundColor = "White"

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Header
Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "Bevco Executive Dashboard - Power BI Import Tool" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

# Validate environment
Write-Info "Validating environment..."

# Check if Power BI is installed
$powerBIPath = "${env:ProgramFiles}\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
if (-not (Test-Path $powerBIPath)) {
    $powerBIPath = "${env:ProgramFiles(x86)}\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
}

if (Test-Path $powerBIPath) {
    Write-Success "Power BI Desktop found"
} else {
    Write-Error "Power BI Desktop not found. Please install from: https://powerbi.microsoft.com/desktop/"
    exit 1
}

# Check data files
$dataPath = Join-Path $WorkingDirectory "data\master"
$requiredFiles = @(
    "dim_date.csv",
    "dim_product.csv",
    "dim_customer.csv",
    "dim_employee.csv",
    "fact_sales.csv",
    "fact_budget.csv",
    "fact_inventory.csv",
    "dim_kpi_targets.csv"
)

Write-Info "Checking data files..."
$missingFiles = @()

foreach ($file in $requiredFiles) {
    $filePath = Join-Path $dataPath $file
    if (Test-Path $filePath) {
        $fileInfo = Get-Item $filePath
        Write-Success "$file ($('{0:N0}' -f ($fileInfo.Length / 1KB)) KB)"
    } else {
        Write-Error "$file - NOT FOUND"
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Error "`nMissing files detected. Please run setup script first."
    exit 1
}

if ($ValidateOnly) {
    Write-Success "`nValidation completed successfully!"
    exit 0
}

# Generate M Query script
Write-Info "`nGenerating Power Query script..."

$mQueryTemplate = @'
// Bevco Executive Dashboard - Data Import Queries
// Generated: {0}

let
    // Configuration
    DataFolder = "{1}",
    
    // Import Functions
    ImportCSV = (filename as text, types as type) =>
        let
            Source = Csv.Document(
                File.Contents(DataFolder & filename),
                [Delimiter=",", Columns=null, Encoding=1252, QuoteStyle=QuoteStyle.None]
            ),
            PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
            TypedData = Table.TransformColumnTypes(PromotedHeaders, types)
        in
            TypedData,
    
    // Date Dimension
    Dim_Date = ImportCSV("dim_date.csv", {{
        {{"DateKey", Int64.Type}}, {{"Date", type date}}, {{"Year", Int64.Type}},
        {{"Quarter", Int64.Type}}, {{"Month", Int64.Type}}, {{"MonthName", type text}},
        {{"Week", Int64.Type}}, {{"DayOfWeek", Int64.Type}}, {{"DayName", type text}},
        {{"DayOfMonth", Int64.Type}}, {{"DayOfYear", Int64.Type}}, {{"IsWeekend", Int64.Type}},
        {{"IsHoliday", Int64.Type}}, {{"FiscalYear", Int64.Type}}, {{"FiscalQuarter", Int64.Type}},
        {{"FiscalMonth", Int64.Type}}
    }}),
    
    // Product Dimension
    Dim_Product = ImportCSV("dim_product.csv", {{
        {{"ProductKey", Int64.Type}}, {{"SKU", type text}}, {{"ProductName", type text}},
        {{"Vendor", type text}}, {{"Category", type text}}, {{"SubCategory", type text}},
        {{"Brand", type text}}, {{"PackSize", type text}}, {{"UnitCost", type number}},
        {{"UnitPrice", type number}}, {{"LaunchDate", type date}}, {{"Status", type text}}
    }}),
    
    // Customer Dimension
    Dim_Customer = ImportCSV("dim_customer.csv", {{
        {{"CustomerKey", Int64.Type}}, {{"CustomerCode", type text}}, {{"CustomerName", type text}},
        {{"Channel", type text}}, {{"CustomerType", type text}}, {{"Region", type text}},
        {{"Province", type text}}, {{"City", type text}}, {{"CreditLimit", Int64.Type}},
        {{"PaymentTerms", Int64.Type}}, {{"Status", type text}}, {{"OnboardingDate", type date}}
    }}),
    
    // Employee Dimension
    Dim_Employee = ImportCSV("dim_employee.csv", {{
        {{"EmployeeKey", Int64.Type}}, {{"EmployeeCode", type text}}, {{"Name", type text}},
        {{"Position", type text}}, {{"Department", type text}}, {{"ReportsTo", Int64.Type}},
        {{"HireDate", type date}}, {{"Salary", Int64.Type}}, {{"EmploymentType", type text}}
    }}),
    
    // Sales Facts
    Fact_Sales = ImportCSV("fact_sales.csv", {{
        {{"SalesKey", Int64.Type}}, {{"DateKey", Int64.Type}}, {{"ProductKey", Int64.Type}},
        {{"CustomerKey", Int64.Type}}, {{"EmployeeKey", Int64.Type}}, {{"InvoiceNumber", type text}},
        {{"Quantity", Int64.Type}}, {{"UnitPrice", type number}}, {{"GrossSales", type number}},
        {{"DiscountPercent", type number}}, {{"DiscountAmount", type number}}, {{"NetSales", type number}},
        {{"Cost", type number}}, {{"GrossProfit", type number}}
    }}),
    
    // Budget Facts
    Fact_Budget = ImportCSV("fact_budget.csv", {{
        {{"BudgetKey", Int64.Type}}, {{"DateKey", Int64.Type}}, {{"Year", Int64.Type}},
        {{"Month", Int64.Type}}, {{"Department", type text}}, {{"BudgetAmount", type number}},
        {{"ForecastAmount", type number}}, {{"ActualAmount", type number}}
    }}),
    
    // Inventory Facts
    Fact_Inventory = ImportCSV("fact_inventory.csv", {{
        {{"InventoryKey", Int64.Type}}, {{"ProductKey", Int64.Type}}, {{"Warehouse", type text}},
        {{"StockOnHand", Int64.Type}}, {{"ReorderPoint", Int64.Type}}, {{"MaxStock", Int64.Type}},
        {{"StockValue", type number}}, {{"DaysOnHand", Int64.Type}}, {{"LastUpdated", type datetime}}
    }}),
    
    // KPI Targets
    Dim_KPI_Targets = ImportCSV("dim_kpi_targets.csv", {{
        {{"KPIName", type text}}, {{"Target", type number}}, {{"Unit", type text}},
        {{"Frequency", type text}}
    }})
in
    Dim_Date
'@ -f (Get-Date).ToString("yyyy-MM-dd HH:mm:ss"), $dataPath.Replace("\", "\\") + "\\"

# Save M Query to file
$mQueryPath = Join-Path $WorkingDirectory "powerbi\datasets\DataImportQuery.pq"
$mQueryTemplate | Out-File -FilePath $mQueryPath -Encoding UTF8
Write-Success "Power Query script saved to: $mQueryPath"

# Create sample PBIX template
if ($CreateSampleReport) {
    Write-Info "`nCreating sample Power BI template..."
    
    # This would require Power BI API or COM automation
    # For now, we'll create instructions
    $templateInstructions = @'
# Power BI Report Template Instructions

## Data Import Steps:
1. Open Power BI Desktop
2. Click "Get Data" > "Blank Query"
3. Open Advanced Editor
4. Copy the contents of DataImportQuery.pq
5. Update the DataFolder path to match your environment
6. Click "Done" and then "Close & Apply"

## Create Relationships:
1. Go to Model view
2. Create the following relationships:
   - Fact_Sales[DateKey] → Dim_Date[DateKey]
   - Fact_Sales[ProductKey] → Dim_Product[ProductKey]
   - Fact_Sales[CustomerKey] → Dim_Customer[CustomerKey]
   - Fact_Sales[EmployeeKey] → Dim_Employee[EmployeeKey]
   - Fact_Budget[DateKey] → Dim_Date[DateKey]
   - Fact_Inventory[ProductKey] → Dim_Product[ProductKey]

## Import DAX Measures:
1. Go to Data view
2. Create a new measure
3. Copy measures from DAX_Measures.txt
4. Organize measures into folders

## Create Visualizations:
1. Follow the Dashboard_Structure.md guide
2. Start with Executive Summary page
3. Add KPI cards, charts, and slicers
4. Apply Bevco color theme
'@
    
    $templatePath = Join-Path $WorkingDirectory "powerbi\reports\TEMPLATE_INSTRUCTIONS.md"
    $templateInstructions | Out-File -FilePath $templatePath -Encoding UTF8
    Write-Success "Template instructions saved to: $templatePath"
}

# Generate automation script for measure creation
Write-Info "`nGenerating DAX measure import script..."

$daxScriptPath = Join-Path $WorkingDirectory "powerbi\datasets\ImportDAXMeasures.csx"
$daxScript = @'
// C# Script for Tabular Editor to import all DAX measures
// Usage: Open Tabular Editor, connect to your model, and run this script

var measuresFile = @"{0}\DAX_Measures.txt";
var measures = System.IO.File.ReadAllText(measuresFile);

// Parse measures (simplified - in production use proper parsing)
var measureDefinitions = measures.Split(new[] { "\r\n\r\n" }, StringSplitOptions.RemoveEmptyEntries);

foreach(var measureDef in measureDefinitions)
{
    if(measureDef.Contains(" = ") && !measureDef.StartsWith("//"))
    {
        var parts = measureDef.Split(new[] { " = " }, 2, StringSplitOptions.None);
        if(parts.Length == 2)
        {
            var measureName = parts[0].Trim();
            var measureExpression = parts[1].Trim();
            
            // Skip section headers
            if(!measureName.Contains("=") && !measureExpression.StartsWith("="))
            {
                // Create measure in the model
                var measure = Model.Tables["Fact_Sales"].AddMeasure(measureName, measureExpression);
                
                // Assign to appropriate folder based on name
                if(measureName.Contains("Sales") || measureName.Contains("Revenue"))
                    measure.DisplayFolder = "Sales Metrics";
                else if(measureName.Contains("Budget") || measureName.Contains("Forecast"))
                    measure.DisplayFolder = "Financial Metrics";
                else if(measureName.Contains("Customer"))
                    measure.DisplayFolder = "Customer Metrics";
                else if(measureName.Contains("Inventory") || measureName.Contains("Stock"))
                    measure.DisplayFolder = "Inventory Metrics";
                else if(measureName.Contains("Employee") || measureName.Contains("HR"))
                    measure.DisplayFolder = "HR Metrics";
                else
                    measure.DisplayFolder = "Other Metrics";
            }
        }
    }
}

Info("Measures imported successfully!");
'@ -f ($WorkingDirectory -replace '\\', '\\')

$daxScript | Out-File -FilePath $daxScriptPath -Encoding UTF8
Write-Success "DAX import script saved to: $daxScriptPath"

# Create quick start guide
$quickStartPath = Join-Path $WorkingDirectory "QUICKSTART.md"
$quickStart = @"
# Bevco Executive Dashboard - Quick Start Guide

## 1. Prerequisites
- ✓ Power BI Desktop installed
- ✓ Data files generated
- ✓ Scripts prepared

## 2. Import Data (5 minutes)
1. Open Power BI Desktop
2. Get Data > Blank Query > Advanced Editor
3. Copy contents from: \powerbi\datasets\DataImportQuery.pq
4. Update DataFolder path if needed
5. Close & Apply

## 3. Create Relationships (2 minutes)
In Model view, create these relationships:
- Fact_Sales → Dim_Date (DateKey)
- Fact_Sales → Dim_Product (ProductKey)
- Fact_Sales → Dim_Customer (CustomerKey)
- Fact_Sales → Dim_Employee (EmployeeKey)
- Fact_Budget → Dim_Date (DateKey)
- Fact_Inventory → Dim_Product (ProductKey)

## 4. Import Measures (5 minutes)
Option A - Manual:
1. Create new measure
2. Copy from DAX_Measures.txt
3. Organize into folders

Option B - Automated (requires Tabular Editor):
1. Download Tabular Editor
2. Connect to your model
3. Run ImportDAXMeasures.csx

## 5. Create First Visual (2 minutes)
1. Insert Card visual
2. Add "Total Net Sales" measure
3. Format with Bevco blue (#003366)

## 6. Build Executive Dashboard (30 minutes)
Follow the guide in Dashboard_Structure.md

## Need Help?
- User Guide: /documentation/user-guides/
- Technical Docs: /documentation/technical/
- Sample Data: /data/master/
"@

$quickStart | Out-File -FilePath $quickStartPath -Encoding UTF8
Write-Success "Quick start guide created"

# Summary
Write-Host "`n================================================" -ForegroundColor Green
Write-Host "Import preparation completed successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Open Power BI Desktop" -ForegroundColor White
Write-Host "2. Follow the QUICKSTART.md guide" -ForegroundColor White
Write-Host "3. Import data using the generated query" -ForegroundColor White
Write-Host "4. Create relationships and measures" -ForegroundColor White
Write-Host "5. Build your dashboards" -ForegroundColor White

Write-Host "`nKey Files Generated:" -ForegroundColor Cyan
Write-Host "- Power Query: \powerbi\datasets\DataImportQuery.pq" -ForegroundColor White
Write-Host "- DAX Script: \powerbi\datasets\ImportDAXMeasures.csx" -ForegroundColor White
Write-Host "- Quick Start: \QUICKSTART.md" -ForegroundColor White

if (-not $CreateSampleReport) {
    Write-Host "`nTip: Run with -CreateSampleReport flag for additional templates" -ForegroundColor Gray
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")