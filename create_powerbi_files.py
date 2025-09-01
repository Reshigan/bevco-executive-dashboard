#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Power BI File Creator
Creates complete Power BI files ready for import into Power BI Desktop
"""

import os
import sys
import subprocess
from pathlib import Path

def print_status(message, status="info"):
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

def main():
    """Main function"""
    print("📊 Bevco Dashboard - Power BI File Creator")
    print("=" * 50)
    print("Create complete Power BI files ready for import")
    print()
    
    print("Choose the type of Power BI files to create:")
    print()
    print("1. 📋 PBIT Templates (Recommended)")
    print("   • Power BI Template files (.pbit)")
    print("   • Double-click to open in Power BI Desktop")
    print("   • Automatically prompts for data source")
    print("   • Includes complete data model and DAX measures")
    print("   • 4 specialized templates for different roles")
    print()
    print("2. 📊 PBIX Files (Advanced)")
    print("   • Complete Power BI Desktop files (.pbix)")
    print("   • Includes embedded data and visualizations")
    print("   • Larger file sizes but complete solutions")
    print("   • Ready-to-use dashboards with sample data")
    print()
    print("3. 🌐 Web-based Template Creator")
    print("   • Browser-based template creation")
    print("   • Mac-optimized interface")
    print("   • Generate and download templates online")
    print()
    print("4. 📖 View Documentation")
    print("   • Usage guides and instructions")
    print("   • Troubleshooting help")
    print("   • Implementation examples")
    print()
    
    try:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            print()
            print_status("Creating PBIT Template files...", "info")
            print("This will create 4 specialized Power BI Template files:")
            print("• BevcoExecutiveDashboard.pbit - Complete executive dashboard")
            print("• BevcoSalesAnalysis.pbit - Sales-focused dashboard")
            print("• BevcoFinancialReporting.pbit - Financial dashboard")
            print("• BevcoOperationalMetrics.pbit - Operational dashboard")
            print()
            
            confirm = input("Continue? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                result = subprocess.run([
                    sys.executable, 
                    "scripts/create_pbit_templates.py"
                ], cwd=os.getcwd())
                
                if result.returncode == 0:
                    print()
                    print_status("PBIT templates created successfully!", "success")
                    print("📁 Location: pbit_templates/")
                    print("📖 Usage guide: pbit_templates/PBIT_USAGE_GUIDE.md")
                    print()
                    print("🚀 Next steps:")
                    print("1. Double-click any .pbit file to open in Power BI Desktop")
                    print("2. Point to your CSV files when prompted")
                    print("3. Customize and publish to Power BI Service")
                else:
                    print_status("PBIT template creation failed", "error")
                    return 1
            else:
                print("Operation cancelled.")
        
        elif choice == "2":
            print()
            print_status("Creating PBIX files...", "info")
            print("This will create complete Power BI Desktop files with embedded data.")
            print("Note: PBIX creation is more complex and may require additional setup.")
            print()
            
            confirm = input("Continue? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                result = subprocess.run([
                    sys.executable, 
                    "scripts/create_pbix_files.py"
                ], cwd=os.getcwd())
                
                if result.returncode == 0:
                    print()
                    print_status("PBIX files created successfully!", "success")
                    print("📁 Location: pbix_files/")
                    print("📖 Usage guide: pbix_files/PBIX_IMPORT_INSTRUCTIONS.md")
                else:
                    print_status("PBIX file creation failed", "error")
                    return 1
            else:
                print("Operation cancelled.")
        
        elif choice == "3":
            print()
            print_status("Starting web-based template creator...", "info")
            print("This will open a browser-based interface for creating templates.")
            print()
            
            try:
                result = subprocess.run([
                    sys.executable, 
                    "scripts/mac_web_server.py"
                ], cwd=os.getcwd())
            except KeyboardInterrupt:
                print()
                print_status("Web server stopped", "info")
        
        elif choice == "4":
            print()
            print_status("Opening documentation...", "info")
            print()
            print("📖 Available Documentation:")
            print("• README.md - Main project documentation")
            print("• MAC_SETUP_GUIDE.md - Mac-specific setup guide")
            print("• ONLINE_POWERBI_SETUP.md - Online Power BI setup")
            print("• AUTHENTICATION_SOLUTIONS.md - Auth troubleshooting")
            print("• POWERBI_IMPLEMENTATION_GUIDE.md - Complete implementation guide")
            print()
            
            # Try to open main documentation
            docs_to_open = [
                "README.md",
                "MAC_SETUP_GUIDE.md",
                "AUTHENTICATION_SOLUTIONS.md"
            ]
            
            for doc in docs_to_open:
                if Path(doc).exists():
                    print(f"📄 {doc}")
                    try:
                        if sys.platform == "darwin":  # macOS
                            subprocess.run(["open", doc])
                        elif sys.platform == "win32":  # Windows
                            subprocess.run(["start", doc], shell=True)
                        else:  # Linux
                            subprocess.run(["xdg-open", doc])
                    except:
                        print(f"   Please manually open: {doc}")
            
            print()
            print("🌐 GitHub Repository: https://github.com/Reshigan/bevco-executive-dashboard")
        
        else:
            print("Invalid choice. Please run the script again and choose 1-4.")
            return 1
    
    except KeyboardInterrupt:
        print()
        print_status("Operation cancelled by user", "warning")
        return 0
    except Exception as e:
        print_status(f"Error: {e}", "error")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())