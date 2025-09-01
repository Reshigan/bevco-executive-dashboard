# Bevco Executive Dashboard - Full Automation Script
# This script generates data, creates dashboards, and publishes to Power BI Service automatically

param(
    [Parameter(Mandatory=$false)]
    [string]$WorkspaceName = "Bevco Executive Dashboard",
    
    [Parameter(Mandatory=$false)]
    [string]$TenantId = "",
    
    [Parameter(Mandatory=$false)]
    [string]$ClientId = "",
    
    [Parameter(Mandatory=$false)]
    [string]$ClientSecret = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$UseServicePrincipal = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateSampleDashboard = $true
)

# Import required modules
$requiredModules = @(
    "MicrosoftPowerBIMgmt",
    "MicrosoftPowerBIMgmt.Admin", 
    "MicrosoftPowerBIMgmt.Capacities",
    "MicrosoftPowerBIMgmt.Data",
    "MicrosoftPowerBIMgmt.Profile",
    "MicrosoftPowerBIMgmt.Reports",
    "MicrosoftPowerBIMgmt.Workspaces"
)

Write-Host "🚀 Bevco Dashboard - Full Automation" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Function to install and import modules
function Install-PowerBIModules {
    Write-Host "`n📦 Setting up Power BI modules..." -ForegroundColor Yellow
    
    foreach ($module in $requiredModules) {
        if (!(Get-Module -ListAvailable -Name $module)) {
            Write-Host "Installing $module..." -ForegroundColor Gray
            Install-Module -Name $module -Force -AllowClobber -Scope CurrentUser
        }
        Import-Module $module -Force
    }
    Write-Host "✅ Power BI modules ready" -ForegroundColor Green
}

# Function to generate sample data
function New-SampleData {
    Write-Host "`n📊 Generating sample data..." -ForegroundColor Yellow
    
    # Check if Python is available
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
        return $false
    }
    
    # Install required Python packages
    Write-Host "Installing Python dependencies..." -ForegroundColor Gray
    pip install pandas numpy openpyxl --quiet
    
    # Create data directories
    $dataDir = Join-Path (Get-Location).Path "data\master"
    if (!(Test-Path $dataDir)) {
        New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    }
    
    # Run data generation
    $result = python generate_data_standalone.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Sample data generated successfully" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Failed to generate sample data" -ForegroundColor Red
        return $false
    }
}

