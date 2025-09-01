#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Web-based Automation
Uses Selenium to automate Power BI Service web interface directly
This bypasses API authentication issues
"""

import time
import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class PowerBIWebAutomation:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.wait_timeout = 30
        
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
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        self.print_status("Setting up web browser...", "info")
        
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Try to create driver
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception:
                # If Chrome driver not found, try to install it
                self.print_status("Chrome driver not found. Installing...", "warning")
                subprocess.run([sys.executable, "-m", "pip", "install", "webdriver-manager"], check=True)
                
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.driver.implicitly_wait(10)
            self.print_status("Browser ready", "success")
            return True
            
        except Exception as e:
            self.print_status(f"Failed to setup browser: {e}", "error")
            return False
    
    def generate_sample_data(self):
        """Generate sample data using the standalone script"""
        self.print_status("Generating sample data...", "info")
        
        try:
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
    
    def login_to_powerbi(self):
        """Navigate to Power BI and handle login"""
        self.print_status("Opening Power BI Service...", "info")
        
        try:
            self.driver.get("https://app.powerbi.com")
            
            # Wait for page to load
            WebDriverWait(self.driver, self.wait_timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Check if already logged in
            try:
                # Look for workspace navigation or home page elements
                WebDriverWait(self.driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='nav-workspaces']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".workspacesList")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Workspaces']"))
                    )
                )
                self.print_status("Already logged in to Power BI", "success")
                return True
                
            except TimeoutException:
                # Need to login
                self.print_status("Please log in to Power BI in the browser window", "warning")
                print("\n🔐 MANUAL LOGIN REQUIRED")
                print("=" * 40)
                print("1. A browser window has opened")
                print("2. Please log in to Power BI with your credentials")
                print("3. Wait for the Power BI home page to load")
                print("4. Press Enter here when you're logged in")
                
                input("\nPress Enter after logging in...")
                
                # Verify login was successful
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='nav-workspaces']")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".workspacesList")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Workspaces']"))
                        )
                    )
                    self.print_status("Login successful!", "success")
                    return True
                    
                except TimeoutException:
                    self.print_status("Login verification failed. Please ensure you're logged in.", "error")
                    return False
            
        except Exception as e:
            self.print_status(f"Error accessing Power BI: {e}", "error")
            return False
    
    def create_workspace(self, workspace_name):
        """Create a new workspace"""
        self.print_status(f"Creating workspace: {workspace_name}", "info")
        
        try:
            # Navigate to workspaces
            try:
                workspaces_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='nav-workspaces'], [aria-label='Workspaces']"))
                )
                workspaces_button.click()
            except TimeoutException:
                # Try alternative selector
                self.driver.find_element(By.XPATH, "//span[contains(text(), 'Workspaces')]").click()
            
            time.sleep(2)
            
            # Click "Create a workspace" or "New workspace"
            try:
                create_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create a workspace') or contains(text(), 'New workspace')]"))
                )
                create_button.click()
            except TimeoutException:
                # Try clicking the + button
                plus_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Create'], .create-workspace-button")
                plus_button.click()
            
            time.sleep(2)
            
            # Enter workspace name
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='workspace name'], input[aria-label*='Name']"))
            )
            name_input.clear()
            name_input.send_keys(workspace_name)
            
            # Click Save/Create
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Create')]"))
            )
            save_button.click()
            
            # Wait for workspace to be created
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{workspace_name}')]"))
            )
            
            self.print_status(f"Workspace '{workspace_name}' created successfully", "success")
            return True
            
        except Exception as e:
            self.print_status(f"Error creating workspace: {e}", "error")
            return False
    
    def upload_files(self, data_directory):
        """Upload CSV files to the workspace"""
        self.print_status("Uploading data files...", "info")
        
        try:
            csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
            
            for csv_file in csv_files:
                self.print_status(f"Uploading {csv_file}...", "info")
                
                # Click "New" or "Get Data"
                try:
                    new_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New') or contains(text(), 'Get data')]"))
                    )
                    new_button.click()
                except TimeoutException:
                    # Try alternative approach
                    self.driver.find_element(By.CSS_SELECTOR, "[aria-label='New'], .new-button").click()
                
                time.sleep(1)
                
                # Click "Upload a file"
                upload_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Upload a file')]"))
                )
                upload_option.click()
                
                time.sleep(1)
                
                # Click "Local File"
                local_file_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Local File')]"))
                )
                local_file_option.click()
                
                # Upload file
                file_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
                )
                
                file_path = os.path.join(data_directory, csv_file)
                file_input.send_keys(os.path.abspath(file_path))
                
                # Wait for upload to complete
                try:
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), '{csv_file.replace('.csv', '')}')]"))
                    )
                    self.print_status(f"✅ {csv_file} uploaded successfully", "success")
                except TimeoutException:
                    self.print_status(f"⚠️ Upload timeout for {csv_file}", "warning")
                
                time.sleep(2)
            
            return True
            
        except Exception as e:
            self.print_status(f"Error uploading files: {e}", "error")
            return False
    
    def create_basic_report(self):
        """Create a basic report with sample visualizations"""
        self.print_status("Creating sample report...", "info")
        
        try:
            # Look for a dataset to create report from
            try:
                dataset = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'fact_sales') or contains(text(), 'Sales')]"))
                )
                dataset.click()
            except TimeoutException:
                # Try to find any dataset
                datasets = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='dataset-tile'], .dataset-item")
                if datasets:
                    datasets[0].click()
                else:
                    self.print_status("No datasets found to create report", "warning")
                    return False
            
            time.sleep(2)
            
            # Click "Create report"
            create_report_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create report')]"))
            )
            create_report_button.click()
            
            # Wait for report editor to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".visualizations-pane, [data-testid='visualizations-pane']"))
            )
            
            self.print_status("Report editor loaded successfully", "success")
            
            # Give user instructions for manual report building
            print("\n🎨 REPORT BUILDING")
            print("=" * 30)
            print("The Power BI report editor is now open!")
            print("You can now:")
            print("1. Drag fields from the Fields pane to create visualizations")
            print("2. Add KPI cards, charts, and maps")
            print("3. Save your report when done")
            print("4. Create a dashboard from your report")
            
            input("\nPress Enter when you've finished building your report...")
            
            return True
            
        except Exception as e:
            self.print_status(f"Error creating report: {e}", "error")
            return False
    
    def run_automation(self, workspace_name="Bevco Executive Dashboard"):
        """Run the complete web automation"""
        print("🌐 Bevco Dashboard - Web Automation")
        print("=" * 40)
        print("This automation uses browser automation to bypass API authentication issues.")
        print()
        
        try:
            # Step 1: Generate sample data
            if not self.generate_sample_data():
                return False
            
            # Step 2: Setup browser
            if not self.setup_driver():
                return False
            
            # Step 3: Login to Power BI
            if not self.login_to_powerbi():
                return False
            
            # Step 4: Create workspace
            if not self.create_workspace(workspace_name):
                return False
            
            # Step 5: Upload files
            data_dir = os.path.join(os.getcwd(), 'data', 'master')
            if os.path.exists(data_dir):
                if not self.upload_files(data_dir):
                    return False
            else:
                # Try alternative data directory
                data_dir = os.path.join(os.getcwd(), 'master_data')
                if os.path.exists(data_dir):
                    if not self.upload_files(data_dir):
                        return False
                else:
                    self.print_status("No data directory found", "error")
                    return False
            
            # Step 6: Create basic report
            self.create_basic_report()
            
            # Success message
            print("\n🎉 WEB AUTOMATION COMPLETE!")
            print("=" * 35)
            print(f"✅ Workspace created: {workspace_name}")
            print("✅ Data files uploaded")
            print("✅ Report editor opened")
            print()
            print("🚀 Next Steps:")
            print("1. Build your visualizations in the report editor")
            print("2. Save your report")
            print("3. Create a dashboard")
            print("4. Share with your team")
            
            # Keep browser open
            input("\nPress Enter to close the browser...")
            
            return True
            
        except Exception as e:
            self.print_status(f"Automation failed: {e}", "error")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()

def install_selenium():
    """Install Selenium if not available"""
    try:
        import selenium
        return True
    except ImportError:
        print("📦 Installing Selenium...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager"], check=True)
            print("✅ Selenium installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Selenium")
            return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bevco Dashboard Web Automation')
    parser.add_argument('--workspace', default='Bevco Executive Dashboard', help='Power BI Workspace Name')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    # Install Selenium if needed
    if not install_selenium():
        return 1
    
    # Import after installation
    global webdriver, WebDriverWait, EC, By, Options, TimeoutException, NoSuchElementException
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    
    # Run automation
    automation = PowerBIWebAutomation(headless=args.headless)
    success = automation.run_automation(args.workspace)
    
    if success:
        print("\n✅ Web automation completed!")
    else:
        print("\n❌ Web automation failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())