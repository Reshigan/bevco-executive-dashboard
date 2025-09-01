# Bevco Executive Dashboard - Automated Power BI Deployment Script
# This script automates the deployment process for Power BI Service

param(
    [Parameter(Mandatory=$false)]
    [string]$WorkspaceName = "Bevco Executive Dashboard",
    
    [Parameter(Mandatory=$false)]
    [string]$ReportName = "Bevco_Executive_Dashboard",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateSamplePBIX = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$ValidateOnly = $false
)

# Import required modules
function Import-RequiredModules {
    $modules = @("MicrosoftPowerBIMgmt", "MicrosoftPowerBIMgmt.Workspaces", "MicrosoftPowerBIMgmt.Reports")
    
    foreach ($module in $modules) {
        if (!(Get-Module -ListAvailable -Name $module)) {
            Write-Host "Installing $module..." -ForegroundColor Yellow
            Install-Module -Name $module -Force -AllowClobber -Scope CurrentUser
        }
        Import-Module $module
    }
}

# Function to create PBIX template
function New-PowerBITemplate {
    param([string]$OutputPath)
    
    $templateContent = @"
{
    "version": "1.0",
    "dataModel": {
        "tables": [
            {
                "name": "Dim_Date",
                "columns": [
                    {"name": "DateKey", "dataType": "int64"},
                    {"name": "Date", "dataType": "dateTime"},
                    {"name": "Year", "dataType": "int64"},
                    {"name": "Month", "dataType": "int64"},
                    {"name": "MonthName", "dataType": "string"}
                ]
            },
            {
                "name": "Dim_Product",
                "columns": [
                    {"name": "ProductKey", "dataType": "int64"},
                    {"name": "ProductName", "dataType": "string"},
                    {"name": "Category", "dataType": "string"},
                    {"name": "UnitPrice", "dataType": "decimal"}
                ]
            },
            {
                "name": "Dim_Customer",
                "columns": [
                    {"name": "CustomerKey", "dataType": "int64"},
                    {"name": "CustomerName", "dataType": "string"},
                    {"name": "Region", "dataType": "string"},
                    {"name": "Channel", "dataType": "string"}
                ]
            },
            {
                "name": "Fact_Sales",
                "columns": [
                    {"name": "SalesKey", "dataType": "int64"},
                    {"name": "DateKey", "dataType": "int64"},
                    {"name": "ProductKey", "dataType": "int64"},
                    {"name": "CustomerKey", "dataType": "int64"},
                    {"name": "NetSales", "dataType": "decimal"},
                    {"name": "GrossProfit", "dataType": "decimal"}
                ]
            }
        ],
        "relationships": [
            {
                "name": "Sales_to_Date",
                "fromTable": "Fact_Sales",
                "fromColumn": "DateKey",
                "toTable": "Dim_Date",
                "toColumn": "DateKey"
            },
            {
                "name": "Sales_to_Product",
                "fromTable": "Fact_Sales",
                "fromColumn": "ProductKey",
                "toTable": "Dim_Product",
                "toColumn": "ProductKey"
            },
            {
                "name": "Sales_to_Customer",
                "fromTable": "Fact_Sales",
                "fromColumn": "CustomerKey",
                "toTable": "Dim_Customer",
                "toColumn": "CustomerKey"
            }
        ],
        "measures": [
            {
                "name": "Total Sales",
                "expression": "SUM(Fact_Sales[NetSales])",
                "table": "Fact_Sales"
            },
            {
                "name": "Total Profit",
                "expression": "SUM(Fact_Sales[GrossProfit])",
                "table": "Fact_Sales"
            },
            {
                "name": "Profit Margin %",
                "expression": "DIVIDE([Total Profit], [Total Sales], 0)",
                "table": "Fact_Sales",
                "formatString": "0.00%"
            }
        ]
    }
}
"@
    
    $templateContent | Out-File -FilePath $OutputPath -Encoding UTF8
    Write-Success "Power BI template created at: $OutputPath"
}

# Function to display colored output
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

# Main script
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Bevco Dashboard - Power BI Auto Deploy" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Validate environment
Write-Info "Step 1: Validating environment..."

# Check if running as administrator (recommended)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Warning "Not running as administrator. Some features may be limited."
}

# Check Power BI Desktop installation
$pbiDesktopPath = "${env:ProgramFiles}\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
if (-not (Test-Path $pbiDesktopPath)) {
    $pbiDesktopPath = "${env:ProgramFiles(x86)}\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
}

