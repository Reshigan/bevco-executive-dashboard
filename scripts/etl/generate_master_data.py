import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define output directory - use relative path from script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
output_dir = os.path.join(project_root, "data", "master")

# Create output directory if it doesn't exist
try:
    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ Output directory: {output_dir}")
except OSError as e:
    print(f"✗ Error creating directory {output_dir}: {e}")
    # Fallback to current directory
    output_dir = os.path.join(os.getcwd(), "data", "master")
    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ Using fallback directory: {output_dir}")

# Generate Date Dimension
def generate_date_dimension():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    date_dim = pd.DataFrame({
        'DateKey': dates.strftime('%Y%m%d').astype(int),
        'Date': dates,
        'Year': dates.year,
        'Quarter': dates.quarter,
        'Month': dates.month,
        'MonthName': dates.strftime('%B'),
        'Week': dates.isocalendar().week,
        'DayOfWeek': dates.dayofweek + 1,
        'DayName': dates.strftime('%A'),
        'DayOfMonth': dates.day,
        'DayOfYear': dates.dayofyear,
        'IsWeekend': (dates.dayofweek >= 5).astype(int),
        'IsHoliday': 0,  # Would need SA holiday calendar
        'FiscalYear': dates.year,
        'FiscalQuarter': dates.quarter,
        'FiscalMonth': dates.month
    })
    
    return date_dim

# Generate Product Dimension
def generate_product_dimension():
    vendors = ['Coca-Cola', 'SABMiller', 'Distell', 'Heineken', 'Diageo']
    
    categories = {
        'Soft Drinks': ['Cola', 'Lemon-Lime', 'Orange', 'Energy', 'Water'],
        'Beer': ['Lager', 'Ale', 'Stout', 'Craft', 'Light'],
        'Spirits': ['Whiskey', 'Vodka', 'Rum', 'Gin', 'Brandy'],
        'Wine': ['Red', 'White', 'Sparkling', 'Rose', 'Fortified']
    }
    
    products = []
    product_id = 1000
    
    for vendor in vendors:
        for category, subcategories in categories.items():
            for subcat in subcategories:
                # Generate 2-5 products per subcategory
                num_products = random.randint(2, 5)
                for i in range(num_products):
                    product = {
                        'ProductKey': product_id,
                        'SKU': f'SKU{product_id}',
                        'ProductName': f'{vendor} {subcat} {i+1}',
                        'Vendor': vendor,
                        'Category': category,
                        'SubCategory': subcat,
                        'Brand': vendor,
                        'PackSize': random.choice(['330ml', '500ml', '750ml', '1L', '2L', '6-pack', '12-pack']),
                        'UnitCost': round(random.uniform(5, 50), 2),
                        'UnitPrice': round(random.uniform(10, 100), 2),
                        'LaunchDate': datetime(2022, random.randint(1, 12), random.randint(1, 28)),
                        'Status': random.choice(['Active', 'Active', 'Active', 'Discontinued'])
                    }
                    products.append(product)
                    product_id += 1
    
    return pd.DataFrame(products)

# Generate Customer Dimension
def generate_customer_dimension():
    channels = ['Retail', 'Wholesale', 'On-Trade', 'E-Commerce']
    regions = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Mpumalanga', 'Limpopo', 'Free State', 'North West', 'Northern Cape']
    
    customer_types = {
        'Retail': ['Supermarket', 'Convenience Store', 'Bottle Store', 'Hypermarket'],
        'Wholesale': ['Cash & Carry', 'Distributor', 'Wholesaler'],
        'On-Trade': ['Restaurant', 'Bar', 'Hotel', 'Club'],
        'E-Commerce': ['Online Retailer', 'Marketplace', 'Direct-to-Consumer']
    }
    
    customers = []
    customer_id = 1
    
    for region in regions:
        for channel in channels:
            # Generate 10-30 customers per channel per region
            num_customers = random.randint(10, 30)
            for i in range(num_customers):
                customer_type = random.choice(customer_types[channel])
                customer = {
                    'CustomerKey': customer_id,
                    'CustomerCode': f'CUST{customer_id:05d}',
                    'CustomerName': f'{customer_type} {region} {i+1}',
                    'Channel': channel,
                    'CustomerType': customer_type,
                    'Region': region,
                    'Province': region,
                    'City': f'{region} City {random.randint(1, 5)}',
                    'CreditLimit': random.randint(10000, 500000),
                    'PaymentTerms': random.choice([7, 14, 30, 45]),
                    'Status': random.choice(['Active', 'Active', 'Active', 'Inactive']),
                    'OnboardingDate': datetime(2022, random.randint(1, 12), random.randint(1, 28))
                }
                customers.append(customer)
                customer_id += 1
    
    return pd.DataFrame(customers)

