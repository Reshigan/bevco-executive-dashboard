# Power BI Online Setup Script
# This script helps you set up the Bevco Dashboard directly in Power BI Service (app.powerbi.com)

param(
    [Parameter(Mandatory=$false)]
    [string]$WorkspaceName = "Bevco Executive Dashboard",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateExcelFile = $true,
    
    [Parameter(Mandatory=$false)]
    [switch]$OpenBrowser = $true
)

Write-Host "`n🚀 Bevco Dashboard - Power BI Online Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Function to create Excel file from CSV data
function New-ExcelFromCSV {
    param([string]$DataPath, [string]$OutputPath)
    
    Write-Host "`n📊 Creating Excel workbook from CSV files..." -ForegroundColor Yellow
    
    try {
        # Check if Excel is available
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $false
        $excel.DisplayAlerts = $false
        
        $workbook = $excel.Workbooks.Add()
        
        # Remove default sheets except the first one
        while ($workbook.Worksheets.Count -gt 1) {
            $workbook.Worksheets.Item($workbook.Worksheets.Count).Delete()
        }
        
        $csvFiles = Get-ChildItem -Path $DataPath -Filter "*.csv" | Sort-Object Name
        $sheetIndex = 1
        
        foreach ($csvFile in $csvFiles) {
            Write-Host "   Processing: $($csvFile.Name)" -ForegroundColor Gray
            
            if ($sheetIndex -eq 1) {
                $worksheet = $workbook.Worksheets.Item(1)
            } else {
                $worksheet = $workbook.Worksheets.Add()
            }
            
            # Clean sheet name (Excel has restrictions)
            $sheetName = $csvFile.BaseName -replace '[^\w]', '_'
            if ($sheetName.Length -gt 31) {
                $sheetName = $sheetName.Substring(0, 31)
            }
            $worksheet.Name = $sheetName
            
            # Import CSV data
            $csvData = Import-Csv -Path $csvFile.FullName
            
            if ($csvData.Count -gt 0) {
                # Add headers
                $headers = $csvData[0].PSObject.Properties.Name
                for ($col = 1; $col -le $headers.Count; $col++) {
                    $worksheet.Cells.Item(1, $col) = $headers[$col - 1]
                }
                
                # Add data
                for ($row = 0; $row -lt $csvData.Count; $row++) {
                    for ($col = 1; $col -le $headers.Count; $col++) {
                        $value = $csvData[$row].($headers[$col - 1])
                        $worksheet.Cells.Item($row + 2, $col) = $value
                    }
                }
                
                # Format as table
                $range = $worksheet.Range("A1").Resize($csvData.Count + 1, $headers.Count)
                $table = $worksheet.ListObjects.Add([Microsoft.Office.Interop.Excel.XlListObjectSourceType]::xlSrcRange, $range, $null, [Microsoft.Office.Interop.Excel.XlYesNoGuess]::xlYes)
                $table.Name = $sheetName + "_Table"
                $table.TableStyle = "TableStyleMedium2"
            }
            
            $sheetIndex++
        }
        
        # Save workbook
        $workbook.SaveAs($OutputPath, 51) # 51 = xlOpenXMLWorkbook (.xlsx)
        $workbook.Close()
        $excel.Quit()
        
        # Clean up COM objects
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
        [System.GC]::Collect()
        [System.GC]::WaitForPendingFinalizers()
        
        Write-Host "✅ Excel file created: $OutputPath" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "❌ Error creating Excel file: $_" -ForegroundColor Red
        Write-Host "💡 Tip: Make sure Microsoft Excel is installed" -ForegroundColor Yellow
        return $false
    }
}