if (Test-Path $pbiDesktopPath) {
    Write-Success "Power BI Desktop found"
} else {
    Write-Error "Power BI Desktop not installed"
    Write-Info "Download from: https://powerbi.microsoft.com/desktop/"
    if (-not $ValidateOnly) { exit 1 }
}

# Check data files
$dataPath = Join-Path (Get-Location).Path "data\master"
if (Test-Path $dataPath) {
    $csvFiles = Get-ChildItem -Path $dataPath -Filter "*.csv"
    Write-Success "Found $($csvFiles.Count) data files"
} else {
    Write-Error "Data files not found. Run setup.bat first."
    if (-not $ValidateOnly) { exit 1 }
}

if ($ValidateOnly) {
    Write-Success "`nValidation completed!"
    exit 0
}

# Step 2: Install Power BI PowerShell modules
Write-Info "`nStep 2: Setting up Power BI PowerShell modules..."
try {
    Import-RequiredModules
    Write-Success "Power BI modules loaded"
} catch {
    Write-Error "Failed to load Power BI modules: $_"
    exit 1
}

# Step 3: Connect to Power BI Service
Write-Info "`nStep 3: Connecting to Power BI Service..."
try {
    $account = Connect-PowerBIServiceAccount
    Write-Success "Connected as: $($account.UserName)"
} catch {
    Write-Error "Failed to connect to Power BI Service: $_"
    Write-Info "Please ensure you have a valid Power BI Pro or Premium license"
    exit 1
}

# Step 4: Create or get workspace
Write-Info "`nStep 4: Setting up workspace..."
try {
    $workspace = Get-PowerBIWorkspace -Name $WorkspaceName -ErrorAction SilentlyContinue
    
    if ($null -eq $workspace) {
        Write-Info "Creating new workspace: $WorkspaceName"
        $workspace = New-PowerBIWorkspace -Name $WorkspaceName
        Write-Success "Workspace created successfully"
    } else {
        Write-Success "Using existing workspace: $WorkspaceName"
    }
    
    $workspaceId = $workspace.Id
    Write-Info "Workspace ID: $workspaceId"
} catch {
    Write-Error "Failed to create/access workspace: $_"
    exit 1
}

# Step 5: Generate deployment package
Write-Info "`nStep 5: Preparing deployment package..."

$deploymentPath = Join-Path (Get-Location).Path "deployment"
if (-not (Test-Path $deploymentPath)) {
    New-Item -ItemType Directory -Path $deploymentPath | Out-Null
}

# Create import script for Power BI Desktop
$importScript = @'
# Power BI Desktop Import Script
# Run this in Power BI Desktop's DAX Query window

// Step 1: Import Data
// Use Get Data > Folder > Select data\master folder

// Step 2: Create Base Measures
EVALUATE
{
    ("Total Sales", "SUM(Fact_Sales[NetSales])"),
    ("Total Profit", "SUM(Fact_Sales[GrossProfit])"),
    ("Profit Margin %", "DIVIDE([Total Profit], [Total Sales], 0)"),
    ("YoY Growth %", "
        VAR CurrentSales = [Total Sales]
        VAR LastYearSales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Dim_Date[Date]))
        RETURN DIVIDE(CurrentSales - LastYearSales, LastYearSales, 0)
    ")
}
'@

$importScript | Out-File -FilePath (Join-Path $deploymentPath "ImportScript.dax") -Encoding UTF8

# Create RLS script
$rlsScript = @'
// Row-Level Security Configuration

// Regional Security
EVALUATE
SUMMARIZECOLUMNS(
    Dim_Customer[Region],
    "Access Rule", "'" & Dim_Customer[Region] & "' = USERNAME()"
)

// Department Security  
EVALUATE
SUMMARIZECOLUMNS(
    Dim_Employee[Department],
    "Access Rule", "'" & Dim_Employee[Department] & "' = USERPRINCIPALNAME()"
)
'@

$rlsScript | Out-File -FilePath (Join-Path $deploymentPath "RLS_Configuration.dax") -Encoding UTF8

Write-Success "Deployment package created"

# Step 6: Create sample PBIX if requested
if ($CreateSamplePBIX) {
    Write-Info "`nStep 6: Creating sample PBIX template..."
    $templatePath = Join-Path $deploymentPath "BevcoTemplate.json"
    New-PowerBITemplate -OutputPath $templatePath
}