# Function to create Excel workbook from CSV files
function New-ExcelWorkbook {
    param([string]$DataPath, [string]$OutputPath)
    
    Write-Host "`n📈 Creating Excel workbook..." -ForegroundColor Yellow
    
    try {
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $false
        $excel.DisplayAlerts = $false
        
        $workbook = $excel.Workbooks.Add()
        
        # Remove default sheets except first
        while ($workbook.Worksheets.Count -gt 1) {
            $workbook.Worksheets.Item($workbook.Worksheets.Count).Delete()
        }
        
        $csvFiles = Get-ChildItem -Path $DataPath -Filter "*.csv" | Sort-Object Name
        $sheetIndex = 1
        
        foreach ($csvFile in $csvFiles) {
            Write-Host "  Processing: $($csvFile.Name)" -ForegroundColor Gray
            
            if ($sheetIndex -eq 1) {
                $worksheet = $workbook.Worksheets.Item(1)
            } else {
                $worksheet = $workbook.Worksheets.Add()
            }
            
            # Clean sheet name
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
        $workbook.SaveAs($OutputPath, 51) # xlOpenXMLWorkbook
        $workbook.Close()
        $excel.Quit()
        
        # Clean up COM objects
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
        [System.GC]::Collect()
        [System.GC]::WaitForPendingFinalizers()
        
        Write-Host "✅ Excel workbook created: $OutputPath" -ForegroundColor Green
        return $true
        
    } catch {
        Write-Host "❌ Error creating Excel file: $_" -ForegroundColor Red
        return $false
    }
}

# Function to connect to Power BI Service
function Connect-PowerBIService {
    Write-Host "`n🔐 Connecting to Power BI Service..." -ForegroundColor Yellow
    
    try {
        if ($UseServicePrincipal -and $TenantId -and $ClientId -and $ClientSecret) {
            # Service Principal authentication
            $secureSecret = ConvertTo-SecureString $ClientSecret -AsPlainText -Force
            $credential = New-Object System.Management.Automation.PSCredential($ClientId, $secureSecret)
            
            Connect-PowerBIServiceAccount -ServicePrincipal -Credential $credential -TenantId $TenantId
            Write-Host "✅ Connected using Service Principal" -ForegroundColor Green
        } else {
            # Interactive authentication
            $account = Connect-PowerBIServiceAccount
            Write-Host "✅ Connected as: $($account.UserName)" -ForegroundColor Green
        }
        return $true
    } catch {
        Write-Host "❌ Failed to connect to Power BI Service: $_" -ForegroundColor Red
        return $false
    }
}

# Function to create or get workspace
function New-PowerBIWorkspaceIfNotExists {
    param([string]$Name)
    
    Write-Host "`n🏢 Setting up workspace..." -ForegroundColor Yellow
    
    try {
        $workspace = Get-PowerBIWorkspace -Name $Name -ErrorAction SilentlyContinue
        
        if ($null -eq $workspace) {
            Write-Host "Creating new workspace: $Name" -ForegroundColor Gray
            $workspace = New-PowerBIWorkspace -Name $Name
            Write-Host "✅ Workspace created successfully" -ForegroundColor Green
        } else {
            Write-Host "✅ Using existing workspace: $Name" -ForegroundColor Green
        }
        
        return $workspace
    } catch {
        Write-Host "❌ Failed to create/access workspace: $_" -ForegroundColor Red
        return $null
    }
}

# Function to upload dataset to Power BI
function Publish-DatasetToPowerBI {
    param(
        [string]$FilePath,
        [string]$WorkspaceId,
        [string]$DatasetName
    )
    
    Write-Host "`n📤 Uploading dataset to Power BI..." -ForegroundColor Yellow
    
    try {
        # Upload file to Power BI
        $import = New-PowerBIImport -Path $FilePath -WorkspaceId $WorkspaceId -ConflictAction CreateOrOverwrite
        
        # Wait for import to complete
        $timeout = 300 # 5 minutes
        $elapsed = 0
        
        do {
            Start-Sleep -Seconds 10
            $elapsed += 10
            $importStatus = Get-PowerBIImport -Id $import.Id -WorkspaceId $WorkspaceId
            Write-Host "  Import status: $($importStatus.ImportState)" -ForegroundColor Gray
        } while ($importStatus.ImportState -eq "Publishing" -and $elapsed -lt $timeout)
        
        if ($importStatus.ImportState -eq "Succeeded") {
            Write-Host "✅ Dataset uploaded successfully" -ForegroundColor Green
            return $importStatus
        } else {
            Write-Host "❌ Dataset upload failed: $($importStatus.ImportState)" -ForegroundColor Red
            return $null
        }
    } catch {
        Write-Host "❌ Error uploading dataset: $_" -ForegroundColor Red
        return $null
    }
}

# Function to create dashboard using Power BI REST API
function New-PowerBIDashboard {
    param(
        [string]$WorkspaceId,
        [string]$DashboardName,
        [object]$Dataset
    )
    
    Write-Host "`n🎨 Creating dashboard..." -ForegroundColor Yellow
    
    try {
        # Get access token
        $token = Get-PowerBIAccessToken
        $headers = @{
            'Authorization' = $token.Authorization
            'Content-Type' = 'application/json'
        }
        
        # Create dashboard
        $dashboardBody = @{
            name = $DashboardName
        } | ConvertTo-Json
        
        $dashboardUri = "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/dashboards"
        $dashboard = Invoke-RestMethod -Uri $dashboardUri -Method Post -Headers $headers -Body $dashboardBody
        
        Write-Host "✅ Dashboard created: $DashboardName" -ForegroundColor Green
        
        # Create sample tiles
        if ($CreateSampleDashboard) {
            New-SampleDashboardTiles -WorkspaceId $WorkspaceId -DashboardId $dashboard.id -Dataset $Dataset -Headers $headers
        }
        
        return $dashboard
    } catch {
        Write-Host "❌ Error creating dashboard: $_" -ForegroundColor Red
        return $null
    }
}

# Function to create sample dashboard tiles
function New-SampleDashboardTiles {
    param(
        [string]$WorkspaceId,
        [string]$DashboardId,
        [object]$Dataset,
        [hashtable]$Headers
    )
    
    Write-Host "  Adding sample tiles..." -ForegroundColor Gray
    
    # Sample tiles configuration
    $tiles = @(
        @{
            title = "Total Sales"
            type = "card"
            query = "EVALUATE SUMMARIZE(fact_sales, `"Total Sales`", SUM(fact_sales[NetSales]))"
        },
        @{
            title = "Sales by Region"
            type = "map"
            query = "EVALUATE SUMMARIZE(fact_sales, dim_customer[Region], `"Sales`", SUM(fact_sales[NetSales]))"
        },
        @{
            title = "Monthly Sales Trend"
            type = "lineChart"
            query = "EVALUATE SUMMARIZE(fact_sales, dim_date[MonthName], `"Sales`", SUM(fact_sales[NetSales]))"
        }
    )
    
    foreach ($tile in $tiles) {
        try {
            $tileBody = @{
                title = $tile.title
                embedData = @{
                    datasetId = $Dataset.datasets[0].id
                    config = $tile.query
                }
            } | ConvertTo-Json -Depth 3
            
            $tileUri = "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/dashboards/$DashboardId/tiles"
            Invoke-RestMethod -Uri $tileUri -Method Post -Headers $Headers -Body $tileBody | Out-Null
            
            Write-Host "    ✅ Added tile: $($tile.title)" -ForegroundColor Green
        } catch {
            Write-Host "    ⚠️ Could not add tile: $($tile.title)" -ForegroundColor Yellow
        }
    }
}

# Function to create Power BI report with visualizations
function New-PowerBIReport {
    param(
        [string]$WorkspaceId,
        [string]$DatasetId,
        [string]$ReportName
    )
    
    Write-Host "`n📊 Creating Power BI report..." -ForegroundColor Yellow
    
    try {
        # Get access token
        $token = Get-PowerBIAccessToken
        $headers = @{
            'Authorization' = $token.Authorization
            'Content-Type' = 'application/json'
        }
        
        # Create report from dataset
        $reportBody = @{
            name = $ReportName
            datasetId = $DatasetId
        } | ConvertTo-Json
        
        $reportUri = "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/reports"
        $report = Invoke-RestMethod -Uri $reportUri -Method Post -Headers $headers -Body $reportBody
        
        Write-Host "✅ Report created: $ReportName" -ForegroundColor Green
        return $report
    } catch {
        Write-Host "❌ Error creating report: $_" -ForegroundColor Red
        return $null
    }
}

# Function to set up data refresh
function Set-DataRefresh {
    param(
        [string]$WorkspaceId,
        [string]$DatasetId
    )
    
    Write-Host "`n🔄 Setting up data refresh..." -ForegroundColor Yellow
    
    try {
        # Get access token
        $token = Get-PowerBIAccessToken
        $headers = @{
            'Authorization' = $token.Authorization
            'Content-Type' = 'application/json'
        }
        
        # Configure refresh schedule
        $refreshBody = @{
            value = @(
                @{
                    days = @("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
                    times = @("06:00", "14:00")
                    enabled = $true
                    localTimeZoneId = "South Africa Standard Time"
                }
            )
        } | ConvertTo-Json -Depth 3
        
        $refreshUri = "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/datasets/$DatasetId/refreshSchedule"
        Invoke-RestMethod -Uri $refreshUri -Method Patch -Headers $headers -Body $refreshBody | Out-Null
        
        Write-Host "✅ Data refresh scheduled (Daily at 6 AM and 2 PM)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not set up automatic refresh: $_" -ForegroundColor Yellow
    }
}

# Function to create and publish app
function Publish-PowerBIApp {
    param(
        [string]$WorkspaceId,
        [string]$AppName
    )
    
    Write-Host "`n📱 Publishing Power BI App..." -ForegroundColor Yellow
    
    try {
        # Get access token
        $token = Get-PowerBIAccessToken
        $headers = @{
            'Authorization' = $token.Authorization
            'Content-Type' = 'application/json'
        }
        
        # Create app
        $appBody = @{
            name = $AppName
            description = "Executive dashboard for Bevco South Africa with real-time KPIs and analytics"
            publishMessage = "Initial publication of Bevco Executive Dashboard"
            sourceGroupId = $WorkspaceId
        } | ConvertTo-Json
        
        $appUri = "https://api.powerbi.com/v1.0/myorg/groups/$WorkspaceId/apps"
        $app = Invoke-RestMethod -Uri $appUri -Method Post -Headers $headers -Body $appBody
        
        Write-Host "✅ App published: $AppName" -ForegroundColor Green
        return $app
    } catch {
        Write-Host "⚠️ Could not publish app: $_" -ForegroundColor Yellow
        return $null
    }
}

# Main execution
function Main {
    Write-Host "`n🎯 Starting full automation process..." -ForegroundColor Cyan
    
    # Step 1: Install modules
    Install-PowerBIModules
    
    # Step 2: Generate sample data
    if (!(New-SampleData)) {
        Write-Host "❌ Cannot proceed without sample data" -ForegroundColor Red
        return $false
    }
    
    # Step 3: Create Excel workbook
    $dataPath = Join-Path (Get-Location).Path "data\master"
    $excelPath = Join-Path (Get-Location).Path "BevcoData.xlsx"
    
    if (!(New-ExcelWorkbook -DataPath $dataPath -OutputPath $excelPath)) {
        Write-Host "❌ Cannot proceed without Excel workbook" -ForegroundColor Red
        return $false
    }
    
    # Step 4: Connect to Power BI
    if (!(Connect-PowerBIService)) {
        Write-Host "❌ Cannot proceed without Power BI connection" -ForegroundColor Red
        return $false
    }
    
    # Step 5: Create workspace
    $workspace = New-PowerBIWorkspaceIfNotExists -Name $WorkspaceName
    if ($null -eq $workspace) {
        Write-Host "❌ Cannot proceed without workspace" -ForegroundColor Red
        return $false
    }
    
    # Step 6: Upload dataset
    $import = Publish-DatasetToPowerBI -FilePath $excelPath -WorkspaceId $workspace.Id -DatasetName "Bevco Data"
    if ($null -eq $import) {
        Write-Host "❌ Cannot proceed without dataset" -ForegroundColor Red
        return $false
    }
    
    # Step 7: Create dashboard
    $dashboard = New-PowerBIDashboard -WorkspaceId $workspace.Id -DashboardName "Bevco Executive Dashboard" -Dataset $import
    
    # Step 8: Create report
    if ($import.datasets -and $import.datasets.Count -gt 0) {
        $report = New-PowerBIReport -WorkspaceId $workspace.Id -DatasetId $import.datasets[0].id -ReportName "Bevco Executive Report"
        
        # Step 9: Set up data refresh
        Set-DataRefresh -WorkspaceId $workspace.Id -DatasetId $import.datasets[0].id
    }
    
    # Step 10: Publish app
    $app = Publish-PowerBIApp -WorkspaceId $workspace.Id -AppName "Bevco Executive Dashboard"
    
    # Display results
    Write-Host "`n🎉 AUTOMATION COMPLETE!" -ForegroundColor Green
    Write-Host "========================" -ForegroundColor Green
    Write-Host "Workspace: $($workspace.Name)" -ForegroundColor White
    Write-Host "Workspace URL: https://app.powerbi.com/groups/$($workspace.Id)" -ForegroundColor Cyan
    
    if ($dashboard) {
        Write-Host "Dashboard: $($dashboard.displayName)" -ForegroundColor White
        Write-Host "Dashboard URL: https://app.powerbi.com/groups/$($workspace.Id)/dashboards/$($dashboard.id)" -ForegroundColor Cyan
    }
    
    if ($report) {
        Write-Host "Report: $($report.name)" -ForegroundColor White
        Write-Host "Report URL: https://app.powerbi.com/groups/$($workspace.Id)/reports/$($report.id)" -ForegroundColor Cyan
    }
    
    if ($app) {
        Write-Host "App: $($app.name)" -ForegroundColor White
        Write-Host "App URL: https://app.powerbi.com/groups/$($workspace.Id)/apps/$($app.id)" -ForegroundColor Cyan
    }
    
    Write-Host "`n📊 Sample Data Generated:" -ForegroundColor Yellow
    Write-Host "• 36,400 sales transactions" -ForegroundColor White
    Write-Host "• 724 customers across 9 regions" -ForegroundColor White
    Write-Host "• 339 products from 5 vendors" -ForegroundColor White
    Write-Host "• Complete 6-month business dataset" -ForegroundColor White
    
    Write-Host "`n🚀 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Open the workspace URL above" -ForegroundColor White
    Write-Host "2. Customize your dashboard and reports" -ForegroundColor White
    Write-Host "3. Share with your team" -ForegroundColor White
    Write-Host "4. Set up alerts and subscriptions" -ForegroundColor White
    
    return $true
}

# Execute main function
try {
    $success = Main
    if ($success) {
        Write-Host "`n✅ Full automation completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Automation failed. Check the error messages above." -ForegroundColor Red
    }
} catch {
    Write-Host "`n❌ Unexpected error: $_" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor Gray
} finally {
    Write-Host "`nPress any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}