# Function to generate Power BI Service instructions
function New-PowerBIInstructions {
    param([string]$ExcelPath, [string]$WorkspaceName)
    
    $instructions = @"
🎯 POWER BI SERVICE SETUP INSTRUCTIONS
=====================================

Your Excel file is ready! Follow these steps to create your dashboard:

📋 STEP-BY-STEP GUIDE:

1️⃣ OPEN POWER BI SERVICE
   • Go to: https://app.powerbi.com
   • Sign in with your organizational account

2️⃣ CREATE WORKSPACE
   • Click "Workspaces" in left navigation
   • Click "Create a workspace"
   • Name: "$WorkspaceName"
   • Click "Save"

3️⃣ UPLOAD EXCEL FILE
   • In your new workspace, click "New" → "Upload a file"
   • Select "Local File"
   • Choose: $ExcelPath
   • Wait for upload to complete

4️⃣ CREATE REPORT
   • Click on the uploaded dataset
   • Click "Create report"
   • You're now in the online report editor!

5️⃣ BUILD YOUR FIRST VISUAL
   • Click "Card" in Visualizations pane
   • Drag "NetSales" from fact_sales to the card
   • Your first KPI is ready!

6️⃣ ADD MORE VISUALS
   • Line Chart: Date (x-axis) + NetSales (values)
   • Map: Region (location) + NetSales (size)
   • Bar Chart: Category (axis) + NetSales (values)

7️⃣ ADD FILTERS
   • Drag "Date" to "Filters on this page"
   • Set as "Date Range" filter
   • Now all visuals will respond to date filtering

8️⃣ SAVE AND SHARE
   • Click "Save" and name your report
   • Click "Share" to invite team members
   • Or create an "App" for wider distribution

🎨 RECOMMENDED VISUALS:
======================

Executive Summary Page:
• 4 KPI Cards: Sales, Profit, Growth %, Customers
• Sales Trend Line Chart
• Regional Performance Map
• Product Category Bar Chart
• Date Range Slicer

Sales Analysis Page:
• Sales by Channel (Pie Chart)
• Top 10 Customers (Table)
• Monthly Performance (Column Chart)
• Product Mix Analysis (Treemap)

💡 PRO TIPS:
============

• Use consistent colors: Primary #003366, Success #28a745
• Add titles to all visuals
• Enable cross-filtering between charts
• Test on mobile using Power BI app
• Set up data alerts on KPI cards
• Create subscriptions for regular reports

🔗 USEFUL LINKS:
================

• Power BI Service: https://app.powerbi.com
• Mobile App: Search "Power BI" in app store
• Documentation: https://docs.microsoft.com/power-bi/
• Community: https://community.powerbi.com

🆘 NEED HELP?
=============

• Check our GitHub: https://github.com/Reshigan/bevco-executive-dashboard
• Power BI Community forums
• Microsoft documentation

🎉 CONGRATULATIONS!
===================

You're now ready to create a world-class executive dashboard!
The sample data includes 36,400 transactions across 6 months,
perfect for demonstrating all the key features.

"@
    
    return $instructions
}

# Main execution
Write-Host "`n🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check if data files exist
$dataPath = Join-Path (Get-Location).Path "data\master"
if (-not (Test-Path $dataPath)) {
    Write-Host "❌ Data files not found at: $dataPath" -ForegroundColor Red
    Write-Host "💡 Please run setup.bat first to generate sample data" -ForegroundColor Yellow
    exit 1
}

$csvFiles = Get-ChildItem -Path $dataPath -Filter "*.csv"
Write-Host "✅ Found $($csvFiles.Count) CSV files" -ForegroundColor Green

# Create Excel file if requested
if ($CreateExcelFile) {
    $excelPath = Join-Path (Get-Location).Path "BevcoData.xlsx"
    
    if (New-ExcelFromCSV -DataPath $dataPath -OutputPath $excelPath) {
        Write-Host "`n📊 Excel file ready for Power BI upload!" -ForegroundColor Green
        Write-Host "📍 Location: $excelPath" -ForegroundColor Cyan
    } else {
        Write-Host "`n⚠️ Excel creation failed. You can still upload CSV files individually." -ForegroundColor Yellow
        $excelPath = "Individual CSV files from: $dataPath"
    }
} else {
    $excelPath = "Individual CSV files from: $dataPath"
}

# Generate instructions
$instructions = New-PowerBIInstructions -ExcelPath $excelPath -WorkspaceName $WorkspaceName

# Save instructions to file
$instructionsPath = Join-Path (Get-Location).Path "PowerBI_Online_Instructions.txt"
$instructions | Out-File -FilePath $instructionsPath -Encoding UTF8

Write-Host "`n📋 Instructions saved to: $instructionsPath" -ForegroundColor Cyan

# Display key information
Write-Host "`n" -NoNewline
Write-Host "🎯 QUICK START SUMMARY" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host "1. Open: " -NoNewline -ForegroundColor White
Write-Host "https://app.powerbi.com" -ForegroundColor Cyan
Write-Host "2. Create workspace: " -NoNewline -ForegroundColor White
Write-Host "$WorkspaceName" -ForegroundColor Cyan
Write-Host "3. Upload file: " -NoNewline -ForegroundColor White
Write-Host "$excelPath" -ForegroundColor Cyan
Write-Host "4. Create report and start building!" -ForegroundColor White

# Open browser if requested
if ($OpenBrowser) {
    Write-Host "`n🌍 Opening Power BI Service in browser..." -ForegroundColor Yellow
    Start-Process "https://app.powerbi.com"
    
    Start-Sleep -Seconds 2
    
    # Open instructions file
    Write-Host "📖 Opening instructions file..." -ForegroundColor Yellow
    Start-Process "notepad.exe" -ArgumentList $instructionsPath
}

# Create web tools server option
Write-Host "`n🛠️ ADDITIONAL TOOLS AVAILABLE:" -ForegroundColor Magenta
Write-Host "• Run 'python scripts\serve_web_tools.py' for web-based tools" -ForegroundColor Gray
Write-Host "• Interactive CSV to Excel converter" -ForegroundColor Gray
Write-Host "• Step-by-step visual guide" -ForegroundColor Gray

Write-Host "`n✨ Setup complete! Happy dashboard building! ✨" -ForegroundColor Green