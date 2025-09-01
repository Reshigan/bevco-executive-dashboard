# Bevco Executive Dashboard - Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Data Preparation](#data-preparation)
4. [Power BI Development](#power-bi-development)
5. [Security Configuration](#security-configuration)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Maintenance](#maintenance)

## Prerequisites

### Software Requirements
- **Power BI Desktop** (Latest version)
- **Power BI Pro or Premium** license for sharing
- **Python 3.8+** (for data generation scripts)
- **SQL Server** or **Azure SQL Database** (for production data)
- **Power BI Gateway** (for on-premises data sources)

### Access Requirements
- Admin access to Power BI Service
- Read access to source systems (ERP, CRM, etc.)
- Azure Active Directory access for security setup

## Environment Setup

### 1. Development Environment

```bash
# Clone the repository
git clone https://github.com/bevco/executive-dashboard.git
cd bevco-executive-dashboard

# Install Python dependencies
pip install pandas numpy

# Generate sample data
python scripts/etl/generate_master_data.py
```

### 2. Power BI Workspace Setup

1. Log in to Power BI Service (app.powerbi.com)
2. Create a new workspace: "Bevco Executive Dashboard"
3. Set workspace type to "Premium" if available
4. Configure workspace settings:
   - Enable "Featured content"
   - Set up workspace roles

## Data Preparation

### 1. Initial Data Load

For development with sample data:
```powershell
# Run the PowerBI setup script
.\scripts\PowerBI_Setup.ps1
```

For production data:
1. Set up connections to source systems
2. Create ETL pipelines for data extraction
3. Implement data quality checks
4. Schedule regular data refreshes

### 2. Data Model Implementation

1. **Import Data Tables**:
   - Open Power BI Desktop
   - Get Data > Text/CSV
   - Import all dimension and fact tables
   
2. **Create Relationships**:
   ```
   Fact_Sales[DateKey] → Dim_Date[DateKey]
   Fact_Sales[ProductKey] → Dim_Product[ProductKey]
   Fact_Sales[CustomerKey] → Dim_Customer[CustomerKey]
   Fact_Sales[EmployeeKey] → Dim_Employee[EmployeeKey]
   Fact_Budget[DateKey] → Dim_Date[DateKey]
   Fact_Inventory[ProductKey] → Dim_Product[ProductKey]
   ```

3. **Configure Relationship Properties**:
   - Set all relationships to Single direction
   - Set cross-filter direction as needed
   - Mark Date table as Date Table

## Power BI Development

### 1. Import DAX Measures

1. Open Power BI Desktop with loaded data model
2. Go to Modeling tab > New Measure
3. Copy measures from `DAX_Measures.txt`
4. Create measure folders for organization:
   - Sales Metrics
   - Financial Metrics
   - Customer Metrics
   - Operational Metrics
   - HR Metrics

### 2. Create Report Pages

Follow the structure in `Dashboard_Structure.md`:

1. **Executive Summary Page**:
   - Add KPI cards for main metrics
   - Create trend charts
   - Add slicers for filtering
   
2. **Sales Performance Page**:
   - Build sales analytics visuals
   - Add drill-through functionality
   
3. **Financial Management Page**:
   - Create P&L visualizations
   - Add budget vs actual comparisons
   
4. **Additional Pages**:
   - Operations Dashboard
   - Customer Intelligence
   - People & Performance

### 3. Apply Formatting

1. **Import Theme**:
   - View tab > Themes > Browse for themes
   - Apply Bevco corporate theme
   
2. **Configure Visuals**:
   - Set consistent fonts (Segoe UI)
   - Apply color scheme
   - Enable data labels where appropriate
   
3. **Add Interactivity**:
   - Configure cross-filtering
   - Set up drill-through pages
   - Create bookmarks for different views

## Security Configuration

### 1. Row-Level Security (RLS)

Create security roles in Power BI Desktop:

```dax
// Regional Manager Role
[Region] = USERPRINCIPALNAME()

// Department Head Role
[Department] = USERPRINCIPALNAME()

// Sales Rep Role
[EmployeeCode] = USERPRINCIPALNAME()
```

### 2. Configure Roles

1. Modeling tab > Manage Roles
2. Create roles as defined above
3. Test roles using "View as Role"
4. Document role assignments

### 3. Workspace Security

In Power BI Service:
1. Workspace settings > Access
2. Assign users to roles:
   - Admin: IT administrators
   - Member: Report developers
   - Contributor: Business analysts
   - Viewer: End users

## Testing

### 1. Functional Testing

- [ ] All measures calculate correctly
- [ ] Filters work as expected
- [ ] Drill-through functionality works
- [ ] Mobile layout displays properly
- [ ] Export functionality works

### 2. Performance Testing

- [ ] Report loads within 3 seconds
- [ ] Slicers respond immediately
- [ ] Large data volumes handled efficiently
- [ ] Concurrent user testing (50+ users)

### 3. Security Testing

- [ ] RLS filters data correctly
- [ ] Users see only authorized data
- [ ] No data leakage between roles
- [ ] Export restrictions work

### 4. User Acceptance Testing

- [ ] Executive stakeholder review
- [ ] Department head validation
- [ ] End user feedback collection
- [ ] Mobile experience testing

## Deployment

### 1. Publish to Power BI Service

1. File > Publish > Select workspace
2. Choose "Bevco Executive Dashboard" workspace
3. Replace existing dataset if updating

### 2. Configure Dataset

1. Go to workspace > Datasets
2. Click on dataset settings
3. Configure:
   - Data source credentials
   - Refresh schedule
   - Query caching
   - Featured tables

### 3. Set Up Refresh Schedule

1. Dataset settings > Scheduled refresh
2. Configure refresh frequency:
   - Sales data: Every 2 hours
   - Financial data: Daily at 6 AM
   - Master data: Weekly
3. Set up failure notifications

### 4. Create App

1. Workspace > Create app
2. Configure app settings:
   - Name: "Bevco Executive Dashboard"
   - Description and support info
   - Navigation settings
   - Permissions

### 5. Distribution

1. **Email Subscriptions**:
   - Set up daily executive summary
   - Configure alert subscriptions
   
2. **Mobile Deployment**:
   - Test on Power BI mobile app
   - Create mobile-optimized views
   
3. **Embedding** (Optional):
   - Embed in SharePoint
   - Integrate with Teams

## Maintenance

### 1. Regular Maintenance Tasks

**Daily**:
- Monitor refresh status
- Check for failed refreshes
- Review usage metrics

**Weekly**:
- Validate data accuracy
- Review performance metrics
- Update documentation

**Monthly**:
- User feedback review
- Performance optimization
- Security audit

### 2. Change Management

1. **Version Control**:
   - Maintain .pbix files in Git
   - Document all changes
   - Use semantic versioning

2. **Update Process**:
   - Test changes in development
   - Get stakeholder approval
   - Deploy during maintenance window
   - Communicate changes to users

### 3. Monitoring

Set up Power BI monitoring:
- Usage metrics reports
- Performance analyzer
- Query diagnostics
- Error tracking

### 4. Support Structure

1. **Tier 1 Support** (Help Desk):
   - Password resets
   - Basic navigation help
   - Access issues

2. **Tier 2 Support** (BI Team):
   - Data discrepancies
   - Report modifications
   - Performance issues

3. **Tier 3 Support** (Development):
   - Major enhancements
   - Integration issues
   - Architecture changes

## Troubleshooting

### Common Issues and Solutions

1. **Slow Performance**:
   - Check query performance
   - Optimize DAX measures
   - Reduce visual count
   - Enable query caching

2. **Data Refresh Failures**:
   - Verify credentials
   - Check gateway status
   - Review error logs
   - Test source connectivity

3. **Access Issues**:
   - Verify user licenses
   - Check RLS configuration
   - Review workspace permissions
   - Validate AD group membership

## Appendices

### A. Useful PowerShell Commands

```powershell
# Check Power BI Gateway status
Get-Service "PBIEgwService"

# Export Power BI activity logs
Get-PowerBIActivityEvent -StartDateTime '2024-01-01T00:00:00' -EndDateTime '2024-01-31T23:59:59'

# Backup workspace
Export-PowerBIReport -WorkspaceId "workspace-guid" -OutPath "C:\Backups"
```

### B. Support Contacts

- **BI Team**: bi-support@bevco.co.za
- **IT Helpdesk**: helpdesk@bevco.co.za
- **Emergency**: +27 11 123 4567

### C. Additional Resources

- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Guide](https://dax.guide/)
- [Power BI Community](https://community.powerbi.com/)
- Internal Wiki: https://wiki.bevco.local/powerbi