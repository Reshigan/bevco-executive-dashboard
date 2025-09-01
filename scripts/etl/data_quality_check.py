import pandas as pd
import os
from datetime import datetime

# Data directory
data_dir = "/workspace/bevco-executive-dashboard/data/master"
output_dir = "/workspace/bevco-executive-dashboard/data/processed"

def check_data_quality():
    """Run data quality checks on all master data files"""
    
    print("Running Data Quality Checks...")
    print("=" * 50)
    
    issues = []
    summary = []
    
    # Check each data file
    files_to_check = [
        ("dim_date.csv", check_date_dimension),
        ("dim_product.csv", check_product_dimension),
        ("dim_customer.csv", check_customer_dimension),
        ("dim_employee.csv", check_employee_dimension),
        ("fact_sales.csv", check_sales_facts),
        ("fact_budget.csv", check_budget_facts),
        ("fact_inventory.csv", check_inventory_facts)
    ]
    
    for filename, check_function in files_to_check:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            print(f"\nChecking {filename}...")
            df = pd.read_csv(filepath)
            file_issues = check_function(df)
            issues.extend([(filename, issue) for issue in file_issues])
            
            summary.append({
                'File': filename,
                'Records': len(df),
                'Columns': len(df.columns),
                'Issues': len(file_issues),
                'Status': 'PASS' if len(file_issues) == 0 else 'WARN'
            })
        else:
            print(f"WARNING: {filename} not found!")
            issues.append((filename, "File not found"))
            summary.append({
                'File': filename,
                'Records': 0,
                'Columns': 0,
                'Issues': 1,
                'Status': 'FAIL'
            })
    
    # Generate quality report
    generate_quality_report(summary, issues)
    
    return len(issues) == 0

def check_date_dimension(df):
    """Check date dimension data quality"""
    issues = []
    
    # Check for missing dates
    date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D')
    if len(df) != len(date_range):
        issues.append("Missing dates in sequence")
    
    # Check for duplicates
    if df['DateKey'].duplicated().any():
        issues.append("Duplicate DateKey values found")
    
    # Check for null values
    if df.isnull().any().any():
        issues.append("Null values found")
    
    return issues

def check_product_dimension(df):
    """Check product dimension data quality"""
    issues = []
    
    # Check for duplicate SKUs
    if df['SKU'].duplicated().any():
        issues.append("Duplicate SKU values found")
    
    # Check price logic
    invalid_prices = df[df['UnitPrice'] < df['UnitCost']]
    if len(invalid_prices) > 0:
        issues.append(f"{len(invalid_prices)} products have UnitPrice < UnitCost")
    
    # Check for missing values in required fields
    required_fields = ['ProductKey', 'SKU', 'ProductName', 'Category']
    for field in required_fields:
        if df[field].isnull().any():
            issues.append(f"Null values found in {field}")
    
    return issues

def check_customer_dimension(df):
    """Check customer dimension data quality"""
    issues = []
    
    # Check for duplicate customer codes
    if df['CustomerCode'].duplicated().any():
        issues.append("Duplicate CustomerCode values found")
    
    # Check credit limits
    if (df['CreditLimit'] < 0).any():
        issues.append("Negative credit limits found")
    
    # Check payment terms
    valid_terms = [7, 14, 30, 45]
    invalid_terms = ~df['PaymentTerms'].isin(valid_terms)
    if invalid_terms.any():
        issues.append("Invalid payment terms found")
    
    return issues

def check_employee_dimension(df):
    """Check employee dimension data quality"""
    issues = []
    
    # Check for duplicate employee codes
    if df['EmployeeCode'].duplicated().any():
        issues.append("Duplicate EmployeeCode values found")
    
    # Check salary ranges
    if (df['Salary'] < 0).any():
        issues.append("Negative salary values found")
    
    # Check reporting structure
    # Employees reporting to non-existent managers
    managers = set(df['EmployeeKey'].values)
    reports_to = set(df['ReportsTo'].dropna().values)
    invalid_managers = reports_to - managers
    if invalid_managers:
        issues.append(f"{len(invalid_managers)} employees report to non-existent managers")
    
    return issues

def check_sales_facts(df):
    """Check sales facts data quality"""
    issues = []
    
    # Check for negative quantities
    if (df['Quantity'] < 0).any():
        issues.append("Negative quantities found")
    
    # Check for negative sales amounts
    if (df['NetSales'] < 0).any():
        issues.append("Negative net sales found")
    
    # Check discount logic
    invalid_discounts = df[df['DiscountAmount'] > df['GrossSales']]
    if len(invalid_discounts) > 0:
        issues.append(f"{len(invalid_discounts)} records have discount > gross sales")
    
    # Check profit calculation
    calc_profit = df['NetSales'] - df['Cost']
    profit_diff = abs(calc_profit - df['GrossProfit']) > 0.01
    if profit_diff.any():
        issues.append("Gross profit calculation errors found")
    
    return issues

def check_budget_facts(df):
    """Check budget facts data quality"""
    issues = []
    
    # Check for negative budget amounts
    if (df['BudgetAmount'] < 0).any():
        issues.append("Negative budget amounts found")
    
    # Check for missing departments
    if df['Department'].isnull().any():
        issues.append("Missing department values found")
    
    return issues

def check_inventory_facts(df):
    """Check inventory facts data quality"""
    issues = []
    
    # Check for negative stock
    if (df['StockOnHand'] < 0).any():
        issues.append("Negative stock on hand found")
    
    # Check reorder logic
    below_reorder = df[df['StockOnHand'] < df['ReorderPoint']]
    if len(below_reorder) > 0:
        issues.append(f"{len(below_reorder)} items below reorder point")
    
    # Check max stock logic
    above_max = df[df['StockOnHand'] > df['MaxStock']]
    if len(above_max) > 0:
        issues.append(f"{len(above_max)} items above maximum stock level")
    
    return issues

def generate_quality_report(summary, issues):
    """Generate a data quality report"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(summary)
    
    # Create report
    report_path = os.path.join(output_dir, "data_quality_report.txt")
    with open(report_path, 'w') as f:
        f.write("BEVCO EXECUTIVE DASHBOARD - DATA QUALITY REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(summary_df.to_string(index=False))
        f.write("\n\n")
        
        if issues:
            f.write("ISSUES FOUND\n")
            f.write("-" * 60 + "\n")
            for filename, issue in issues:
                f.write(f"{filename}: {issue}\n")
        else:
            f.write("No data quality issues found!\n")
        
        f.write("\n" + "=" * 60 + "\n")
        
        # Add statistics
        total_records = summary_df['Records'].sum()
        total_issues = summary_df['Issues'].sum()
        
        f.write(f"\nTotal Records: {total_records:,}\n")
        f.write(f"Total Issues: {total_issues}\n")
        f.write(f"Quality Score: {100 - (total_issues/len(summary_df)*10):.1f}%\n")
    
    print(f"\nQuality report saved to: {report_path}")
    
    # Also save as CSV for Power BI
    summary_df.to_csv(os.path.join(output_dir, "data_quality_summary.csv"), index=False)
    
    if issues:
        issues_df = pd.DataFrame(issues, columns=['File', 'Issue'])
        issues_df.to_csv(os.path.join(output_dir, "data_quality_issues.csv"), index=False)

if __name__ == "__main__":
    success = check_data_quality()
    if success:
        print("\n✓ All data quality checks passed!")
    else:
        print("\n⚠ Data quality issues found. Check the report for details.")
        exit(1)