# Generate Employee Dimension
def generate_employee_dimension():
    departments = ['Sales', 'Operations', 'Finance', 'Marketing', 'IT', 'HR', 'Supply Chain', 'Customer Service']
    positions = {
        'Sales': ['Sales Rep', 'Sales Manager', 'Regional Sales Manager', 'Sales Director'],
        'Operations': ['Operations Analyst', 'Operations Manager', 'Operations Director'],
        'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager', 'CFO'],
        'Marketing': ['Marketing Coordinator', 'Brand Manager', 'Marketing Director'],
        'IT': ['Developer', 'System Administrator', 'IT Manager', 'CTO'],
        'HR': ['HR Coordinator', 'HR Manager', 'HR Director'],
        'Supply Chain': ['Supply Chain Analyst', 'Logistics Manager', 'Supply Chain Director'],
        'Customer Service': ['Customer Service Rep', 'Customer Service Manager']
    }
    
    employees = []
    employee_id = 1000
    
    # Add C-Suite
    c_suite = [
        {'EmployeeKey': employee_id, 'EmployeeCode': f'EMP{employee_id}', 'Name': 'John Smith', 
         'Position': 'CEO', 'Department': 'Executive', 'ReportsTo': None, 'HireDate': datetime(2020, 1, 15)},
        {'EmployeeKey': employee_id+1, 'EmployeeCode': f'EMP{employee_id+1}', 'Name': 'Sarah Johnson', 
         'Position': 'CFO', 'Department': 'Finance', 'ReportsTo': employee_id, 'HireDate': datetime(2020, 3, 1)},
        {'EmployeeKey': employee_id+2, 'EmployeeCode': f'EMP{employee_id+2}', 'Name': 'Michael Brown', 
         'Position': 'Sales Director', 'Department': 'Sales', 'ReportsTo': employee_id, 'HireDate': datetime(2020, 2, 1)},
        {'EmployeeKey': employee_id+3, 'EmployeeCode': f'EMP{employee_id+3}', 'Name': 'Lisa Davis', 
         'Position': 'Operations Director', 'Department': 'Operations', 'ReportsTo': employee_id, 'HireDate': datetime(2020, 4, 1)}
    ]
    
    employees.extend(c_suite)
    employee_id += 4
    
    # Generate other employees
    for dept, positions_list in positions.items():
        if dept in ['Finance', 'Sales', 'Operations']:  # These already have directors
            positions_list = [p for p in positions_list if 'Director' not in p and 'CFO' not in p]
        
        for position in positions_list:
            num_employees = random.randint(5, 20)
            for i in range(num_employees):
                manager_id = [e['EmployeeKey'] for e in employees if e['Department'] == dept and 'Manager' in e['Position']]
                if not manager_id and 'Manager' not in position and 'Director' not in position:
                    manager_id = [e['EmployeeKey'] for e in employees if e['Department'] == dept and 'Director' in e['Position']]
                
                employee = {
                    'EmployeeKey': employee_id,
                    'EmployeeCode': f'EMP{employee_id}',
                    'Name': f'{random.choice(["John", "Jane", "Mike", "Sarah", "Tom", "Lisa"])} {random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Davis"])} {employee_id}',
                    'Position': position,
                    'Department': dept,
                    'ReportsTo': manager_id[0] if manager_id else None,
                    'HireDate': datetime(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)),
                    'Salary': random.randint(30000, 200000),
                    'EmploymentType': random.choice(['Full-time', 'Full-time', 'Full-time', 'Contract'])
                }
                employees.append(employee)
                employee_id += 1
    
    return pd.DataFrame(employees)

