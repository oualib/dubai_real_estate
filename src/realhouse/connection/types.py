"""
Connection type definitions for dubai_real_estate ClickHouse connections.

This module defines two types of ClickHouse connections:
- CHDB: In-memory ClickHouse using chdb.connect() and cursors
- CLIENT: ClickHouse client (server or cloud, same connection method)
"""

from dataclasses import dataclass
from typing import Optional, Union
from enum import Enum


class ConnectionType(Enum):
    """Supported ClickHouse connection types."""

    CHDB = "chdb"  # In-memory ClickHouse (default)
    CLIENT = "client"  # ClickHouse client (server or cloud)


@dataclass
class ConnectionCredentials:
    """Base class for connection credentials."""

    name: str
    connection_type: ConnectionType
    description: Optional[str] = None
    is_auto: bool = False  # If True, this connection is used automatically


@dataclass
class CHDBCredentials(ConnectionCredentials):
    """Credentials for CHDB (in-memory) connections.

    CHDB can work in-memory or with a file-based database.

    Args:
        name: Connection name identifier
        database_path: Database path (":memory:" for in-memory, or file path)
        description: Optional description of the connection
        is_auto: Whether this is the auto-connection

    Example:
        >>> # In-memory connection
        >>> creds = CHDBCredentials(
        ...     name="dev_memory",
        ...     database_path=":memory:"
        ... )
        >>>
        >>> # File-based connection
        >>> creds = CHDBCredentials(
        ...     name="dev_file",
        ...     database_path="dubai_real_estate.db"
        ... )
    """

    connection_type: ConnectionType = ConnectionType.CHDB
    database_path: str = ":memory:"

    def __post_init__(self):
        if self.connection_type != ConnectionType.CHDB:
            self.connection_type = ConnectionType.CHDB


@dataclass
class ClientCredentials(ConnectionCredentials):
    """Credentials for ClickHouse Client connections (server or cloud).

    Uses clickhouse-connect client for both self-hosted servers and cloud.
    Follows the official ClickHouse Connect API parameters.

    Args:
        name: Connection name identifier
        host: ClickHouse hostname (server or cloud)
        port: ClickHouse port (8123 HTTP, 8443 HTTPS, 9000 native - but client uses HTTP)
        username: Username for authentication (ClickHouse Connect uses 'username')
        password: Password for authentication
        database: Default database name
        secure: Whether to use HTTPS/TLS (auto-sets port to 8443 if True and port is default)
        interface: Connection interface ('http' or 'https') - auto-set based on secure
        compress: Enable compression (True, False, or compression algorithm)
        connect_timeout: HTTP connection timeout in seconds
        send_receive_timeout: Send/receive timeout in seconds
        session_id: Session ID for related queries (required for temp tables)
        description: Optional description of the connection
        is_auto: Whether this is the auto-connection

    Example:
        >>> # Server connection (HTTP)
        >>> creds = ClientCredentials(
        ...     name="prod_server",
        ...     host="clickhouse.company.com",
        ...     port=8123,
        ...     username="dubai_real_estate_user",
        ...     password="secure_password",
        ...     database="dubai_real_estate_prod"
        ... )
        >>>
        >>> # Cloud connection (HTTPS)
        >>> creds = ClientCredentials(
        ...     name="cloud_prod",
        ...     host="abc123.clickhouse.cloud",
        ...     port=8443,
        ...     username="cloud_user",
        ...     password="cloud_password",
        ...     secure=True
        ... )
        >>>
        >>> # ClickHouse Play (public demo)
        >>> creds = ClientCredentials(
        ...     name="clickhouse_play",
        ...     host="play.clickhouse.com",
        ...     port=443,
        ...     username="play",
        ...     password="clickhouse",
        ...     secure=True
        ... )
    """

    connection_type: ConnectionType = ConnectionType.CLIENT
    host: Optional[str] = None
    port: int = 8123  # Default HTTP port (8443 for HTTPS)
    username: str = "default"
    password: str = ""
    database: str = "default"
    secure: bool = False
    interface: Optional[str] = None  # Auto-set based on secure flag
    compress: bool = True
    connect_timeout: int = 10
    send_receive_timeout: int = 300
    session_id: Optional[str] = None

    def __post_init__(self):
        if self.connection_type != ConnectionType.CLIENT:
            self.connection_type = ConnectionType.CLIENT

        # Auto-adjust port for secure connections if using default port
        if self.secure and self.port == 8123:
            self.port = 8443

        # Auto-set interface based on secure flag
        if self.interface is None:
            self.interface = "https" if self.secure else "http"


# Type alias for any connection credentials
AnyCredentials = Union[CHDBCredentials, ClientCredentials]


def create_credentials(
    name: str, connection_type: Union[ConnectionType, str], **kwargs
) -> AnyCredentials:
    """Create credentials object based on connection type.

    Args:
        name: Connection name
        connection_type: Type of connection (CHDB or CLIENT)
        **kwargs: Additional connection parameters

    Returns:
        Appropriate credentials object

    Raises:
        ValueError: If connection_type is invalid

    Example:
        >>> # Create CHDB credentials (in-memory)
        >>> creds = create_credentials("dev", "chdb")
        >>>
        >>> # Create CHDB credentials (file-based)
        >>> creds = create_credentials("dev", "chdb", database_path="test.db")
        >>>
        >>> # Create client credentials
        >>> creds = create_credentials(
        ...     "prod", "client",
        ...     host="localhost",
        ...     username="user",
        ...     password="pass"
        ... )
    """
    if isinstance(connection_type, str):
        try:
            connection_type = ConnectionType(connection_type)
        except ValueError:
            raise ValueError(f"Invalid connection type: {connection_type}")

    if connection_type == ConnectionType.CHDB:
        return CHDBCredentials(name=name, connection_type=connection_type, **kwargs)
    elif connection_type == ConnectionType.CLIENT:
        return ClientCredentials(name=name, connection_type=connection_type, **kwargs)
    else:
        raise ValueError(f"Unsupported connection type: {connection_type}")


def get_default_credentials() -> CHDBCredentials:
    """Get default CHDB credentials for development.

    Returns:
        Default CHDB credentials (in-memory)

    Example:
        >>> creds = get_default_credentials()
        >>> print(creds.name)  # "default_chdb"
        >>> print(creds.database_path)  # ":memory:"
    """
    return CHDBCredentials(
        name="default_chdb",
        connection_type=ConnectionType.CHDB,
        database_path=":memory:",
        description="Default in-memory CHDB connection for development",
        is_auto=True,
    )
