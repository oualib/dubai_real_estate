"""
Dubai Real Estate SQL Magic Commands for Jupyter Notebooks

This module provides Jupyter magic commands for working with ClickHouse and
the Dubai Real Estate database system.

Usage:
    # Load the extension
    %load_ext dubai_real_estate.sql

    # Execute single SQL query
    %sql SELECT * FROM dld_transactions LIMIT 5

    # Execute multiple SQL statements
    %%sql
    SELECT count(*) as total_transactions FROM dld_transactions;
    SELECT avg(amount) as avg_amount FROM dld_transactions WHERE date > '2023-01-01';

    # Configure magic settings
    %sql_config max_rows_display=50
    %sql_config minimal_mode=True

    # View query history
    %sql_history

    # Show available tables
    %sql_tables

Features:
- Beautiful yellow/black themed output with ClickHouse branding
- Multi-statement support (statements separated by ';')
- Pandas DataFrame integration
- Query performance metrics
- Result caching and export (CSV, JSON, Excel)
- Query history
- Configurable display options
- Connection management integration

Magic Commands:
- %sql / %%sql: Execute SQL queries
- %sql_config: Configure magic settings
- %sql_history: View query history
- %sql_tables: List available tables

Arguments:
- --limit, -l: Limit number of rows returned
- --cache, -c: Cache the result
- --minimal, -m: Use minimal display mode
- --export, -e: Auto-export format (csv, json, excel)
- --connection: Use specific connection
"""

from .sql_magic import SQLMagic, load_ipython_extension, unload_ipython_extension

__all__ = ["SQLMagic", "load_ipython_extension", "unload_ipython_extension"]