# Generate Sales Fact Table
def generate_sales_facts(date_dim, product_dim, customer_dim, employee_dim):
    print("  Generating sales transactions...")
    
    # Get sales reps
    sales_reps = employee_dim[employee_dim['Position'].str.contains('Sales Rep')]['EmployeeKey'].tolist()
    
    # Get active customers and products
    active_customers = customer_dim[customer_dim['Status'] == 'Active']
    active_products = product_dim[product_dim['Status'] == 'Active']
    
    # Generate daily sales for 2024 (limit to first 6 months for sample data)
    dates_2024 = date_dim[(date_dim['Year'] == 2024) & (date_dim['Month'] <= 6)]['DateKey'].tolist()
    
    # Pre-generate random data for efficiency
    total_days = len(dates_2024)
    avg_transactions_per_day = 200
    total_transactions = total_days * avg_transactions_per_day
    
    print(f"  Creating {total_transactions} sales transactions for {total_days} days...")
    
    # Generate all sales data at once using vectorized operations
    sales_data = {
        'SalesKey': range(1, total_transactions + 1),
        'DateKey': np.repeat(dates_2024, avg_transactions_per_day),
        'ProductKey': np.random.choice(active_products['ProductKey'].values, total_transactions),
        'CustomerKey': np.random.choice(active_customers['CustomerKey'].values, total_transactions),
        'EmployeeKey': np.random.choice(sales_reps, total_transactions) if sales_reps else [None] * total_transactions,
        'Quantity': np.random.randint(1, 100, total_transactions),
        'DiscountPercent': np.random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20], total_transactions)
    }
    
    # Create DataFrame
    sales_df = pd.DataFrame(sales_data)
    
    # Merge with product data to get prices
    sales_df = sales_df.merge(product_dim[['ProductKey', 'UnitPrice', 'UnitCost']], on='ProductKey', how='left')
    
    # Calculate financial metrics
    sales_df['GrossSales'] = sales_df['Quantity'] * sales_df['UnitPrice']
    sales_df['DiscountAmount'] = sales_df['GrossSales'] * sales_df['DiscountPercent']
    sales_df['NetSales'] = sales_df['GrossSales'] - sales_df['DiscountAmount']
    sales_df['Cost'] = sales_df['Quantity'] * sales_df['UnitCost']
    sales_df['GrossProfit'] = sales_df['NetSales'] - sales_df['Cost']
    
    # Generate invoice numbers
    sales_df['InvoiceNumber'] = sales_df.apply(lambda x: f"INV{int(x['DateKey'])}{int(x['SalesKey']):05d}", axis=1)
    
    # Round financial columns
    financial_cols = ['GrossSales', 'DiscountAmount', 'NetSales', 'Cost', 'GrossProfit']
    sales_df[financial_cols] = sales_df[financial_cols].round(2)
    
    print(f"  Sales data generation completed!")
    
    return sales_df

# Generate Budget Data
def generate_budget_data(date_dim):
    budget_data = []
    
    months_2024 = date_dim[(date_dim['Year'] == 2024) & (date_dim['DayOfMonth'] == 1)][['DateKey', 'Year', 'Month']].drop_duplicates()
    
    departments = ['Sales', 'Operations', 'Finance', 'Marketing', 'IT', 'HR', 'Supply Chain', 'Customer Service']
    
    for _, month in months_2024.iterrows():
        for dept in departments:
            # Base budget varies by department
            base_budgets = {
                'Sales': 5000000,
                'Operations': 3000000,
                'Finance': 1000000,
                'Marketing': 2000000,
                'IT': 1500000,
                'HR': 800000,
                'Supply Chain': 2500000,
                'Customer Service': 1200000
            }
            
            base = base_budgets.get(dept, 1000000)
            variance = random.uniform(0.9, 1.1)
            
            budget = {
                'BudgetKey': len(budget_data) + 1,
                'DateKey': month['DateKey'],
                'Year': month['Year'],
                'Month': month['Month'],
                'Department': dept,
                'BudgetAmount': round(base * variance, 2),
                'ForecastAmount': round(base * variance * random.uniform(0.95, 1.05), 2),
                'ActualAmount': round(base * variance * random.uniform(0.85, 1.15), 2) if month['Month'] <= datetime.now().month else None
            }
            budget_data.append(budget)
    
    return pd.DataFrame(budget_data)

# Generate Inventory Data
def generate_inventory_data(product_dim):
    inventory_data = []
    
    warehouses = ['Johannesburg DC', 'Cape Town DC', 'Durban DC', 'Port Elizabeth DC', 'Pretoria DC']
    
    for warehouse in warehouses:
        for _, product in product_dim[product_dim['Status'] == 'Active'].iterrows():
            # Generate current inventory levels
            stock_on_hand = random.randint(0, 10000)
            reorder_point = random.randint(100, 1000)
            max_stock = random.randint(5000, 20000)
            
            inventory = {
                'InventoryKey': len(inventory_data) + 1,
                'ProductKey': product['ProductKey'],
                'Warehouse': warehouse,
                'StockOnHand': stock_on_hand,
                'ReorderPoint': reorder_point,
                'MaxStock': max_stock,
                'StockValue': round(stock_on_hand * product['UnitCost'], 2),
                'DaysOnHand': random.randint(1, 90),
                'LastUpdated': datetime.now()
            }
            inventory_data.append(inventory)
    
    return pd.DataFrame(inventory_data)

