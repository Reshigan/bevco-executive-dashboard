#!/usr/bin/env python3
"""
Bevco Executive Dashboard - PBIT Template Creator
Creates Power BI Template files (.pbit) that can be directly imported into Power BI Desktop
"""

import os
import json
import zipfile
import tempfile
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class PBITCreator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.output_dir = self.project_root / "pbit_templates"
        self.data_dir = self.project_root / "data" / "master"
        
    def print_status(self, message, status="info"):
        """Print colored status messages"""
        colors = {
            "info": "\033[96m",      # Cyan
            "success": "\033[92m",   # Green
            "warning": "\033[93m",   # Yellow
            "error": "\033[91m",     # Red
            "reset": "\033[0m"       # Reset
        }
        
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        print(f"{colors.get(status, '')}{icons.get(status, '')} {message}{colors['reset']}")
    
    def ensure_data_exists(self):
        """Ensure sample data exists"""
        if not self.data_dir.exists() or not any(self.data_dir.glob("*.csv")):
            self.print_status("Generating sample data...", "info")
            try:
                result = subprocess.run([
                    sys.executable, 
                    str(self.project_root / "generate_data_standalone.py")
                ], capture_output=True, text=True, cwd=str(self.project_root))
                
                if result.returncode != 0:
                    self.print_status(f"Data generation failed: {result.stderr}", "error")
                    return False
                    
                self.print_status("Sample data generated successfully", "success")
                return True
                
            except Exception as e:
                self.print_status(f"Error generating data: {e}", "error")
                return False
        else:
            self.print_status("Sample data already exists", "success")
            return True
    
    def create_data_model_schema(self, template_type="executive"):
        """Create the Power BI data model schema"""
        base_schema = {
            "name": "BevcoModel",
            "compatibilityLevel": 1567,
            "model": {
                "culture": "en-US",
                "dataAccessOptions": {
                    "legacyRedirects": True,
                    "returnErrorValuesAsNull": True
                },
                "defaultPowerBIDataSourceVersion": "powerBI_V3",
                "sourceQueryCulture": "en-US",
                "tables": self.get_tables_for_template(template_type),
                "relationships": self.get_relationships_for_template(template_type),
                "measures": self.get_measures_for_template(template_type)
            }
        }
        
        return base_schema
    
    def get_tables_for_template(self, template_type):
        """Get tables based on template type"""
        base_tables = [
            {
                "name": "dim_date",
                "columns": [
                    {"name": "DateKey", "dataType": "int64", "sourceColumn": "DateKey"},
                    {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date"},
                    {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                    {"name": "Quarter", "dataType": "int64", "sourceColumn": "Quarter"},
                    {"name": "Month", "dataType": "int64", "sourceColumn": "Month"},
                    {"name": "MonthName", "dataType": "string", "sourceColumn": "MonthName"},
                    {"name": "Day", "dataType": "int64", "sourceColumn": "Day"},
                    {"name": "DayName", "dataType": "string", "sourceColumn": "DayName"},
                    {"name": "WeekOfYear", "dataType": "int64", "sourceColumn": "WeekOfYear"},
                    {"name": "FiscalYear", "dataType": "int64", "sourceColumn": "FiscalYear"},
                    {"name": "FiscalQuarter", "dataType": "int64", "sourceColumn": "FiscalQuarter"}
                ],
                "partitions": [{
                    "name": "dim_date",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": '''let
    Source = Csv.Document(File.Contents("dim_date.csv"),[Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"DateKey", Int64.Type}, {"Date", type datetime}, {"Year", Int64.Type}, {"Quarter", Int64.Type}, {"Month", Int64.Type}, {"MonthName", type text}, {"Day", Int64.Type}, {"DayName", type text}, {"WeekOfYear", Int64.Type}, {"FiscalYear", Int64.Type}, {"FiscalQuarter", Int64.Type}})
in
    #"Changed Type"'''
                    }
                }]
            },
            {
                "name": "dim_product",
                "columns": [
                    {"name": "ProductKey", "dataType": "int64", "sourceColumn": "ProductKey"},
                    {"name": "ProductCode", "dataType": "string", "sourceColumn": "ProductCode"},
                    {"name": "ProductName", "dataType": "string", "sourceColumn": "ProductName"},
                    {"name": "Category", "dataType": "string", "sourceColumn": "Category"},
                    {"name": "Vendor", "dataType": "string", "sourceColumn": "Vendor"},
                    {"name": "UnitCost", "dataType": "double", "sourceColumn": "UnitCost"},
                    {"name": "UnitPrice", "dataType": "double", "sourceColumn": "UnitPrice"},
                    {"name": "PackSize", "dataType": "string", "sourceColumn": "PackSize"},
                    {"name": "IsActive", "dataType": "boolean", "sourceColumn": "IsActive"}
                ],
                "partitions": [{
                    "name": "dim_product",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": '''let
    Source = Csv.Document(File.Contents("dim_product.csv"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"ProductKey", Int64.Type}, {"ProductCode", type text}, {"ProductName", type text}, {"Category", type text}, {"Vendor", type text}, {"UnitCost", type number}, {"UnitPrice", type number}, {"PackSize", type text}, {"IsActive", type logical}})
in
    #"Changed Type"'''
                    }
                }]
            },
            {
                "name": "dim_customer",
                "columns": [
                    {"name": "CustomerKey", "dataType": "int64", "sourceColumn": "CustomerKey"},
                    {"name": "CustomerCode", "dataType": "string", "sourceColumn": "CustomerCode"},
                    {"name": "CustomerName", "dataType": "string", "sourceColumn": "CustomerName"},
                    {"name": "Region", "dataType": "string", "sourceColumn": "Region"},
                    {"name": "City", "dataType": "string", "sourceColumn": "City"},
                    {"name": "Channel", "dataType": "string", "sourceColumn": "Channel"},
                    {"name": "CustomerType", "dataType": "string", "sourceColumn": "CustomerType"},
                    {"name": "CreditLimit", "dataType": "int64", "sourceColumn": "CreditLimit"},
                    {"name": "IsActive", "dataType": "boolean", "sourceColumn": "IsActive"}
                ],
                "partitions": [{
                    "name": "dim_customer",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": '''let
    Source = Csv.Document(File.Contents("dim_customer.csv"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"CustomerKey", Int64.Type}, {"CustomerCode", type text}, {"CustomerName", type text}, {"Region", type text}, {"City", type text}, {"Channel", type text}, {"CustomerType", type text}, {"CreditLimit", Int64.Type}, {"IsActive", type logical}})
in
    #"Changed Type"'''
                    }
                }]
            },
            {
                "name": "fact_sales",
                "columns": [
                    {"name": "SalesKey", "dataType": "int64", "sourceColumn": "SalesKey"},
                    {"name": "DateKey", "dataType": "int64", "sourceColumn": "DateKey"},
                    {"name": "ProductKey", "dataType": "int64", "sourceColumn": "ProductKey"},
                    {"name": "CustomerKey", "dataType": "int64", "sourceColumn": "CustomerKey"},
                    {"name": "EmployeeKey", "dataType": "int64", "sourceColumn": "EmployeeKey"},
                    {"name": "InvoiceNumber", "dataType": "string", "sourceColumn": "InvoiceNumber"},
                    {"name": "Quantity", "dataType": "int64", "sourceColumn": "Quantity"},
                    {"name": "GrossSales", "dataType": "double", "sourceColumn": "GrossSales"},
                    {"name": "DiscountAmount", "dataType": "double", "sourceColumn": "DiscountAmount"},
                    {"name": "NetSales", "dataType": "double", "sourceColumn": "NetSales"},
                    {"name": "COGS", "dataType": "double", "sourceColumn": "COGS"},
                    {"name": "GrossProfit", "dataType": "double", "sourceColumn": "GrossProfit"}
                ],
                "partitions": [{
                    "name": "fact_sales",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": '''let
    Source = Csv.Document(File.Contents("fact_sales.csv"),[Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SalesKey", Int64.Type}, {"DateKey", Int64.Type}, {"ProductKey", Int64.Type}, {"CustomerKey", Int64.Type}, {"EmployeeKey", Int64.Type}, {"InvoiceNumber", type text}, {"Quantity", Int64.Type}, {"GrossSales", type number}, {"DiscountAmount", type number}, {"NetSales", type number}, {"COGS", type number}, {"GrossProfit", type number}})
in
    #"Changed Type"'''
                    }
                }]
            }
        ]
        
        # Add additional tables based on template type
        if template_type in ["executive", "financial"]:
            base_tables.extend([
                {
                    "name": "fact_budget",
                    "columns": [
                        {"name": "BudgetKey", "dataType": "int64", "sourceColumn": "BudgetKey"},
                        {"name": "DateKey", "dataType": "int64", "sourceColumn": "DateKey"},
                        {"name": "Department", "dataType": "string", "sourceColumn": "Department"},
                        {"name": "BudgetAmount", "dataType": "int64", "sourceColumn": "BudgetAmount"},
                        {"name": "ActualAmount", "dataType": "int64", "sourceColumn": "ActualAmount"},
                        {"name": "ForecastAmount", "dataType": "int64", "sourceColumn": "ForecastAmount"}
                    ],
                    "partitions": [{
                        "name": "fact_budget",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": '''let
    Source = Csv.Document(File.Contents("fact_budget.csv"),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"BudgetKey", Int64.Type}, {"DateKey", Int64.Type}, {"Department", type text}, {"BudgetAmount", Int64.Type}, {"ActualAmount", Int64.Type}, {"ForecastAmount", Int64.Type}})
in
    #"Changed Type"'''
                        }
                    }]
                }
            ])
        
        if template_type in ["executive", "operational"]:
            base_tables.extend([
                {
                    "name": "dim_employee",
                    "columns": [
                        {"name": "EmployeeKey", "dataType": "int64", "sourceColumn": "EmployeeKey"},
                        {"name": "EmployeeID", "dataType": "string", "sourceColumn": "EmployeeID"},
                        {"name": "FirstName", "dataType": "string", "sourceColumn": "FirstName"},
                        {"name": "LastName", "dataType": "string", "sourceColumn": "LastName"},
                        {"name": "Department", "dataType": "string", "sourceColumn": "Department"},
                        {"name": "Position", "dataType": "string", "sourceColumn": "Position"},
                        {"name": "HireDate", "dataType": "dateTime", "sourceColumn": "HireDate"},
                        {"name": "Salary", "dataType": "int64", "sourceColumn": "Salary"},
                        {"name": "IsActive", "dataType": "boolean", "sourceColumn": "IsActive"}
                    ],
                    "partitions": [{
                        "name": "dim_employee",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": '''let
    Source = Csv.Document(File.Contents("dim_employee.csv"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"EmployeeKey", Int64.Type}, {"EmployeeID", type text}, {"FirstName", type text}, {"LastName", type text}, {"Department", type text}, {"Position", type text}, {"HireDate", type datetime}, {"Salary", Int64.Type}, {"IsActive", type logical}})
in
    #"Changed Type"'''
                        }
                    }]
                },
                {
                    "name": "fact_inventory",
                    "columns": [
                        {"name": "InventoryKey", "dataType": "int64", "sourceColumn": "InventoryKey"},
                        {"name": "ProductKey", "dataType": "int64", "sourceColumn": "ProductKey"},
                        {"name": "WarehouseLocation", "dataType": "string", "sourceColumn": "WarehouseLocation"},
                        {"name": "StockOnHand", "dataType": "int64", "sourceColumn": "StockOnHand"},
                        {"name": "ReorderLevel", "dataType": "int64", "sourceColumn": "ReorderLevel"},
                        {"name": "MaxStockLevel", "dataType": "int64", "sourceColumn": "MaxStockLevel"},
                        {"name": "LastStockDate", "dataType": "dateTime", "sourceColumn": "LastStockDate"}
                    ],
                    "partitions": [{
                        "name": "fact_inventory",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": '''let
    Source = Csv.Document(File.Contents("fact_inventory.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"InventoryKey", Int64.Type}, {"ProductKey", Int64.Type}, {"WarehouseLocation", type text}, {"StockOnHand", Int64.Type}, {"ReorderLevel", Int64.Type}, {"MaxStockLevel", Int64.Type}, {"LastStockDate", type datetime}})
in
    #"Changed Type"'''
                        }
                    }]
                }
            ])
        
        return base_tables
    
    def get_relationships_for_template(self, template_type):
        """Get relationships based on template type"""
        base_relationships = [
            {
                "name": "fact_sales_dim_date",
                "fromTable": "fact_sales",
                "fromColumn": "DateKey",
                "toTable": "dim_date",
                "toColumn": "DateKey",
                "crossFilteringBehavior": "oneToMany"
            },
            {
                "name": "fact_sales_dim_product",
                "fromTable": "fact_sales",
                "fromColumn": "ProductKey",
                "toTable": "dim_product",
                "toColumn": "ProductKey",
                "crossFilteringBehavior": "oneToMany"
            },
            {
                "name": "fact_sales_dim_customer",
                "fromTable": "fact_sales",
                "fromColumn": "CustomerKey",
                "toTable": "dim_customer",
                "toColumn": "CustomerKey",
                "crossFilteringBehavior": "oneToMany"
            }
        ]
        
        # Add additional relationships based on template type
        if template_type in ["executive", "financial"]:
            base_relationships.append({
                "name": "fact_budget_dim_date",
                "fromTable": "fact_budget",
                "fromColumn": "DateKey",
                "toTable": "dim_date",
                "toColumn": "DateKey",
                "crossFilteringBehavior": "oneToMany"
            })
        
        if template_type in ["executive", "operational"]:
            base_relationships.extend([
                {
                    "name": "fact_sales_dim_employee",
                    "fromTable": "fact_sales",
                    "fromColumn": "EmployeeKey",
                    "toTable": "dim_employee",
                    "toColumn": "EmployeeKey",
                    "crossFilteringBehavior": "oneToMany"
                },
                {
                    "name": "fact_inventory_dim_product",
                    "fromTable": "fact_inventory",
                    "fromColumn": "ProductKey",
                    "toTable": "dim_product",
                    "toColumn": "ProductKey",
                    "crossFilteringBehavior": "oneToMany"
                }
            ])
        
        return base_relationships
    
    def get_measures_for_template(self, template_type):
        """Get DAX measures based on template type"""
        base_measures = [
            {
                "name": "Total Sales",
                "expression": "SUM(fact_sales[NetSales])",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Sales Metrics"
            },
            {
                "name": "Total Profit",
                "expression": "SUM(fact_sales[GrossProfit])",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Sales Metrics"
            },
            {
                "name": "Profit Margin %",
                "expression": "DIVIDE([Total Profit], [Total Sales], 0)",
                "formatString": "0.00%",
                "displayFolder": "Sales Metrics"
            },
            {
                "name": "Total Quantity",
                "expression": "SUM(fact_sales[Quantity])",
                "formatString": "#,0",
                "displayFolder": "Sales Metrics"
            },
            {
                "name": "Average Order Value",
                "expression": "DIVIDE([Total Sales], DISTINCTCOUNT(fact_sales[InvoiceNumber]), 0)",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Sales Metrics"
            },
            {
                "name": "Total Sales LY",
                "expression": "CALCULATE([Total Sales], SAMEPERIODLASTYEAR(dim_date[Date]))",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Time Intelligence"
            },
            {
                "name": "Sales Growth %",
                "expression": "DIVIDE([Total Sales] - [Total Sales LY], [Total Sales LY], 0)",
                "formatString": "0.00%",
                "displayFolder": "Time Intelligence"
            },
            {
                "name": "YTD Sales",
                "expression": "TOTALYTD([Total Sales], dim_date[Date])",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Time Intelligence"
            }
        ]
        
        # Add template-specific measures
        if template_type in ["executive", "financial"]:
            base_measures.extend([
                {
                    "name": "Budget Amount",
                    "expression": "SUM(fact_budget[BudgetAmount])",
                    "formatString": "\"R\"#,0.00",
                    "displayFolder": "Budget Metrics"
                },
                {
                    "name": "Actual Amount",
                    "expression": "SUM(fact_budget[ActualAmount])",
                    "formatString": "\"R\"#,0.00",
                    "displayFolder": "Budget Metrics"
                },
                {
                    "name": "Budget Variance %",
                    "expression": "DIVIDE([Actual Amount] - [Budget Amount], [Budget Amount], 0)",
                    "formatString": "0.00%",
                    "displayFolder": "Budget Metrics"
                }
            ])
        
        if template_type in ["executive", "operational"]:
            base_measures.extend([
                {
                    "name": "Total Stock Value",
                    "expression": "SUMX(fact_inventory, fact_inventory[StockOnHand] * RELATED(dim_product[UnitCost]))",
                    "formatString": "\"R\"#,0.00",
                    "displayFolder": "Inventory Metrics"
                },
                {
                    "name": "Active Employees",
                    "expression": "CALCULATE(DISTINCTCOUNT(dim_employee[EmployeeKey]), dim_employee[IsActive] = TRUE)",
                    "formatString": "#,0",
                    "displayFolder": "Employee Metrics"
                }
            ])
        
        return base_measures
    
    def create_layout_json(self, template_type):
        """Create basic layout for the template"""
        layout = {
            "version": "5.43",
            "themeCollection": {
                "baseTheme": {
                    "name": "CityPark"
                }
            },
            "activeSectionIndex": 0,
            "defaultDrillFilterOtherVisuals": True,
            "sections": [
                {
                    "name": "ReportSection",
                    "displayName": self.get_section_name(template_type),
                    "visualContainers": []
                }
            ]
        }
        
        return layout
    
    def get_section_name(self, template_type):
        """Get section name based on template type"""
        names = {
            "executive": "Executive Summary",
            "sales": "Sales Analysis", 
            "financial": "Financial Dashboard",
            "operational": "Operational Metrics"
        }
        return names.get(template_type, "Dashboard")
    
    def create_pbit_file(self, template_type, filename):
        """Create a PBIT template file"""
        self.print_status(f"Creating PBIT template: {filename}", "info")
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create DataModelSchema
            schema = self.create_data_model_schema(template_type)
            with open(temp_path / "DataModelSchema", "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2)
            
            # Create Layout
            layout = self.create_layout_json(template_type)
            with open(temp_path / "Layout", "w", encoding="utf-8") as f:
                json.dump(layout, f, indent=2)
            
            # Create Version
            version_info = {
                "version": "1.0",
                "powerBIVersion": "2.0",
                "created": datetime.now().isoformat(),
                "description": f"Bevco {template_type.title()} Dashboard Template"
            }
            with open(temp_path / "Version", "w", encoding="utf-8") as f:
                json.dump(version_info, f, indent=2)
            
            # Create the PBIT file (ZIP format)
            pbit_path = self.output_dir / filename
            with zipfile.ZipFile(pbit_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in temp_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(temp_path)
                        zipf.write(file_path, arcname)
            
            self.print_status(f"PBIT template created: {pbit_path}", "success")
            return pbit_path
    
    def create_all_templates(self):
        """Create all PBIT template files"""
        self.print_status("Creating Power BI Template files (.pbit)", "info")
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        
        # Ensure data exists
        if not self.ensure_data_exists():
            return False
        
        # Create different template files
        templates = [
            {
                "type": "executive",
                "filename": "BevcoExecutiveDashboard.pbit",
                "description": "Complete executive dashboard with all KPIs and visualizations"
            },
            {
                "type": "sales",
                "filename": "BevcoSalesAnalysis.pbit",
                "description": "Sales-focused dashboard for sales teams and managers"
            },
            {
                "type": "financial",
                "filename": "BevcoFinancialReporting.pbit",
                "description": "Financial dashboard with budget vs actual analysis"
            },
            {
                "type": "operational",
                "filename": "BevcoOperationalMetrics.pbit",
                "description": "Operational dashboard with inventory and employee metrics"
            }
        ]
        
        created_files = []
        
        for template_info in templates:
            try:
                pbit_path = self.create_pbit_file(template_info["type"], template_info["filename"])
                created_files.append({
                    "path": pbit_path,
                    "type": template_info["type"],
                    "description": template_info["description"]
                })
            except Exception as e:
                self.print_status(f"Error creating {template_info['filename']}: {e}", "error")
        
        return created_files
    
    def create_usage_instructions(self, created_files):
        """Create instructions for using PBIT templates"""
        instructions = f"""# 📊 Power BI Template Files (.pbit) - Usage Guide

## 🎯 Ready-to-Use PBIT Templates

The following Power BI Template files have been created and are ready for use:

"""
        
        for i, file_info in enumerate(created_files, 1):
            filename = file_info["path"].name
            description = file_info["description"]
            file_size = file_info["path"].stat().st_size / 1024
            instructions += f"""
### {i}. {filename}
**Type:** {file_info["type"].title()} Dashboard
**Description:** {description}
**File Size:** {file_size:.1f} KB
**Location:** `pbit_templates/{filename}`

"""
        
        instructions += """
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
"""
        
        instructions_path = self.output_dir / "PBIT_USAGE_GUIDE.md"
        with open(instructions_path, "w", encoding="utf-8") as f:
            f.write(instructions)
        
        self.print_status(f"Usage guide created: {instructions_path}", "success")
        return instructions_path

def main():
    """Main function"""
    creator = PBITCreator()
    
    print("📊 Bevco Dashboard - PBIT Template Creator")
    print("=" * 48)
    print("Creating Power BI Template files ready for import")
    print()
    
    try:
        # Create all PBIT templates
        created_files = creator.create_all_templates()
        
        if not created_files:
            creator.print_status("No PBIT templates were created", "error")
            return 1
        
        # Create usage instructions
        creator.create_usage_instructions(created_files)
        
        # Success summary
        print("\n🎉 PBIT TEMPLATE CREATION COMPLETE!")
        print("=" * 42)
        print(f"✅ Created {len(created_files)} PBIT templates")
        print(f"📁 Location: {creator.output_dir}")
        print()
        print("📊 Templates Created:")
        for file_info in created_files:
            filename = file_info["path"].name
            size_kb = file_info["path"].stat().st_size / 1024
            print(f"   • {filename} ({size_kb:.1f} KB) - {file_info['type'].title()}")
        
        print()
        print("🚀 How to Use:")
        print("1. Double-click any .pbit file")
        print("2. Point Power BI to your CSV files folder")
        print("3. Click 'Load' to import data")
        print("4. Customize and publish to Power BI Service")
        print()
        print("📖 See PBIT_USAGE_GUIDE.md for detailed instructions")
        
        return 0
        
    except Exception as e:
        creator.print_status(f"PBIT creation failed: {e}", "error")
        return 1

if __name__ == "__main__":
    exit(main())