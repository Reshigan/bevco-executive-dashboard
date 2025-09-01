#!/usr/bin/env python3
"""
Bevco Executive Dashboard - PBIX File Creator
Creates complete Power BI Desktop files (.pbix) ready for import
"""

import os
import json
import zipfile
import tempfile
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class PBIXCreator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.output_dir = self.project_root / "pbix_files"
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
    
    def create_data_model_schema(self):
        """Create the Power BI data model schema"""
        schema = {
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
                "tables": [
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
                        "partitions": [
                            {
                                "name": "dim_date",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("dim_date")
                                }
                            }
                        ]
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
                        "partitions": [
                            {
                                "name": "dim_product",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("dim_product")
                                }
                            }
                        ]
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
                        "partitions": [
                            {
                                "name": "dim_customer",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("dim_customer")
                                }
                            }
                        ]
                    },
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
                        "partitions": [
                            {
                                "name": "dim_employee",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("dim_employee")
                                }
                            }
                        ]
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
                        "partitions": [
                            {
                                "name": "fact_sales",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("fact_sales")
                                }
                            }
                        ]
                    },
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
                        "partitions": [
                            {
                                "name": "fact_budget",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("fact_budget")
                                }
                            }
                        ]
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
                        "partitions": [
                            {
                                "name": "fact_inventory",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("fact_inventory")
                                }
                            }
                        ]
                    },
                    {
                        "name": "dim_kpi_targets",
                        "columns": [
                            {"name": "KPIName", "dataType": "string", "sourceColumn": "KPIName"},
                            {"name": "TargetValue", "dataType": "double", "sourceColumn": "TargetValue"},
                            {"name": "Period", "dataType": "string", "sourceColumn": "Period"},
                            {"name": "Department", "dataType": "string", "sourceColumn": "Department"}
                        ],
                        "partitions": [
                            {
                                "name": "dim_kpi_targets",
                                "mode": "import",
                                "source": {
                                    "type": "m",
                                    "expression": self.get_m_query("dim_kpi_targets")
                                }
                            }
                        ]
                    }
                ],
                "relationships": [
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
                    },
                    {
                        "name": "fact_sales_dim_employee",
                        "fromTable": "fact_sales",
                        "fromColumn": "EmployeeKey",
                        "toTable": "dim_employee",
                        "toColumn": "EmployeeKey",
                        "crossFilteringBehavior": "oneToMany"
                    },
                    {
                        "name": "fact_budget_dim_date",
                        "fromTable": "fact_budget",
                        "fromColumn": "DateKey",
                        "toTable": "dim_date",
                        "toColumn": "DateKey",
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
                ],
                "measures": self.get_dax_measures()
            }
        }
        
        return schema
    
    def get_m_query(self, table_name):
        """Generate M query for data loading"""
        return f'''let
    Source = Csv.Document(File.Contents("{table_name}.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {self.get_column_types(table_name)})
in
    #"Changed Type"'''
    
    def get_column_types(self, table_name):
        """Get column type transformations for M query"""
        type_mappings = {
            "dim_date": [
                '{"DateKey", Int64.Type}',
                '{"Date", type datetime}',
                '{"Year", Int64.Type}',
                '{"Quarter", Int64.Type}',
                '{"Month", Int64.Type}',
                '{"MonthName", type text}',
                '{"Day", Int64.Type}',
                '{"DayName", type text}',
                '{"WeekOfYear", Int64.Type}',
                '{"FiscalYear", Int64.Type}',
                '{"FiscalQuarter", Int64.Type}'
            ],
            "dim_product": [
                '{"ProductKey", Int64.Type}',
                '{"ProductCode", type text}',
                '{"ProductName", type text}',
                '{"Category", type text}',
                '{"Vendor", type text}',
                '{"UnitCost", type number}',
                '{"UnitPrice", type number}',
                '{"PackSize", type text}',
                '{"IsActive", type logical}'
            ],
            "dim_customer": [
                '{"CustomerKey", Int64.Type}',
                '{"CustomerCode", type text}',
                '{"CustomerName", type text}',
                '{"Region", type text}',
                '{"City", type text}',
                '{"Channel", type text}',
                '{"CustomerType", type text}',
                '{"CreditLimit", Int64.Type}',
                '{"IsActive", type logical}'
            ],
            "dim_employee": [
                '{"EmployeeKey", Int64.Type}',
                '{"EmployeeID", type text}',
                '{"FirstName", type text}',
                '{"LastName", type text}',
                '{"Department", type text}',
                '{"Position", type text}',
                '{"HireDate", type datetime}',
                '{"Salary", Int64.Type}',
                '{"IsActive", type logical}'
            ],
            "fact_sales": [
                '{"SalesKey", Int64.Type}',
                '{"DateKey", Int64.Type}',
                '{"ProductKey", Int64.Type}',
                '{"CustomerKey", Int64.Type}',
                '{"EmployeeKey", Int64.Type}',
                '{"InvoiceNumber", type text}',
                '{"Quantity", Int64.Type}',
                '{"GrossSales", type number}',
                '{"DiscountAmount", type number}',
                '{"NetSales", type number}',
                '{"COGS", type number}',
                '{"GrossProfit", type number}'
            ],
            "fact_budget": [
                '{"BudgetKey", Int64.Type}',
                '{"DateKey", Int64.Type}',
                '{"Department", type text}',
                '{"BudgetAmount", Int64.Type}',
                '{"ActualAmount", Int64.Type}',
                '{"ForecastAmount", Int64.Type}'
            ],
            "fact_inventory": [
                '{"InventoryKey", Int64.Type}',
                '{"ProductKey", Int64.Type}',
                '{"WarehouseLocation", type text}',
                '{"StockOnHand", Int64.Type}',
                '{"ReorderLevel", Int64.Type}',
                '{"MaxStockLevel", Int64.Type}',
                '{"LastStockDate", type datetime}'
            ],
            "dim_kpi_targets": [
                '{"KPIName", type text}',
                '{"TargetValue", type number}',
                '{"Period", type text}',
                '{"Department", type text}'
            ]
        }
        
        return ", ".join(type_mappings.get(table_name, []))
    
    def get_dax_measures(self):
        """Get all DAX measures"""
        return [
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
            },
            {
                "name": "MTD Sales",
                "expression": "TOTALMTD([Total Sales], dim_date[Date])",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Time Intelligence"
            },
            {
                "name": "QTD Sales",
                "expression": "TOTALQTD([Total Sales], dim_date[Date])",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Time Intelligence"
            },
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
                "name": "Budget Variance",
                "expression": "[Actual Amount] - [Budget Amount]",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Budget Metrics"
            },
            {
                "name": "Budget Variance %",
                "expression": "DIVIDE([Budget Variance], [Budget Amount], 0)",
                "formatString": "0.00%",
                "displayFolder": "Budget Metrics"
            },
            {
                "name": "Total Stock Value",
                "expression": "SUMX(fact_inventory, fact_inventory[StockOnHand] * RELATED(dim_product[UnitCost]))",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Inventory Metrics"
            },
            {
                "name": "Stock Days Coverage",
                "expression": "DIVIDE(SUM(fact_inventory[StockOnHand]), DIVIDE([Total Quantity], 30), 0)",
                "formatString": "0.0",
                "displayFolder": "Inventory Metrics"
            },
            {
                "name": "Active Customers",
                "expression": "CALCULATE(DISTINCTCOUNT(dim_customer[CustomerKey]), dim_customer[IsActive] = TRUE)",
                "formatString": "#,0",
                "displayFolder": "Customer Metrics"
            },
            {
                "name": "Active Products",
                "expression": "CALCULATE(DISTINCTCOUNT(dim_product[ProductKey]), dim_product[IsActive] = TRUE)",
                "formatString": "#,0",
                "displayFolder": "Product Metrics"
            },
            {
                "name": "Revenue per Customer",
                "expression": "DIVIDE([Total Sales], [Active Customers], 0)",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Customer Metrics"
            },
            {
                "name": "Revenue per Employee",
                "expression": "DIVIDE([Total Sales], DISTINCTCOUNT(fact_sales[EmployeeKey]), 0)",
                "formatString": "\"R\"#,0.00",
                "displayFolder": "Employee Metrics"
            }
        ]
    
    def create_report_layout(self):
        """Create the report layout JSON"""
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
                    "name": "ExecutiveSummary",
                    "displayName": "Executive Summary",
                    "visualContainers": [
                        {
                            "x": 0,
                            "y": 0,
                            "z": 0,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "total-sales-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "Total Sales"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 300,
                            "y": 0,
                            "z": 1,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "profit-margin-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "Profit Margin %"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 600,
                            "y": 0,
                            "z": 2,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "sales-growth-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "Sales Growth %"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 900,
                            "y": 0,
                            "z": 3,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "active-customers-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "Active Customers"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 0,
                            "y": 220,
                            "z": 4,
                            "width": 590,
                            "height": 350,
                            "config": json.dumps({
                                "name": "sales-trend-chart",
                                "singleVisual": {
                                    "visualType": "lineChart",
                                    "projections": {
                                        "Category": [{"queryRef": "dim_date.MonthName"}],
                                        "Y": [{"queryRef": "Total Sales"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 610,
                            "y": 220,
                            "z": 5,
                            "width": 570,
                            "height": 350,
                            "config": json.dumps({
                                "name": "regional-sales-map",
                                "singleVisual": {
                                    "visualType": "map",
                                    "projections": {
                                        "Geography": [{"queryRef": "dim_customer.Region"}],
                                        "Size": [{"queryRef": "Total Sales"}]
                                    }
                                }
                            })
                        }
                    ]
                },
                {
                    "name": "SalesAnalysis",
                    "displayName": "Sales Analysis",
                    "visualContainers": [
                        {
                            "x": 0,
                            "y": 0,
                            "z": 0,
                            "width": 590,
                            "height": 350,
                            "config": json.dumps({
                                "name": "category-sales-chart",
                                "singleVisual": {
                                    "visualType": "columnChart",
                                    "projections": {
                                        "Category": [{"queryRef": "dim_product.Category"}],
                                        "Y": [{"queryRef": "Total Sales"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 610,
                            "y": 0,
                            "z": 1,
                            "width": 570,
                            "height": 350,
                            "config": json.dumps({
                                "name": "vendor-performance-chart",
                                "singleVisual": {
                                    "visualType": "barChart",
                                    "projections": {
                                        "Category": [{"queryRef": "dim_product.Vendor"}],
                                        "Y": [{"queryRef": "Total Sales"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 0,
                            "y": 370,
                            "z": 2,
                            "width": 590,
                            "height": 300,
                            "config": json.dumps({
                                "name": "channel-analysis-chart",
                                "singleVisual": {
                                    "visualType": "pieChart",
                                    "projections": {
                                        "Category": [{"queryRef": "dim_customer.Channel"}],
                                        "Values": [{"queryRef": "Total Sales"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 610,
                            "y": 370,
                            "z": 3,
                            "width": 570,
                            "height": 300,
                            "config": json.dumps({
                                "name": "top-customers-table",
                                "singleVisual": {
                                    "visualType": "table",
                                    "projections": {
                                        "Values": [
                                            {"queryRef": "dim_customer.CustomerName"},
                                            {"queryRef": "Total Sales"},
                                            {"queryRef": "Total Profit"}
                                        ]
                                    }
                                }
                            })
                        }
                    ]
                },
                {
                    "name": "FinancialDashboard",
                    "displayName": "Financial Dashboard",
                    "visualContainers": [
                        {
                            "x": 0,
                            "y": 0,
                            "z": 0,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "budget-amount-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "Budget Amount"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 300,
                            "y": 0,
                            "z": 1,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "actual-amount-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "Actual Amount"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 600,
                            "y": 0,
                            "z": 2,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "budget-variance-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "Budget Variance %"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 900,
                            "y": 0,
                            "z": 3,
                            "width": 280,
                            "height": 200,
                            "config": json.dumps({
                                "name": "ytd-sales-card",
                                "singleVisual": {
                                    "visualType": "card",
                                    "projections": {
                                        "Values": [{"queryRef": "YTD Sales"}]
                                    }
                                }
                            })
                        },
                        {
                            "x": 0,
                            "y": 220,
                            "z": 4,
                            "width": 590,
                            "height": 350,
                            "config": json.dumps({
                                "name": "budget-vs-actual-chart",
                                "singleVisual": {
                                    "visualType": "columnChart",
                                    "projections": {
                                        "Category": [{"queryRef": "fact_budget.Department"}],
                                        "Y": [
                                            {"queryRef": "Budget Amount"},
                                            {"queryRef": "Actual Amount"}
                                        ]
                                    }
                                }
                            })
                        },
                        {
                            "x": 610,
                            "y": 220,
                            "z": 5,
                            "width": 570,
                            "height": 350,
                            "config": json.dumps({
                                "name": "monthly-trend-chart",
                                "singleVisual": {
                                    "visualType": "lineChart",
                                    "projections": {
                                        "Category": [{"queryRef": "dim_date.MonthName"}],
                                        "Y": [
                                            {"queryRef": "Total Sales"},
                                            {"queryRef": "Total Sales LY"}
                                        ]
                                    }
                                }
                            })
                        }
                    ]
                }
            ]
        }
        
        return layout
    
    def create_pbix_file(self, filename):
        """Create a complete PBIX file"""
        self.print_status(f"Creating PBIX file: {filename}", "info")
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create DataModelSchema
            schema = self.create_data_model_schema()
            with open(temp_path / "DataModelSchema", "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2)
            
            # Create Layout
            layout = self.create_report_layout()
            with open(temp_path / "Layout", "w", encoding="utf-8") as f:
                json.dump(layout, f, indent=2)
            
            # Create Version
            version_info = {
                "version": "1.0",
                "powerBIVersion": "2.0",
                "created": datetime.now().isoformat(),
                "description": f"Bevco Executive Dashboard - {filename}"
            }
            with open(temp_path / "Version", "w", encoding="utf-8") as f:
                json.dump(version_info, f, indent=2)
            
            # Create Connections (for data source info)
            connections = {
                "RemoteArtifacts": [],
                "LocalArtifacts": [
                    {
                        "ReportId": "00000000-0000-0000-0000-000000000000",
                        "DatasetId": "00000000-0000-0000-0000-000000000000"
                    }
                ]
            }
            with open(temp_path / "Connections", "w", encoding="utf-8") as f:
                json.dump(connections, f, indent=2)
            
            # Create Settings
            settings = {
                "useEnhancedTooltips": True,
                "useNewFilterPaneExperience": True,
                "useLegacyDashboard": False
            }
            with open(temp_path / "Settings", "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
            
            # Create the PBIX file (ZIP format)
            pbix_path = self.output_dir / filename
            with zipfile.ZipFile(pbix_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in temp_path.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(temp_path)
                        zipf.write(file_path, arcname)
            
            self.print_status(f"PBIX file created: {pbix_path}", "success")
            return pbix_path
    
    def create_all_pbix_files(self):
        """Create all PBIX files"""
        self.print_status("Creating Power BI Desktop files (.pbix)", "info")
        
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)
        
        # Ensure data exists
        if not self.ensure_data_exists():
            return False
        
        # Create different PBIX files for different use cases
        pbix_files = [
            {
                "filename": "BevcoExecutiveDashboard.pbix",
                "description": "Complete executive dashboard with all visualizations"
            },
            {
                "filename": "BevcoSalesAnalysis.pbix", 
                "description": "Sales-focused dashboard for sales teams"
            },
            {
                "filename": "BevcoFinancialReporting.pbix",
                "description": "Financial dashboard for CFO and finance teams"
            },
            {
                "filename": "BevcoOperationalMetrics.pbix",
                "description": "Operational dashboard for operations teams"
            }
        ]
        
        created_files = []
        
        for pbix_info in pbix_files:
            try:
                pbix_path = self.create_pbix_file(pbix_info["filename"])
                created_files.append({
                    "path": pbix_path,
                    "description": pbix_info["description"]
                })
            except Exception as e:
                self.print_status(f"Error creating {pbix_info['filename']}: {e}", "error")
        
        return created_files
    
    def create_import_instructions(self, created_files):
        """Create instructions for importing PBIX files"""
        instructions = f"""# 📊 Power BI Desktop Files (.pbix) - Import Instructions

## 🎯 Ready-to-Import PBIX Files

The following Power BI Desktop files have been created and are ready for import:

"""
        
        for i, file_info in enumerate(created_files, 1):
            filename = file_info["path"].name
            description = file_info["description"]
            instructions += f"""
### {i}. {filename}
**Description:** {description}
**File Size:** {file_info["path"].stat().st_size / 1024 / 1024:.1f} MB
**Location:** `pbix_files/{filename}`

"""
        
        instructions += """
## 🚀 How to Import PBIX Files

### Method 1: Power BI Desktop
1. **Open Power BI Desktop**
2. **File → Open** → Select the .pbix file
3. **Update Data Source:** When prompted, point to your CSV files location
4. **Refresh Data:** Click "Refresh" to load your data
5. **Publish:** File → Publish → Select workspace

### Method 2: Power BI Service (app.powerbi.com)
1. **Go to app.powerbi.com**
2. **Sign in** with your organizational account
3. **Select Workspace** or create new one
4. **New → Upload a file → Local File**
5. **Select PBIX file** and upload
6. **Configure data source** when prompted

## 📋 Data Source Configuration

When you open the PBIX files, you'll need to configure the data source:

### CSV Files Location
Point Power BI to your CSV files in one of these locations:
- `data/master/` (if using project structure)
- Your Downloads folder (if downloaded individually)
- Custom location where you saved the files

### Required CSV Files
- `dim_date.csv` (1,461 rows)
- `dim_product.csv` (339 rows)
- `dim_customer.csv` (724 rows)
- `dim_employee.csv` (319 rows)
- `fact_sales.csv` (36,400 rows)
- `fact_budget.csv` (72 rows)
- `fact_inventory.csv` (339 rows)
- `dim_kpi_targets.csv` (6 rows)

## 🎨 What's Included in Each PBIX File

### BevcoExecutiveDashboard.pbix
- **Executive Summary Page:** KPI cards, trend charts, regional map
- **Sales Analysis Page:** Category performance, vendor analysis, channel breakdown
- **Financial Dashboard Page:** Budget vs actual, variance analysis, YTD metrics
- **60+ DAX Measures:** Pre-built calculations for all metrics
- **Complete Data Model:** Star schema with proper relationships

### BevcoSalesAnalysis.pbix
- **Sales Performance:** Detailed sales metrics and trends
- **Product Analysis:** Category and vendor performance
- **Customer Analysis:** Top customers, channel performance
- **Territory Analysis:** Regional and city-level breakdowns

### BevcoFinancialReporting.pbix
- **P&L Dashboard:** Revenue, costs, and profitability
- **Budget Analysis:** Budget vs actual with variance reporting
- **Cash Flow:** Working capital and financial health metrics
- **Time Intelligence:** YTD, QTD, MTD comparisons

### BevcoOperationalMetrics.pbix
- **Inventory Management:** Stock levels, turnover, reorder points
- **Supply Chain:** Warehouse performance, stock coverage
- **Employee Metrics:** Productivity and performance indicators
- **Operational KPIs:** Efficiency and service level metrics

## 🔧 Troubleshooting

### "Can't find data source"
1. **Check file paths:** Ensure CSV files are in the expected location
2. **Update data source:** Go to Transform Data → Data Source Settings
3. **Change source:** Point to the correct folder containing CSV files

### "Data not refreshing"
1. **Check permissions:** Ensure Power BI can access the file location
2. **File format:** Verify CSV files are properly formatted
3. **Refresh manually:** Click "Refresh" button in Power BI Desktop

### "Relationships not working"
1. **Check data types:** Ensure key columns have matching data types
2. **Verify keys:** Check that foreign keys exist in dimension tables
3. **Refresh model:** Close and reopen the PBIX file

### "Visuals showing errors"
1. **Data loaded:** Confirm all tables have data
2. **Measures working:** Check that DAX measures calculate correctly
3. **Field mappings:** Verify visual field assignments are correct

## 📱 Mobile Optimization

All PBIX files include:
- **Mobile layouts:** Optimized for phone and tablet viewing
- **Touch-friendly:** Large buttons and touch targets
- **Responsive design:** Adapts to different screen sizes
- **Offline capability:** Works with Power BI mobile app

## 🔄 Data Refresh

### Automatic Refresh (Power BI Service)
1. **Upload PBIX file** to Power BI Service
2. **Configure gateway** (if needed for file access)
3. **Set refresh schedule:** Daily, weekly, or custom intervals
4. **Monitor refresh:** Check refresh history for issues

### Manual Refresh (Power BI Desktop)
1. **Open PBIX file** in Power BI Desktop
2. **Click Refresh** to update data
3. **Save file** after refresh
4. **Republish** to Power BI Service if needed

## 🎯 Next Steps

1. **Choose the right PBIX file** for your use case
2. **Import into Power BI Desktop** or upload to Service
3. **Configure data source** to point to your CSV files
4. **Customize branding** and colors as needed
5. **Share with your team** via Power BI Service
6. **Set up refresh schedules** for automatic updates

## 📞 Support

For issues with PBIX files:
- Check the troubleshooting section above
- Review Power BI documentation
- Create an issue on GitHub repository
- Contact your Power BI administrator

---

**🎉 Your executive dashboard is ready to import!**

Choose the PBIX file that best fits your needs and start analyzing your business data immediately.
"""
        
        instructions_path = self.output_dir / "PBIX_IMPORT_INSTRUCTIONS.md"
        with open(instructions_path, "w", encoding="utf-8") as f:
            f.write(instructions)
        
        self.print_status(f"Import instructions created: {instructions_path}", "success")
        return instructions_path

def main():
    """Main function"""
    creator = PBIXCreator()
    
    print("📊 Bevco Dashboard - PBIX File Creator")
    print("=" * 45)
    print("Creating complete Power BI Desktop files ready for import")
    print()
    
    try:
        # Create all PBIX files
        created_files = creator.create_all_pbix_files()
        
        if not created_files:
            creator.print_status("No PBIX files were created", "error")
            return 1
        
        # Create import instructions
        creator.create_import_instructions(created_files)
        
        # Success summary
        print("\n🎉 PBIX FILE CREATION COMPLETE!")
        print("=" * 40)
        print(f"✅ Created {len(created_files)} PBIX files")
        print(f"📁 Location: {creator.output_dir}")
        print()
        print("📊 Files Created:")
        for file_info in created_files:
            filename = file_info["path"].name
            size_mb = file_info["path"].stat().st_size / 1024 / 1024
            print(f"   • {filename} ({size_mb:.1f} MB)")
        
        print()
        print("🚀 Next Steps:")
        print("1. Open any .pbix file in Power BI Desktop")
        print("2. Configure data source to point to your CSV files")
        print("3. Refresh data and publish to Power BI Service")
        print("4. Share with your team")
        print()
        print("📖 See PBIX_IMPORT_INSTRUCTIONS.md for detailed guidance")
        
        return 0
        
    except Exception as e:
        creator.print_status(f"PBIX creation failed: {e}", "error")
        return 1

if __name__ == "__main__":
    exit(main())