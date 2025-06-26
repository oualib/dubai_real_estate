try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

# Import main modules
from . import connection
from . import sql
from . import install

# Export commonly used functions
from .connection import get_connection, create_connection, setup_default_connection
from .sql import get_table_sql, get_function_sql, SQLParser
from .install import (
    DEFAULT_DATABASE,
    create_database,
    install_database,
    install_functions,
    install_tables,
    install_views,
    install_prod_tables,
    drop_staging_and_views,
)

__all__ = [
    "__version__",
    # Modules
    "connection",
    "sql",
    "install",
    # Connection functions
    "get_connection",
    "create_connection",
    "setup_default_connection",
    # SQL functions
    "get_table_sql",
    "get_function_sql",
    "SQLParser",
    # Install functions
    "DEFAULT_DATABASE",
    "create_database",
    "install_database",
    "install_functions",
    "install_tables",
    "install_views",
    "install_prod_tables",
    "drop_staging_and_views",
]
