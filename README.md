# Bevco Executive Dashboard 📊

[![Data Quality](https://github.com/Reshigan/bevco-executive-dashboard/actions/workflows/data-quality.yml/badge.svg)](https://github.com/Reshigan/bevco-executive-dashboard/actions/workflows/data-quality.yml)
[![Documentation](https://github.com/Reshigan/bevco-executive-dashboard/actions/workflows/documentation.yml/badge.svg)](https://github.com/Reshigan/bevco-executive-dashboard/actions/workflows/documentation.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Power BI executive dashboard solution for Bevco South Africa, providing real-time visibility of business performance across all organizational levels, from C-suite to operational teams.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Bevco+Executive+Dashboard)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Reshigan/bevco-executive-dashboard.git
cd bevco-executive-dashboard

# Run automated setup (Linux/Mac)
./scripts/setup.sh

# Run automated setup (Windows)
scripts\setup.bat

# Follow the quick start guide
cat QUICKSTART.md
```

## ✨ Key Features

### 📈 Executive Analytics
- **Real-time KPIs**: Monitor business health with live metrics
- **Predictive Insights**: AI-powered forecasting and anomaly detection
- **Multi-level Drill-down**: From executive summary to detailed analysis
- **Mobile Responsive**: Access dashboards on any device

### 📊 Comprehensive Dashboards
- **Executive Summary**: C-suite overview with critical KPIs
- **Sales & Revenue**: Channel, product, and customer analytics
- **Financial Management**: P&L, cash flow, and budget tracking
- **Operations**: Inventory, supply chain, and quality metrics
- **Customer Intelligence**: Segmentation and lifetime value analysis
- **People Analytics**: HR metrics and workforce productivity

### 🔧 Technical Capabilities
- **Automated Data Processing**: ETL scripts for data transformation
- **60+ DAX Measures**: Pre-built calculations for all KPIs
- **Row-Level Security**: Role-based data access control
- **CI/CD Integration**: GitHub Actions for quality assurance
- **Sample Data Generation**: Realistic test data for development

## 📁 Project Structure

```
bevco-executive-dashboard/
├── 📊 data/
│   ├── master/          # Sample master data (8 CSV files)
│   ├── processed/       # Data quality reports
│   └── raw/            # Raw data staging
├── 🔧 scripts/
│   ├── etl/            # Data generation and quality checks
│   ├── setup.sh        # Linux/Mac setup script
│   ├── setup.bat       # Windows setup script
│   └── *.ps1           # PowerShell automation scripts
├── 📈 powerbi/
│   ├── datasets/       # Data model and DAX measures
│   └── reports/        # Dashboard structure documentation
├── 📚 documentation/
│   ├── technical/      # Deployment and technical guides
│   └── user-guides/    # End-user documentation
└── 🔄 .github/
    └── workflows/      # CI/CD automation
```

## 🛠️ Installation

### Prerequisites
- Power BI Desktop (latest version)
- Python 3.8+ (for data generation)
- 500MB free disk space

### Automated Setup

#### Linux/macOS
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

#### Windows
```batch
scripts\setup.bat
```

### Manual Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Generate sample data: `python scripts/etl/generate_master_data.py`
3. Run data quality checks: `python scripts/etl/data_quality_check.py`
4. Open Power BI Desktop and import data using the provided scripts

## 📊 Data Model

The solution implements a star schema optimized for Power BI:

### Fact Tables
- **Fact_Sales**: 36,400 transactions with full financial metrics
- **Fact_Budget**: Department budgets with actuals and forecasts
- **Fact_Inventory**: Real-time stock levels across warehouses

### Dimension Tables
- **Dim_Date**: 4-year calendar with fiscal periods
- **Dim_Product**: 339 products across categories
- **Dim_Customer**: 724 customers with geographic data
- **Dim_Employee**: 319 employees with org hierarchy

## 🎯 KPIs and Metrics

### Financial KPIs
- Net Sales (Actual vs Budget vs LY)
- Gross Profit Margin %
- EBITDA and Net Profit
- Working Capital Days
- Cash Flow Analysis

### Operational KPIs
- Inventory Turnover
- On-Time In-Full (OTIF) Delivery
- Stock Coverage Days
- Cost per Case

### Customer KPIs
- Customer Acquisition and Retention
- Revenue per Customer
- Customer Satisfaction Score
- Market Share %

## 🔒 Security

- **Row-Level Security (RLS)**: Implemented for regional and departmental access
- **Role-Based Access**: Executive, Manager, Analyst, and Viewer roles
- **Data Protection**: POPIA compliant for South African regulations
- **Audit Trail**: Complete tracking of data changes

## 📱 Mobile Experience

- Responsive design for tablets and smartphones
- Offline capability for key metrics
- Touch-optimized interactions
- Push notifications for alerts

## 🚀 Deployment

### Quick Deployment
1. Run setup scripts to generate data
2. Open Power BI Desktop
3. Import data using `PowerBI_Setup.ps1`
4. Apply DAX measures from `DAX_Measures.txt`
5. Publish to Power BI Service

### Production Deployment
See the comprehensive [Deployment Guide](documentation/technical/Deployment_Guide.md) for:
- Enterprise setup instructions
- Data source configuration
- Security implementation
- Performance optimization

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)**: Get up and running in minutes
- **[Project Summary](PROJECT_SUMMARY.md)**: Detailed feature overview
- **[User Guide](documentation/user-guides/Executive_Dashboard_User_Guide.md)**: Complete end-user documentation
- **[Technical Documentation](documentation/technical/)**: Architecture and deployment guides
- **[Data Model](powerbi/datasets/BevcoDataModel.md)**: Complete schema documentation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🧪 Testing

```bash
# Run data quality checks
python scripts/etl/data_quality_check.py

# Validate Power BI import
powershell -ExecutionPolicy Bypass .\scripts\import_to_powerbi.ps1 -ValidateOnly
```

## 📊 Sample Data

The repository includes realistic sample data for 2024:
- 36,400 sales transactions
- 724 customers across 9 regions
- 339 products from 5 vendors
- Complete financial and operational metrics

## 🏆 Use Cases

Perfect for:
- Executive teams requiring real-time business visibility
- Financial controllers monitoring budgets and cash flow
- Sales directors tracking performance and territories
- Operations managers optimizing supply chain
- HR leaders analyzing workforce metrics

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Power BI and Python
- Designed for the South African beverage industry
- Follows Microsoft best practices for Power BI development

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Reshigan/bevco-executive-dashboard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Reshigan/bevco-executive-dashboard/discussions)
- **Documentation**: [Wiki](https://github.com/Reshigan/bevco-executive-dashboard/wiki)

---

**⭐ If you find this project useful, please consider giving it a star!**

*Developed with ❤️ for data-driven decision making*