# Generate KPI Targets
def generate_kpi_targets():
    kpis = [
        {'KPIName': 'Net Sales', 'Target': 150000000, 'Unit': 'ZAR', 'Frequency': 'Monthly'},
        {'KPIName': 'Gross Profit Margin', 'Target': 35, 'Unit': '%', 'Frequency': 'Monthly'},
        {'KPIName': 'Operating Profit', 'Target': 30000000, 'Unit': 'ZAR', 'Frequency': 'Monthly'},
        {'KPIName': 'Net Profit', 'Target': 20000000, 'Unit': 'ZAR', 'Frequency': 'Monthly'},
        {'KPIName': 'Cash Flow', 'Target': 25000000, 'Unit': 'ZAR', 'Frequency': 'Monthly'},
        {'KPIName': 'Working Capital Days', 'Target': 45, 'Unit': 'Days', 'Frequency': 'Monthly'},
        {'KPIName': 'Market Share', 'Target': 25, 'Unit': '%', 'Frequency': 'Quarterly'},
        {'KPIName': 'Customer Satisfaction', 'Target': 85, 'Unit': 'Score', 'Frequency': 'Monthly'},
        {'KPIName': 'Inventory Turnover', 'Target': 12, 'Unit': 'Times', 'Frequency': 'Monthly'},
        {'KPIName': 'OTIF Delivery', 'Target': 95, 'Unit': '%', 'Frequency': 'Weekly'},
        {'KPIName': 'Employee Turnover', 'Target': 10, 'Unit': '%', 'Frequency': 'Quarterly'},
        {'KPIName': 'Revenue per Employee', 'Target': 2000000, 'Unit': 'ZAR', 'Frequency': 'Annual'}
    ]
    
    return pd.DataFrame(kpis)

# Main execution
if __name__ == "__main__":
    print("Generating master data for Bevco Executive Dashboard...")
    
    # Generate dimensions
    print("Creating Date Dimension...")
    date_dim = generate_date_dimension()
    date_dim.to_csv(f"{output_dir}/dim_date.csv", index=False)
    
    print("Creating Product Dimension...")
    product_dim = generate_product_dimension()
    product_dim.to_csv(f"{output_dir}/dim_product.csv", index=False)
    
    print("Creating Customer Dimension...")
    customer_dim = generate_customer_dimension()
    customer_dim.to_csv(f"{output_dir}/dim_customer.csv", index=False)
    
    print("Creating Employee Dimension...")
    employee_dim = generate_employee_dimension()
    employee_dim.to_csv(f"{output_dir}/dim_employee.csv", index=False)
    
    # Generate fact tables
    print("Creating Sales Facts...")
    sales_facts = generate_sales_facts(date_dim, product_dim, customer_dim, employee_dim)
    sales_facts.to_csv(f"{output_dir}/fact_sales.csv", index=False)
    
    print("Creating Budget Data...")
    budget_data = generate_budget_data(date_dim)
    budget_data.to_csv(f"{output_dir}/fact_budget.csv", index=False)
    
    print("Creating Inventory Data...")
    inventory_data = generate_inventory_data(product_dim)
    inventory_data.to_csv(f"{output_dir}/fact_inventory.csv", index=False)
    
    print("Creating KPI Targets...")
    kpi_targets = generate_kpi_targets()
    kpi_targets.to_csv(f"{output_dir}/dim_kpi_targets.csv", index=False)
    
    # Generate summary statistics
    print("\nData Generation Summary:")
    print(f"Date records: {len(date_dim)}")
    print(f"Products: {len(product_dim)}")
    print(f"Customers: {len(customer_dim)}")
    print(f"Employees: {len(employee_dim)}")
    print(f"Sales transactions: {len(sales_facts)}")
    print(f"Budget records: {len(budget_data)}")
    print(f"Inventory records: {len(inventory_data)}")
    print(f"KPI targets: {len(kpi_targets)}")
    
    print("\nMaster data generation completed successfully!")
    print(f"Files saved to: {output_dir}")