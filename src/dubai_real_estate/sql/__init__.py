"""
dubai_real_estate SQL Module

Provides SQL file parsing and management capabilities for tables and functions.
By default, uses sql_files/ folder in the same directory as the module.

Also includes Jupyter magic commands for executing SQL queries.

Examples:
    Basic usage (automatic path):
    >>> from dubai_real_estate.sql import SQLParser
    >>> parser = SQLParser()  # Uses dubai_real_estate/sql_files/ automatically
    >>>
    >>> # Get table SQL
    >>> create_sql = parser.get_table("users", "CREATE")
    >>> ingest_sql = parser.get_table("dld_orders", "INGEST")
    >>>
    >>> # Get function SQL
    >>> math_func = parser.get_function("MATH", "calculate_total")
    >>> format_func = parser.get_function("FORMAT", "format_date")

    Custom path:
    >>> parser = SQLParser("/custom/path/to/sql")

    Quick functions (automatic path):
    >>> from dubai_real_estate.sql import get_table_sql, get_function_sql
    >>>
    >>> sql = get_table_sql("users", "CREATE")
    >>> func = get_function_sql("MATH", "sum_values")

    Quick functions (custom path):
    >>> sql = get_table_sql("users", "CREATE", "/custom/path")

    List operations:
    >>> parser = SQLParser()
    >>>
    >>> tables = parser.list_tables()
    >>> options = parser.list_table_options("users")
    >>> functions = parser.list_functions("MATH")
    >>> all_sql = parser.get_all_table_files("orders")

    Jupyter Magic Commands:
    >>> # In Jupyter notebook
    >>> %load_ext dubai_real_estate.sql
    >>> %sql SELECT * FROM dld_transactions LIMIT 5
    >>> %%sql
    >>> SELECT count(*) FROM dld_transactions;
    >>> SELECT avg(amount) FROM dld_transactions;
"""

from .parser import (
    SQLParser,
    create_parser,
    get_table_sql,
    get_function_sql,
)

# Import magic command functions for Jupyter
try:
    from ..magic.sql_magic import (
        SQLMagic,
        load_ipython_extension,
        unload_ipython_extension,
    )

    _MAGIC_AVAILABLE = True
except ImportError:
    _MAGIC_AVAILABLE = False

__all__ = [
    "SQLParser",
    "create_parser",
    "get_table_sql",
    "get_function_sql",
]

# Add magic command exports if available
if _MAGIC_AVAILABLE:
    __all__.extend(["SQLMagic", "load_ipython_extension", "unload_ipython_extension"])
