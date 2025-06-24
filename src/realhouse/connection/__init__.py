"""
dubai_real_estate Connection Module

This module provides unified connection management for ClickHouse variants:
- CHDB (in-memory, default for development)
- CLIENT (ClickHouse client for server or cloud)

Features:
- Secure credential storage in user filesystem
- Auto-connection support
- Connection sharing across modules
- Context managers for temporary connections

    Examples:
    Basic usage:
    >>> from dubai_real_estate.connection import create_connection, get_connection
    >>>
    >>> # Create a development connection (CHDB in-memory)
    >>> conn = create_connection("dev", "chdb")
    >>>
    >>> # Create a file-based CHDB connection
    >>> conn = create_connection("dev_file", "chdb", database_path="test.db")
    >>>
    >>> # Create a client connection (server)
    >>> conn = create_connection(
    ...     "prod", "client",
    ...     host="localhost",
    ...     port=8123,
    ...     username="user",
    ...     password="secret",
    ...     save=True,
    ...     set_auto=True
    ... )
    >>>
    >>> # Create a secure cloud connection
    >>> conn = create_connection(
    ...     "cloud", "client",
    ...     host="play.clickhouse.com",
    ...     port=443,
    ...     username="play",
    ...     password="clickhouse",
    ...     secure=True
    ... )
    >>>
    >>> # Use connection with cursor pattern
    >>> conn = get_connection()
    >>>
    >>> # Connect to the DB
    >>> conn.connect()
    >>>
    >>> with conn:
    ...     cursor = conn.execute("SELECT number FROM system.numbers LIMIT 3")
    ...     print(cursor.fetchone())  # (0,)
    ...     cursor.close()

    Advanced usage:
    >>> from dubai_real_estate.connection import get_manager
    >>>
    >>> manager = get_manager()
    >>> connections = manager.list_connections()
    >>>
    >>> # Use connection context manager
    >>> with manager.connection("prod") as conn:
    ...     cursor = conn.execute("SELECT COUNT(*) FROM transactions")
    ...     result = cursor.fetchone()
    ...     cursor.close()
"""

from .types import (
    ConnectionType,
    CHDBCredentials,
    ClientCredentials,
    AnyCredentials,
    get_default_credentials,
    create_credentials,
)

from .storage import CredentialStorage, get_storage

from .clients import CHDBConnection, ClientConnection, BaseConnection

from .manager import ConnectionManager, get_manager, get_connection, create_connection


# Convenience functions for quick setup
def setup_default_connection() -> None:
    """Set up default CHDB connection for development.

    Creates a default in-memory CHDB connection that's perfect for
    getting started with dubai_real_estate development.

    Example:
        >>> from dubai_real_estate.connection import setup_default_connection
        >>> setup_default_connection()
        >>>
        >>> # Now you can use the default connection
        >>> from dubai_real_estate.connection import get_connection
        >>> conn = get_connection()
    """
    manager = get_manager()

    # Check if default connection already exists
    if manager.get_connection() is not None:
        return

    # Create default CHDB connection
    manager.create_connection(
        name="default_chdb",
        connection_type="chdb",
        description="Default in-memory CHDB connection for development",
        save=True,
        set_auto=True,
    )


def quick_connect(connection_type: str = "chdb", **kwargs) -> BaseConnection:
    """Quickly create and connect to ClickHouse.

    This is a convenience function for rapid prototyping and testing.
    Creates a temporary connection without saving credentials.

    Args:
        connection_type: Type of connection ("chdb", "client")
        **kwargs: Connection parameters

    Returns:
        Connected connection object

    Example:
        >>> from dubai_real_estate.connection import quick_connect
        >>>
        >>> # Quick CHDB connection (in-memory)
        >>> with quick_connect("chdb") as conn:
        ...     cursor = conn.execute("SELECT 1")
        ...     result = cursor.fetchone()
        ...     cursor.close()
        >>>
        >>> # Quick CHDB connection (file-based)
        >>> with quick_connect("chdb", database_path="test.db") as conn:
        ...     cursor = conn.execute("SELECT 1")
        ...     result = cursor.fetchone()
        ...     cursor.close()
        >>>
        >>> # Quick client connection (server)
        >>> with quick_connect(
        ...     "client",
        ...     host="localhost",
        ...     port=8123,
        ...     username="user",
        ...     password="pass"
        ... ) as conn:
        ...     cursor = conn.execute("SELECT version()")
        ...     result = cursor.fetchone()
        ...     cursor.close()
        >>>
        >>> # Quick cloud connection (ClickHouse Play)
        >>> with quick_connect(
        ...     "client",
        ...     host="play.clickhouse.com",
        ...     port=443,
        ...     username="play",
        ...     password="clickhouse",
        ...     secure=True
        ... ) as conn:
        ...     result = conn.command("SELECT timezone()")
        ...     print(result)  # 'Etc/UTC'
    """
    manager = get_manager()

    # Create temporary connection name
    import uuid

    temp_name = f"temp_{uuid.uuid4().hex[:8]}"

    # Create connection without saving
    connection = manager.create_connection(
        name=temp_name, connection_type=connection_type, save=False, **kwargs
    )

    # Connect immediately
    connection.connect()

    return connection


# Export main classes and functions
__all__ = [
    # Types
    "ConnectionType",
    "CHDBCredentials",
    "ClientCredentials",
    "AnyCredentials",
    # Storage
    "CredentialStorage",
    "get_storage",
    # Clients
    "CHDBConnection",
    "ClientConnection",
    # Manager
    "ConnectionManager",
    "get_manager",
    # Convenience functions
    "get_connection",
    "create_connection",
    "setup_default_connection",
    "quick_connect",
    # Utilities
    "get_default_credentials",
    "create_credentials",
]

# Auto-setup default connection on import
# This ensures there's always a working connection available
try:
    setup_default_connection()
except Exception:
    # Ignore setup errors on import
    pass
