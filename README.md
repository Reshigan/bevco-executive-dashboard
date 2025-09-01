# Bevco Executive Dashboard

A comprehensive Power BI executive dashboard solution for Bevco South Africa, providing real-time visibility of business performance across all organizational levels.

## Project Structure

```
bevco-executive-dashboard/
├── data/
│   ├── raw/              # Raw data files
│   ├── processed/        # Processed data ready for Power BI
│   └── master/          # Master data files
├── scripts/
│   ├── etl/             # ETL scripts for data processing
│   └── analysis/        # Analysis and calculation scripts
├── powerbi/
│   ├── reports/         # Power BI report files (.pbix)
│   ├── datasets/        # Shared datasets
│   └── dataflows/       # Power BI dataflows
├── documentation/
│   ├── technical/       # Technical documentation
│   └── user-guides/     # User guides and training materials
├── config/              # Configuration files
└── tests/              # Test scripts and data
```

## Key Features

- **Executive Summary Dashboard**: Real-time KPIs with drill-down capabilities
- **Sales & Revenue Management**: Comprehensive sales analytics
- **Financial Management**: P&L, working capital, and budget tracking
- **Operational Excellence**: Supply chain and quality metrics
- **Customer & Market Intelligence**: Customer analytics and market insights
- **People & Performance**: HR metrics and sales force effectiveness

## Getting Started

1. Install Power BI Desktop
2. Set up data connections to source systems
3. Load sample master data from `/data/master/`
4. Open the main report file from `/powerbi/reports/`

## Data Model

The solution uses a star schema design with:
- Fact tables for transactions, sales, inventory, and financial data
- Dimension tables for time, products, customers, geography, and employees
- Calculated measures for KPIs and advanced analytics

## Security

- Row-level security (RLS) implemented for role-based access
- Data encryption at rest and in transit
- POPIA compliance for South African data protection

## Support

For technical support and questions, please refer to the documentation in the `/documentation/` folder.