# Dubai Real Estate Database

A comprehensive Python package for working with Dubai real estate data from Dubai Land Department (DLD). This package provides easy access to Dubai's real estate datasets through ClickHouse, with beautiful SQL magic commands for Jupyter notebooks.

## ✨ Features

- **🚀 One-command setup**: Install complete Dubai real estate database with a single function call
- **📊 Rich datasets**: Access 18+ Dubai real estate datasets including transactions, valuations, permits, and more
- **🎯 ClickHouse integration**: Optimized for ClickHouse's powerful analytics capabilities
- **📝 Beautiful SQL Magic**: Jupyter notebook integration with syntax highlighting and rich output
- **🔐 Secure credentials**: Encrypted storage of connection credentials
- **📈 Production ready**: Optimized for both development and production deployments

## 🚀 Quick Start

### Installation

```bash
pip install dubai_real_estate
```

### 1. Set Up ClickHouse

You'll need a ClickHouse instance. Get started quickly with:

**🆓 [ClickHouse Cloud - 1 Month Free Trial](https://clickhouse.com/cloud)**
- No setup required - ready in minutes
- Production-grade performance
- Automatic scaling and backups

Or use your existing ClickHouse server.

### 2. Create Connection

```python
from dubai_real_estate.connection import create_connection

# For ClickHouse Cloud
create_connection(
    "cloud", 
    "client",
    host="your-instance.clickhouse.cloud",
    port=8443,
    username="default", 
    password="your-password",
    database="dubai_real_estate", # Default name. Replace with your Dubai database name if you've changed it
    secure=True,
    set_auto=True
)

# For self-hosted ClickHouse
create_connection(
    "local", 
    "client",
    host="localhost",
    port=8123,
    username="default", 
    password="",
    database="dubai_real_estate", # Default name. Replace with your Dubai database name if you've changed it
    set_auto=True
)
```

### 3. Install Database

```python
from dubai_real_estate.install import install_database

# Complete installation (only production tables)
result = install_database()
```

### 4. Query with SQL Magic

```python
# Load the magic extension in Jupyter
%load_ext dubai_real_estate.sql

# Use Registered Connections
%sql_connect cloud

# Start querying the real data!
%sql SELECT COUNT(*) as total_transactions FROM dld_transactions
# Result: +1,475,500 transactions

# Analyze Dubai real estate trends by year
%%sql
SELECT 
    year(instance_date) as year,
    COUNT(*) as transactions,
    round(AVG(actual_worth), 0) as avg_amount_aed
FROM dld_transactions 
WHERE actual_worth > 0 AND instance_date > '2020-01-01'
GROUP BY year
ORDER BY year DESC;

# Top 10 areas by transaction volume
%%sql
SELECT 
    area_name_english as area,
    COUNT(*) as total_transactions,
    round(AVG(actual_worth), 0) as avg_price_aed
FROM dld_transactions 
WHERE area_name_english IS NOT NULL AND actual_worth > 0
GROUP BY area_name_english 
ORDER BY total_transactions DESC 
LIMIT 10;
```

That's it! You now have access to Dubai's complete real estate database with beautiful SQL querying capabilities.

## 📊 Available Datasets

The package includes 18 comprehensive datasets from Dubai Land Department with **13+ million records**:

| Dataset | Description | Records |
|---------|-------------|---------|
| `dld_rent_contracts` | Rental contracts and lease agreements | **8.9M+** |
| `dld_units` | Property units and details | **2.2M+** |
| `dld_transactions` | Real estate transactions (2002-2025) | **1.5M+** |
| `dld_buildings` | Building information and specifications | **223K+** |
| `dld_real_estate_permits` | Construction and real estate permits | **132K+** |
| `dld_valuation` | Property valuations and assessments | **84K+** |
| `dld_brokers` | Licensed real estate brokers | **8.4K+** |
| `dld_offices` | Real estate offices and agencies | **4.9K+** |
| `dld_projects` | Development projects and master plans | **3.2K+** |
| `dld_developers` | Developer companies and information | **2.0K+** |
| `dld_accredited_escrow_agents` | Licensed escrow service providers | ✓ |
| `dld_free_zone_companies_licensing` | Free zone company licenses | ✓ |
| `dld_land_registry` | Land registry and ownership records | ✓ |
| `dld_licenced_owner_associations` | Owner association licenses | ✓ |
| `dld_map_requests` | Property mapping and survey requests | ✓ |
| `dld_oa_service_charges` | Owner association service charges | ✓ |
| `dld_real_estate_licenses` | Real estate professional licenses | ✓ |
| `dld_valuator_licensing` | Property valuator certifications | ✓ |

## 🕐 Installation Time

The complete database installation processes **13+ million records** across 18 datasets:

```python
import time
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        print(f"⏱️  Installation completed in {duration/60:.2f} minutes")

# Time your installation
with timer():
    result = install_database()

print(f"✅ Success: {result['success']}")
print(f"📊 Total records: {result.get('validation', {}).get('total_staging_rows', 0):,}")
```

**Expected timing:**
- **ClickHouse Cloud (free trial)**: ~14 minutes ⭐
- **ClickHouse Local**: ~8-15 minutes (depending on hardware)
- Processing 1.5M transactions, 2.2M units, 8.9M rental contracts, and more!

## 🎓 Examples

Check out these example notebooks to get started:
- **[Quick Start with SQL Magic](examples/sql_magic_notebook.ipynb)** - Install and query data in 15 minutes

- **[ClickHouse MCP Setup](examples/clickhouse_mcp_notebook.ipynb)** - Prepare data for ClickHouse MCP integration

## 🏗️ Advanced Usage

```python
from dubai_real_estate.connection import get_connection, create_connection

# Create multiple connections
create_connection("staging", "client", host="staging-db.com", set_auto=True)
create_connection("prod", "client", host="prod-db.com")

# Use specific connection
conn = get_connection("prod")
with conn:
    result = conn.execute("SELECT COUNT(*) FROM dld_transactions")
```

### Selective Installation

```python
from dubai_real_estate.install import install_tables, install_functions

# Install specific tables only
install_tables(table_names=["dld_transactions", "dld_units"])

# Install SQL functions only
install_functions(categories=["FORMAT", "MAP"])
```

### SQL Magic Configuration

```python
# Configure display options
%sql_config max_rows_display=50
%sql_config minimal_mode=True

# View configuration
%sql_config

# Query with options
%sql --limit 10 --minimal SELECT * FROM dld_transactions

# Export results
%sql --export csv SELECT * FROM dld_units WHERE area_name_english = 'Downtown Dubai'
```

## 📜 Data License

This package is licensed under **Apache 2.0**, but the data accessed through this package is subject to Dubai's Open Data License. After ingesting the data, you must comply with the [Dubai Open Data License](https://www.dubaipulse.gov.ae/docs/DDE%20_%20DRAFT_Open_Data%20Licence_LONG_Form_English%203.pdf).

**Key points:**
- ✅ Free to use for research, analysis, and commercial applications
- ✅ Attribution required: "Data provided by Dubai Land Department via Dubai Pulse"
- ✅ Redistribution allowed with proper attribution
- ❌ No warranty provided on data accuracy or completeness

## 🗃️ Data Source

All data is sourced from **Dubai Pulse**, the official open data platform of Dubai:
- **Source**: [Dubai Land Department (DLD)](https://www.dubaipulse.gov.ae/organisation/dld)
- **Platform**: Dubai Pulse Open Data Portal
- **Updates**: Data is regularly updated by Dubai Land Department
- **Quality**: Official government data with high reliability

## 🛠️ Technical Details

### System Requirements

- Python 3.12+
- ClickHouse instance ([Get 1 month free trial](https://clickhouse.com/cloud))
- 8GB+ RAM (for full dataset - 13M+ records)
- 15GB+ disk space (for production installation)

### Dependencies

- `clickhouse-connect` - ClickHouse client connectivity
- `pandas` - Data manipulation
- `cryptography` - Secure credential storage
- `IPython` - Jupyter magic commands

### Performance

- **ClickHouse Local**: ~2-10 seconds for most queries
- **ClickHouse Cloud**: ~1-2 seconds for most queries (depends on instance size)
- **Installation time**: 
  - ClickHouse Cloud (free trial): ~14 minutes for full database (13M+ records)
  - ClickHouse Local: ~8-12 minutes depending on hardware
  - Network speed affects data ingestion time significantly
- **Memory usage**: ~8-12GB for full dataset processing
- **Data coverage**: 2002-2025 (live updates from Dubai Pulse)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Submit a pull request

## 📄 License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/oualib/dubai_real_estate/issues)
- **Discussions**: [GitHub Discussions](https://github.com/oualib/dubai_real_estate/discussions)
- **Documentation**: [Full Documentation](https://github.com/oualib/dubai_real_estate)

## 🎯 Roadmap

- [ ] Real-time data streaming
- [ ] Advanced analytics functions
- [ ] Data quality monitoring
- [ ] REST API interface
- [ ] Docker deployment options
- [ ] Additional data sources integration

---

**Made with ❤️ for Dubai's real estate community**

> Access Dubai's real estate insights with the power of ClickHouse and the simplicity of Python.