#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Python Automation Script
Generates data, creates dashboards, and publishes to Power BI Service automatically
"""

import requests
import json
import time
import os
import pandas as pd
from datetime import datetime
import subprocess
import sys

class PowerBIAutomation:
    def __init__(self, tenant_id=None, client_id=None, client_secret=None):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.base_url = "https://api.powerbi.com/v1.0/myorg"
        
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
    
    def get_access_token(self):
        """Get access token for Power BI API"""
        self.print_status("Getting Power BI access token...", "info")
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            self.print_status("Service principal credentials not provided. Using device code flow...", "warning")
            return self.get_device_code_token()
        
        # Service Principal authentication
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        
        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.print_status("Access token obtained successfully", "success")
            return True
            
        except requests.exceptions.RequestException as e:
            self.print_status(f"Failed to get access token: {e}", "error")
            return False
    
    def get_device_code_token(self):
        """Get access token using device code flow (interactive)"""
        device_code_url = "https://login.microsoftonline.com/common/oauth2/v2.0/devicecode"
        
        data = {
            'client_id': '871c010f-5e61-4fb1-83ac-98610a7e9110',  # Power BI CLI client ID
            'scope': 'https://analysis.windows.net/powerbi/api/Dataset.ReadWrite.All https://analysis.windows.net/powerbi/api/Report.ReadWrite.All https://analysis.windows.net/powerbi/api/Dashboard.ReadWrite.All'
        }
        
        try:
            response = requests.post(device_code_url, data=data)
            response.raise_for_status()
            
            device_data = response.json()
            
            print(f"\n🔐 AUTHENTICATION REQUIRED")
            print(f"Go to: {device_data['verification_uri']}")
            print(f"Enter code: {device_data['user_code']}")
            print(f"Waiting for authentication...")
            
            # Poll for token
            token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
            poll_data = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                'client_id': '871c010f-5e61-4fb1-83ac-98610a7e9110',
                'device_code': device_data['device_code']
            }
            
            timeout = time.time() + device_data['expires_in']
            interval = device_data['interval']
            
            while time.time() < timeout:
                time.sleep(interval)
                
                token_response = requests.post(token_url, data=poll_data)
                token_result = token_response.json()
                
                if 'access_token' in token_result:
                    self.access_token = token_result['access_token']
                    self.print_status("Authentication successful!", "success")
                    return True
                elif token_result.get('error') == 'authorization_pending':
                    continue
                else:
                    self.print_status(f"Authentication failed: {token_result.get('error_description', 'Unknown error')}", "error")
                    return False
            
            self.print_status("Authentication timed out", "error")
            return False
            
        except requests.exceptions.RequestException as e:
            self.print_status(f"Device code authentication failed: {e}", "error")
            return False
    
    def get_headers(self):
        """Get HTTP headers with authorization"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def generate_sample_data(self):
        """Generate sample data using the standalone script"""
        self.print_status("Generating sample data...", "info")
        
        try:
            # Run the standalone data generator
            result = subprocess.run([sys.executable, 'generate_data_standalone.py'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.print_status("Sample data generated successfully", "success")
                return True
            else:
                self.print_status(f"Data generation failed: {result.stderr}", "error")
                return False
                
        except Exception as e:
            self.print_status(f"Error generating data: {e}", "error")
            return False
    
    def create_workspace(self, workspace_name):
        """Create or get Power BI workspace"""
        self.print_status(f"Setting up workspace: {workspace_name}", "info")
        
        # Check if workspace exists
        try:
            response = requests.get(f"{self.base_url}/groups", headers=self.get_headers())
            response.raise_for_status()
            
            workspaces = response.json()['value']
            existing_workspace = next((ws for ws in workspaces if ws['name'] == workspace_name), None)
            
            if existing_workspace:
                self.print_status(f"Using existing workspace: {workspace_name}", "success")
                return existing_workspace
            
            # Create new workspace
            workspace_data = {
                'name': workspace_name,
                'description': 'Bevco Executive Dashboard - Automated deployment'
            }
            
            response = requests.post(f"{self.base_url}/groups", 
                                   headers=self.get_headers(), 
                                   json=workspace_data)
            response.raise_for_status()
            
            workspace = response.json()
            self.print_status(f"Workspace created successfully: {workspace_name}", "success")
            return workspace
            
        except requests.exceptions.RequestException as e:
            self.print_status(f"Failed to create workspace: {e}", "error")
            return None
    
    def upload_dataset(self, workspace_id, file_path, dataset_name):
        """Upload dataset to Power BI workspace"""
        self.print_status(f"Uploading dataset: {dataset_name}", "info")
        
        try:
            # For CSV files, we need to create a streaming dataset or use dataflows
            # For now, we'll create a push dataset with sample schema
            
            # Define dataset schema based on our data model
            dataset_schema = {
                "name": dataset_name,
                "tables": [
                    {
                        "name": "Sales",
                        "columns": [
                            {"name": "SalesKey", "dataType": "Int64"},
                            {"name": "DateKey", "dataType": "Int64"},
                            {"name": "ProductKey", "dataType": "Int64"},
                            {"name": "CustomerKey", "dataType": "Int64"},
                            {"name": "NetSales", "dataType": "Double"},
                            {"name": "GrossProfit", "dataType": "Double"},
                            {"name": "Quantity", "dataType": "Int64"}
                        ]
                    },
                    {
                        "name": "Products",
                        "columns": [
                            {"name": "ProductKey", "dataType": "Int64"},
                            {"name": "ProductName", "dataType": "String"},
                            {"name": "Category", "dataType": "String"},
                            {"name": "UnitPrice", "dataType": "Double"}
                        ]
                    },
                    {
                        "name": "Customers",
                        "columns": [
                            {"name": "CustomerKey", "dataType": "Int64"},
                            {"name": "CustomerName", "dataType": "String"},
                            {"name": "Region", "dataType": "String"},
                            {"name": "Channel", "dataType": "String"}
                        ]
                    },
                    {
                        "name": "Dates",
                        "columns": [
                            {"name": "DateKey", "dataType": "Int64"},
                            {"name": "Date", "dataType": "DateTime"},
                            {"name": "Year", "dataType": "Int64"},
                            {"name": "Month", "dataType": "Int64"},
                            {"name": "MonthName", "dataType": "String"}
                        ]
                    }
                ]
            }
            
            # Create dataset
            response = requests.post(f"{self.base_url}/groups/{workspace_id}/datasets",
                                   headers=self.get_headers(),
                                   json=dataset_schema)
            response.raise_for_status()
            
            dataset = response.json()
            self.print_status(f"Dataset created: {dataset_name}", "success")
            
            # Load sample data into the dataset
            self.load_sample_data_to_dataset(workspace_id, dataset['id'])
            
            return dataset
            
        except requests.exceptions.RequestException as e:
            self.print_status(f"Failed to upload dataset: {e}", "error")
            return None
    
    def load_sample_data_to_dataset(self, workspace_id, dataset_id):
        """Load sample data into Power BI dataset"""
        self.print_status("Loading sample data into dataset...", "info")
        
        try:
            # Load CSV files and push data to Power BI
            data_dir = os.path.join(os.getcwd(), 'data', 'master')
            
            # Load and push sales data
            if os.path.exists(os.path.join(data_dir, 'fact_sales.csv')):
                sales_df = pd.read_csv(os.path.join(data_dir, 'fact_sales.csv'))
                # Take first 1000 rows for demo (API has limits)
                sales_sample = sales_df.head(1000)
                
                sales_data = {
                    "rows": sales_sample[['SalesKey', 'DateKey', 'ProductKey', 'CustomerKey', 'NetSales', 'GrossProfit', 'Quantity']].to_dict('records')
                }
                
                response = requests.post(f"{self.base_url}/groups/{workspace_id}/datasets/{dataset_id}/tables/Sales/rows",
                                       headers=self.get_headers(),
                                       json=sales_data)
                
                if response.status_code == 200:
                    self.print_status("Sales data loaded successfully", "success")
            
            # Load products data
            if os.path.exists(os.path.join(data_dir, 'dim_product.csv')):
                products_df = pd.read_csv(os.path.join(data_dir, 'dim_product.csv'))
                products_data = {
                    "rows": products_df[['ProductKey', 'ProductName', 'Category', 'UnitPrice']].to_dict('records')
                }
                
                response = requests.post(f"{self.base_url}/groups/{workspace_id}/datasets/{dataset_id}/tables/Products/rows",
                                       headers=self.get_headers(),
                                       json=products_data)
                
                if response.status_code == 200:
                    self.print_status("Products data loaded successfully", "success")
            
            # Load customers data
            if os.path.exists(os.path.join(data_dir, 'dim_customer.csv')):
                customers_df = pd.read_csv(os.path.join(data_dir, 'dim_customer.csv'))
                customers_data = {
                    "rows": customers_df[['CustomerKey', 'CustomerName', 'Region', 'Channel']].to_dict('records')
                }
                
                response = requests.post(f"{self.base_url}/groups/{workspace_id}/datasets/{dataset_id}/tables/Customers/rows",
                                       headers=self.get_headers(),
                                       json=customers_data)
                
                if response.status_code == 200:
                    self.print_status("Customers data loaded successfully", "success")
            
            # Load dates data
            if os.path.exists(os.path.join(data_dir, 'dim_date.csv')):
                dates_df = pd.read_csv(os.path.join(data_dir, 'dim_date.csv'))
                # Convert date strings to proper format
                dates_df['Date'] = pd.to_datetime(dates_df['Date']).dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                
                dates_data = {
                    "rows": dates_df[['DateKey', 'Date', 'Year', 'Month', 'MonthName']].to_dict('records')
                }
                
                response = requests.post(f"{self.base_url}/groups/{workspace_id}/datasets/{dataset_id}/tables/Dates/rows",
                                       headers=self.get_headers(),
                                       json=dates_data)
                
                if response.status_code == 200:
                    self.print_status("Dates data loaded successfully", "success")
            
        except Exception as e:
            self.print_status(f"Error loading sample data: {e}", "warning")
    
    def create_dashboard(self, workspace_id, dashboard_name):
        """Create Power BI dashboard"""
        self.print_status(f"Creating dashboard: {dashboard_name}", "info")
        
        try:
            dashboard_data = {
                'name': dashboard_name
            }
            
            response = requests.post(f"{self.base_url}/groups/{workspace_id}/dashboards",
                                   headers=self.get_headers(),
                                   json=dashboard_data)
            response.raise_for_status()
            
            dashboard = response.json()
            self.print_status(f"Dashboard created: {dashboard_name}", "success")
            return dashboard
            
        except requests.exceptions.RequestException as e:
            self.print_status(f"Failed to create dashboard: {e}", "error")
            return None
    
    def create_report(self, workspace_id, dataset_id, report_name):
        """Create Power BI report"""
        self.print_status(f"Creating report: {report_name}", "info")
        
        try:
            report_data = {
                'name': report_name,
                'datasetId': dataset_id
            }
            
            response = requests.post(f"{self.base_url}/groups/{workspace_id}/reports",
                                   headers=self.get_headers(),
                                   json=report_data)
            response.raise_for_status()
            
            report = response.json()
            self.print_status(f"Report created: {report_name}", "success")
            return report
            
        except requests.exceptions.RequestException as e:
            self.print_status(f"Failed to create report: {e}", "error")
            return None
    
    def run_full_automation(self, workspace_name="Bevco Executive Dashboard"):
        """Run the complete automation process"""
        print("🚀 Bevco Dashboard - Full Python Automation")
        print("=" * 50)
        
        # Step 1: Generate sample data
        if not self.generate_sample_data():
            return False
        
        # Step 2: Get access token
        if not self.get_access_token():
            return False
        
        # Step 3: Create workspace
        workspace = self.create_workspace(workspace_name)
        if not workspace:
            return False
        
        # Step 4: Upload dataset
        dataset = self.upload_dataset(workspace['id'], None, "Bevco Data")
        if not dataset:
            return False
        
        # Step 5: Create dashboard
        dashboard = self.create_dashboard(workspace['id'], "Bevco Executive Dashboard")
        
        # Step 6: Create report
        report = self.create_report(workspace['id'], dataset['id'], "Bevco Executive Report")
        
        # Display results
        print("\n🎉 AUTOMATION COMPLETE!")
        print("=" * 30)
        print(f"Workspace: {workspace['name']}")
        print(f"Workspace URL: https://app.powerbi.com/groups/{workspace['id']}")
        
        if dashboard:
            print(f"Dashboard: {dashboard['displayName']}")
            print(f"Dashboard URL: https://app.powerbi.com/groups/{workspace['id']}/dashboards/{dashboard['id']}")
        
        if report:
            print(f"Report: {report['name']}")
            print(f"Report URL: https://app.powerbi.com/groups/{workspace['id']}/reports/{report['id']}")
        
        print("\n📊 Sample Data Generated:")
        print("• Sales transactions with realistic data")
        print("• Product catalog with South African beverages")
        print("• Customer data across 9 regions")
        print("• Complete business intelligence dataset")
        
        print("\n🚀 Next Steps:")
        print("1. Open the workspace URL above")
        print("2. Customize your dashboard and reports")
        print("3. Add more visualizations")
        print("4. Share with your team")
        
        return True

def main():
    """Main function to run automation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bevco Dashboard Power BI Automation')
    parser.add_argument('--tenant-id', help='Azure AD Tenant ID')
    parser.add_argument('--client-id', help='Azure AD Client ID')
    parser.add_argument('--client-secret', help='Azure AD Client Secret')
    parser.add_argument('--workspace', default='Bevco Executive Dashboard', help='Power BI Workspace Name')
    
    args = parser.parse_args()
    
    # Create automation instance
    automation = PowerBIAutomation(
        tenant_id=args.tenant_id,
        client_id=args.client_id,
        client_secret=args.client_secret
    )
    
    # Run automation
    success = automation.run_full_automation(args.workspace)
    
    if success:
        print("\n✅ Full automation completed successfully!")
    else:
        print("\n❌ Automation failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())