# Step 7: Generate deployment report
Write-Info "`nStep 7: Generating deployment report..."

$deploymentReport = @"
BEVCO EXECUTIVE DASHBOARD - DEPLOYMENT REPORT
============================================
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

ENVIRONMENT DETAILS
------------------
Power BI Account: $($account.UserName)
Workspace: $WorkspaceName
Workspace ID: $workspaceId
Data Location: $dataPath

DEPLOYMENT CHECKLIST
-------------------
[✓] Power BI Desktop installed
[✓] Power BI Service connected
[✓] Workspace configured
[✓] Data files available
[✓] Import scripts generated
[✓] RLS configuration prepared

NEXT STEPS
----------
1. Open Power BI Desktop
2. Import data from: $dataPath
3. Run DAX script from: $deploymentPath\ImportScript.dax
4. Configure RLS using: $deploymentPath\RLS_Configuration.dax
5. Publish to workspace: $WorkspaceName

QUICK COMMANDS
--------------
# To open Power BI Desktop:
Start-Process "$pbiDesktopPath"

# To view workspace in browser:
Start-Process "https://app.powerbi.com/groups/$workspaceId"

# To import all DAX measures:
Copy content from: $(Join-Path (Get-Location).Path "powerbi\datasets\DAX_Measures.txt")

SUPPORT
-------
Documentation: $(Join-Path (Get-Location).Path "documentation")
Issues: https://github.com/Reshigan/bevco-executive-dashboard/issues
"@

$reportPath = Join-Path $deploymentPath "DeploymentReport.txt"
$deploymentReport | Out-File -FilePath $reportPath -Encoding UTF8

Write-Success "Deployment report saved to: $reportPath"

# Step 8: Create Power BI Service configuration
Write-Info "`nStep 8: Preparing Power BI Service configuration..."

$serviceConfig = @{
    "workspace" = @{
        "id" = $workspaceId
        "name" = $WorkspaceName
    }
    "dataset" = @{
        "name" = "$ReportName Dataset"
        "defaultMode" = "Import"
        "refreshSchedule" = @{
            "enabled" = $true
            "days" = @("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
            "times" = @("06:00", "14:00")
            "localTimeZoneId" = "South Africa Standard Time"
        }
    }
    "report" = @{
        "name" = $ReportName
        "pages" = @(
            "Executive Summary",
            "Sales Performance", 
            "Financial Management",
            "Operations",
            "Customer Intelligence",
            "People & Performance"
        )
    }
    "app" = @{
        "name" = "Bevco Executive Dashboard"
        "description" = "Real-time business analytics and KPI monitoring"
        "navigation" = @{
            "Executive" = @("Executive Summary")
            "Sales" = @("Sales Performance", "Customer Intelligence")
            "Finance" = @("Financial Management")
            "Operations" = @("Operations", "People & Performance")
        }
    }
}

$configPath = Join-Path $deploymentPath "PowerBIServiceConfig.json"
$serviceConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $configPath -Encoding UTF8
Write-Success "Service configuration saved"

# Final summary
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Deployment Preparation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nQuick Start Commands:" -ForegroundColor Yellow
Write-Host "1. Open Power BI Desktop:" -ForegroundColor White
Write-Host "   Start-Process `"$pbiDesktopPath`"" -ForegroundColor Gray

Write-Host "`n2. View workspace in browser:" -ForegroundColor White
Write-Host "   Start-Process `"https://app.powerbi.com/groups/$workspaceId`"" -ForegroundColor Gray

Write-Host "`n3. View deployment report:" -ForegroundColor White
Write-Host "   notepad `"$reportPath`"" -ForegroundColor Gray

Write-Host "`nDeployment files created in:" -ForegroundColor Cyan
Write-Host $deploymentPath -ForegroundColor White

# Optionally open Power BI Desktop
$openPBI = Read-Host "`nWould you like to open Power BI Desktop now? (Y/N)"
if ($openPBI -eq 'Y' -or $openPBI -eq 'y') {
    Start-Process $pbiDesktopPath
}

# Optionally open workspace in browser
$openWorkspace = Read-Host "Would you like to open the workspace in your browser? (Y/N)"
if ($openWorkspace -eq 'Y' -or $openWorkspace -eq 'y') {
    Start-Process "https://app.powerbi.com/groups/$workspaceId"
}

Write-Host "`nDeployment preparation completed successfully!" -ForegroundColor Green