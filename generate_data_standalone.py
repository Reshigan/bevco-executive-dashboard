#!/usr/bin/env python3
"""
Standalone Bevco Dashboard Data Generator
Run this script from the project root directory to generate sample data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("🚀 Bevco Executive Dashboard - Data Generator")
print("=" * 50)

# Define output directory - current working directory
current_dir = os.getcwd()
output_dir = os.path.join(current_dir, "data", "master")

# Create output directory if it doesn't exist
try:
    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ Output directory: {output_dir}")
except OSError as e:
    print(f"✗ Error creating directory {output_dir}: {e}")
    print("Creating data directory in current folder...")
    output_dir = os.path.join(current_dir, "master_data")
    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ Using directory: {output_dir}")

# Generate Date Dimension
def generate_date_dimension():
    print("📅 Generating date dimension...")
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    date_dim = pd.DataFrame({
        'DateKey': [int(d.strftime('%Y%m%d')) for d in dates],
        'Date': dates,
        'Year': dates.year,
        'Quarter': dates.quarter,
        'Month': dates.month,
        'MonthName': dates.strftime('%B'),
        'Day': dates.day,
        'DayName': dates.strftime('%A'),
        'WeekOfYear': dates.isocalendar().week,
        'DayOfYear': dates.dayofyear,
        'IsWeekend': dates.weekday >= 5,
        'FiscalYear': np.where(dates.month >= 4, dates.year + 1, dates.year),
        'FiscalQuarter': np.where(dates.month >= 4, 
                                 ((dates.month - 4) // 3) + 1,
                                 ((dates.month + 8) // 3) + 1)
    })
    
    return date_dim

# Generate Product Dimension
def generate_product_dimension():
    print("📦 Generating product dimension...")
    
    # South African beverage categories
    categories = ['Beer', 'Wine', 'Spirits', 'Soft Drinks', 'Water']
    vendors = ['SAB Miller', 'Distell', 'Coca-Cola', 'Pepsi', 'Local Brands']
    
    products = []
    product_key = 1
    
    for category in categories:
        for vendor in vendors:
            # Generate 10-15 products per category-vendor combination
            num_products = random.randint(10, 15)
            for i in range(num_products):
                base_price = {
                    'Beer': random.uniform(15, 45),
                    'Wine': random.uniform(50, 300),
                    'Spirits': random.uniform(80, 500),
                    'Soft Drinks': random.uniform(8, 25),
                    'Water': random.uniform(5, 15)
                }[category]
                
                product = {
                    'ProductKey': product_key,
                    'ProductCode': f"{category[:3].upper()}{vendor[:3].upper()}{i+1:03d}",
                    'ProductName': f"{vendor} {category} Product {i+1}",
                    'Category': category,
                    'Vendor': vendor,
                    'UnitCost': round(base_price * 0.6, 2),
                    'UnitPrice': round(base_price, 2),
                    'PackSize': random.choice(['330ml', '500ml', '750ml', '1L', '2L']),
                    'LaunchDate': datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1095)),
                    'IsActive': random.choice([True, True, True, False])  # 75% active
                }
                products.append(product)
                product_key += 1
    
    return pd.DataFrame(products)

# Generate Customer Dimension
def generate_customer_dimension():
    print("🏪 Generating customer dimension...")
    
    # South African regions and cities
    regions = {
        'Gauteng': ['Johannesburg', 'Pretoria', 'Sandton', 'Randburg'],
        'Western Cape': ['Cape Town', 'Stellenbosch', 'Paarl', 'George'],
        'KwaZulu-Natal': ['Durban', 'Pietermaritzburg', 'Newcastle', 'Richards Bay'],
        'Eastern Cape': ['Port Elizabeth', 'East London', 'Grahamstown'],
        'Free State': ['Bloemfontein', 'Welkom', 'Kroonstad'],
        'Limpopo': ['Polokwane', 'Tzaneen', 'Musina'],
        'Mpumalanga': ['Nelspruit', 'Witbank', 'Secunda'],
        'North West': ['Rustenburg', 'Klerksdorp', 'Potchefstroom'],
        'Northern Cape': ['Kimberley', 'Upington', 'Springbok']
    }
    
    channels = ['Retail', 'Wholesale', 'On-Trade', 'Export']
    customer_types = ['Chain Store', 'Independent', 'Restaurant', 'Bar', 'Hotel']
    
    customers = []
    customer_key = 1
    
    for region, cities in regions.items():
        # Generate 80-90 customers per region
        num_customers = random.randint(80, 90)
        for i in range(num_customers):
            city = random.choice(cities)
            channel = random.choice(channels)
            customer_type = random.choice(customer_types)
            
            customer = {
                'CustomerKey': customer_key,
                'CustomerCode': f"C{region[:3].upper()}{customer_key:04d}",
                'CustomerName': f"{customer_type} {city} {i+1}",
                'Region': region,
                'City': city,
                'Channel': channel,
                'CustomerType': customer_type,
                'CreditLimit': random.randint(50000, 500000),
                'PaymentTerms': random.choice(['30 Days', '60 Days', '90 Days', 'Cash']),
                'IsActive': random.choice([True, True, True, False])  # 75% active
            }
            customers.append(customer)
            customer_key += 1
    
    return pd.DataFrame(customers)

# Generate Employee Dimension
def generate_employee_dimension():
    print("👥 Generating employee dimension...")
    
    departments = ['Sales', 'Marketing', 'Finance', 'Operations', 'HR', 'IT']
    positions = {
        'Sales': ['Sales Rep', 'Sales Manager', 'Regional Manager', 'Sales Director'],
        'Marketing': ['Marketing Coordinator', 'Brand Manager', 'Marketing Manager', 'CMO'],
        'Finance': ['Accountant', 'Financial Analyst', 'Finance Manager', 'CFO'],
        'Operations': ['Warehouse Clerk', 'Logistics Coordinator', 'Operations Manager', 'COO'],
        'HR': ['HR Assistant', 'HR Generalist', 'HR Manager', 'CHRO'],
        'IT': ['IT Support', 'Developer', 'IT Manager', 'CTO']
    }
    
    employees = []
    employee_key = 1
    
    for dept in departments:
        # Generate 50-55 employees per department
        num_employees = random.randint(50, 55)
        for i in range(num_employees):
            position = random.choice(positions[dept])
            base_salary = {
                'Sales Rep': random.randint(180000, 300000),
                'Sales Manager': random.randint(400000, 600000),
                'Regional Manager': random.randint(600000, 800000),
                'Sales Director': random.randint(800000, 1200000),
                'Marketing Coordinator': random.randint(200000, 350000),
                'Brand Manager': random.randint(450000, 650000),
                'Marketing Manager': random.randint(600000, 800000),
                'CMO': random.randint(1000000, 1500000)
            }.get(position, random.randint(200000, 500000))
            
            employee = {
                'EmployeeKey': employee_key,
                'EmployeeID': f"EMP{employee_key:04d}",
                'FirstName': f"Employee{employee_key}",
                'LastName': f"Surname{employee_key}",
                'Department': dept,
                'Position': position,
                'HireDate': datetime(2018, 1, 1) + timedelta(days=random.randint(0, 1825)),
                'Salary': base_salary,
                'Manager': random.choice([True, False]) if position in ['Manager', 'Director', 'CMO', 'CFO', 'COO', 'CHRO', 'CTO'] else False,
                'IsActive': random.choice([True, True, True, True, False])  # 80% active
            }
            employees.append(employee)
            employee_key += 1
    
    return pd.DataFrame(employees)

# Generate Sales Facts
def generate_sales_facts(date_dim, product_dim, customer_dim, employee_dim):
    print("💰 Generating sales transactions...")
    
    # Filter to active records and recent dates
    active_products = product_dim[product_dim['IsActive']].copy()
    active_customers = customer_dim[customer_dim['IsActive']].copy()
    active_employees = employee_dim[employee_dim['IsActive']].copy()
    recent_dates = date_dim[date_dim['Date'] >= '2024-01-01'].copy()
    
    print(f"   Active products: {len(active_products)}")
    print(f"   Active customers: {len(active_customers)}")
    print(f"   Active employees: {len(active_employees)}")
    print(f"   Date range: {len(recent_dates)} days")
    
    # Generate sales transactions using vectorized operations
    num_transactions = 36400  # Target number of transactions
    
    # Pre-generate random choices
    date_keys = np.random.choice(recent_dates['DateKey'].values, num_transactions)
    product_keys = np.random.choice(active_products['ProductKey'].values, num_transactions)
    customer_keys = np.random.choice(active_customers['CustomerKey'].values, num_transactions)
    employee_keys = np.random.choice(active_employees['EmployeeKey'].values, num_transactions)
    
    # Create base DataFrame
    sales_facts = pd.DataFrame({
        'SalesKey': range(1, num_transactions + 1),
        'DateKey': date_keys,
        'ProductKey': product_keys,
        'CustomerKey': customer_keys,
        'EmployeeKey': employee_keys,
        'InvoiceNumber': [f"INV{i:06d}" for i in range(1, num_transactions + 1)],
        'Quantity': np.random.randint(1, 101, num_transactions),
        'DiscountPercent': np.random.uniform(0, 0.15, num_transactions)
    })
    
    # Merge with product data to get prices
    sales_facts = sales_facts.merge(
        active_products[['ProductKey', 'UnitCost', 'UnitPrice']], 
        on='ProductKey', 
        how='left'
    )
    
    # Calculate financial metrics
    sales_facts['GrossSales'] = sales_facts['Quantity'] * sales_facts['UnitPrice']
    sales_facts['DiscountAmount'] = sales_facts['GrossSales'] * sales_facts['DiscountPercent']
    sales_facts['NetSales'] = sales_facts['GrossSales'] - sales_facts['DiscountAmount']
    sales_facts['COGS'] = sales_facts['Quantity'] * sales_facts['UnitCost']
    sales_facts['GrossProfit'] = sales_facts['NetSales'] - sales_facts['COGS']
    
    # Round financial columns
    financial_cols = ['GrossSales', 'DiscountAmount', 'NetSales', 'COGS', 'GrossProfit']
    for col in financial_cols:
        sales_facts[col] = sales_facts[col].round(2)
    
    sales_facts['DiscountPercent'] = sales_facts['DiscountPercent'].round(4)
    
    # Drop helper columns
    sales_facts = sales_facts.drop(['UnitCost', 'UnitPrice'], axis=1)
    
    return sales_facts

# Generate other fact tables
def generate_budget_facts(date_dim):
    print("📊 Generating budget data...")
    
    departments = ['Sales', 'Marketing', 'Finance', 'Operations', 'HR', 'IT']
    budget_data = []
    
    for dept in departments:
        for _, date_row in date_dim[date_dim['Date'] >= '2024-01-01'].iterrows():
            if date_row['Day'] == 1:  # Monthly budget entries
                base_budget = random.randint(500000, 2000000)
                budget_entry = {
                    'BudgetKey': len(budget_data) + 1,
                    'DateKey': date_row['DateKey'],
                    'Department': dept,
                    'BudgetAmount': base_budget,
                    'ActualAmount': base_budget * random.uniform(0.8, 1.2),
                    'ForecastAmount': base_budget * random.uniform(0.9, 1.1)
                }
                budget_data.append(budget_entry)
    
    return pd.DataFrame(budget_data)

def generate_inventory_facts(product_dim):
    print("📦 Generating inventory data...")
    
    active_products = product_dim[product_dim['IsActive']].copy()
    inventory_data = []
    
    for _, product in active_products.iterrows():
        inventory_entry = {
            'InventoryKey': len(inventory_data) + 1,
            'ProductKey': product['ProductKey'],
            'WarehouseLocation': random.choice(['JHB Main', 'CPT Main', 'DBN Main', 'PE Branch']),
            'StockOnHand': random.randint(0, 1000),
            'ReorderLevel': random.randint(50, 200),
            'MaxStockLevel': random.randint(500, 1500),
            'LastStockDate': datetime.now() - timedelta(days=random.randint(0, 30))
        }
        inventory_data.append(inventory_entry)
    
    return pd.DataFrame(inventory_data)

def generate_kpi_targets():
    print("🎯 Generating KPI targets...")
    
    kpi_targets = [
        {'KPIName': 'Total Sales', 'TargetValue': 50000000, 'Period': 'Annual', 'Department': 'Sales'},
        {'KPIName': 'Gross Margin %', 'TargetValue': 35, 'Period': 'Annual', 'Department': 'Sales'},
        {'KPIName': 'Customer Satisfaction', 'TargetValue': 85, 'Period': 'Quarterly', 'Department': 'Sales'},
        {'KPIName': 'Inventory Turnover', 'TargetValue': 12, 'Period': 'Annual', 'Department': 'Operations'},
        {'KPIName': 'Employee Retention %', 'TargetValue': 90, 'Period': 'Annual', 'Department': 'HR'},
        {'KPIName': 'Cost per Case', 'TargetValue': 25, 'Period': 'Monthly', 'Department': 'Operations'}
    ]
    
    return pd.DataFrame(kpi_targets)

# Main execution
def main():
    try:
        # Generate all dimensions
        date_dim = generate_date_dimension()
        product_dim = generate_product_dimension()
        customer_dim = generate_customer_dimension()
        employee_dim = generate_employee_dimension()
        
        # Generate fact tables
        sales_facts = generate_sales_facts(date_dim, product_dim, customer_dim, employee_dim)
        budget_facts = generate_budget_facts(date_dim)
        inventory_facts = generate_inventory_facts(product_dim)
        kpi_targets = generate_kpi_targets()
        
        # Save all files
        print("\n💾 Saving data files...")
        
        files_to_save = [
            (date_dim, 'dim_date.csv'),
            (product_dim, 'dim_product.csv'),
            (customer_dim, 'dim_customer.csv'),
            (employee_dim, 'dim_employee.csv'),
            (sales_facts, 'fact_sales.csv'),
            (budget_facts, 'fact_budget.csv'),
            (inventory_facts, 'fact_inventory.csv'),
            (kpi_targets, 'dim_kpi_targets.csv')
        ]
        
        for df, filename in files_to_save:
            filepath = os.path.join(output_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"   ✓ {filename} ({len(df):,} rows)")
        
        print(f"\n🎉 Data generation complete!")
        print(f"📁 Files saved to: {output_dir}")
        print(f"📊 Total sales transactions: {len(sales_facts):,}")
        print(f"🏪 Total customers: {len(customer_dim):,}")
        print(f"📦 Total products: {len(product_dim):,}")
        print(f"👥 Total employees: {len(employee_dim):,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n⚠️  Data generation failed. Please check the error messages above.")
        input("Press Enter to exit...")
    else:
        print("\n✅ Ready for Power BI import!")
        print("\nNext steps:")
        print("1. Go to https://app.powerbi.com")
        print("2. Create a new workspace")
        print("3. Upload the CSV files from the data folder")
        print("4. Create your dashboard!")