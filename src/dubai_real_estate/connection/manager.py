"""
Connection manager for dubai_real_estate ClickHouse connections.

This module provides the main connection manager that handles creating,
managing, and sharing connections across the dubai_real_estate module.
"""

import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from .types import (
    AnyCredentials,
    ConnectionType,
    CHDBCredentials,
    ClientCredentials,
    get_default_credentials,
)
from .storage import get_storage
from .clients import CHDBConnection, ClientConnection, BaseConnection

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages ClickHouse connections for dubai_real_estate.

    This class provides a unified interface for creating, storing, and
    managing different types of ClickHouse connections. It handles
    credential storage, auto-connection, and connection sharing.
    """

    def __init__(self):
        """Initialize connection manager.

        Example:
            >>> manager = ConnectionManager()
        """
        self._active_connection = None
        self._connection_cache: Dict[str, BaseConnection] = {}
        self._storage = get_storage()

    def create_connection(
        self,
        name: str,
        connection_type: str,
        save: bool = True,
        set_auto: bool = False,
        **kwargs,
    ) -> BaseConnection:
        """Create a new connection.

        Args:
            name: Unique name for the connection
            connection_type: Type of connection ("chdb", "client")
            save: Whether to save credentials to storage
            set_auto: Whether to set as auto connection
            **kwargs: Connection-specific parameters

        Returns:
            Connection object

        Raises:
            ValueError: If connection type is invalid
            ConnectionError: If connection fails

        Example:
            >>> # Create CHDB connection
            >>> conn = manager.create_connection(
            ...     name="dev",
            ...     connection_type="chdb"
            ... )
            >>>
            >>> # Create client connection
            >>> conn = manager.create_connection(
            ...     name="prod",
            ...     connection_type="client",
            ...     host="localhost",
            ...     username="user",
            ...     password="secret",
            ...     save=True,
            ...     set_auto=True
            ... )
        """
        # Create credentials
        credentials = self._create_credentials(
            name=name, connection_type=connection_type, is_auto=set_auto, **kwargs
        )

        # Save credentials if requested
        if save:
            self._storage.save_credentials(credentials)
            logger.info(f"Saved credentials for connection '{name}'")

        # Create connection object
        connection = self._create_connection_object(credentials)

        # Cache connection
        self._connection_cache[name] = connection

        logger.info(f"Created {connection_type} connection '{name}'")

        try:
            if not (connection.is_connected()):
                # trying to connect if possible
                connection.connect()
        except:
            pass

        return connection

    def get_connection(self, name: Optional[str] = None) -> Optional[BaseConnection]:
        """Get a connection by name or auto connection.

        Args:
            name: Connection name. If None, uses auto connection

        Returns:
            Connection object or None if not found

        Example:
            >>> # Get specific connection
            >>> conn = manager.get_connection("prod")
            >>>
            >>> # Get auto connection
            >>> conn = manager.get_connection()
        """
        # If no name provided, try auto connection
        if name is None:
            name = self._storage.get_auto_connection()
            if name is None:
                logger.warning("No auto connection set")
                return None

        # Check cache first
        if name in self._connection_cache:
            return self._connection_cache[name]

        # Load from storage
        credentials = self._storage.load_credentials(name)
        if credentials is None:
            logger.warning(f"Connection '{name}' not found")
            return None

        # Create and cache connection
        connection = self._create_connection_object(credentials)
        self._connection_cache[name] = connection

        return connection

    def list_connections(self) -> List[Dict[str, Any]]:
        """List all available connections with details.

        Returns:
            List of connection information dictionaries

        Example:
            >>> connections = manager.list_connections()
            >>> for conn in connections:
            ...     print(f"{conn['name']}: {conn['type']} ({'auto' if conn['is_auto'] else 'manual'})")
        """
        connection_names = self._storage.list_connections()
        auto_connection = self._storage.get_auto_connection()

        connections = []
        for name in connection_names:
            credentials = self._storage.load_credentials(name)
            if credentials:
                connections.append(
                    {
                        "name": credentials.name,
                        "type": credentials.connection_type.value,
                        "description": credentials.description,
                        "is_auto": name == auto_connection,
                        "is_cached": name in self._connection_cache,
                        "is_connected": (
                            self._connection_cache[name].is_connected()
                            if name in self._connection_cache
                            else False
                        ),
                    }
                )

        return connections

    def set_auto_connection(self, name: str) -> bool:
        """Set a connection as the auto connection.

        Args:
            name: Name of the connection to set as auto

        Returns:
            True if successful, False otherwise

        Example:
            >>> success = manager.set_auto_connection("prod")
            >>> print(f"Set auto connection: {success}")
        """
        success = self._storage.set_auto_connection(name)
        if success:
            logger.info(f"Set '{name}' as auto connection")
        return success

    def delete_connection(self, name: str) -> bool:
        """Delete a connection.

        Args:
            name: Name of the connection to delete

        Returns:
            True if deleted, False if not found

        Example:
            >>> success = manager.delete_connection("old_connection")
            >>> print(f"Deleted: {success}")
        """
        # Remove from cache
        if name in self._connection_cache:
            connection = self._connection_cache[name]
            if connection.is_connected():
                connection.disconnect()
            del self._connection_cache[name]

        # Delete from storage
        success = self._storage.delete_credentials(name)
        if success:
            logger.info(f"Deleted connection '{name}'")

        return success

    def get_active_connection(self) -> Optional[BaseConnection]:
        """Get the currently active connection.

        Returns:
            Active connection or None

        Example:
            >>> conn = manager.get_active_connection()
            >>> if conn and conn.is_connected():
            ...     result = conn.execute("SELECT 1")
        """
        return self._active_connection

    def set_active_connection(self, name: Optional[str] = None) -> bool:
        """Set the active connection.

        Args:
            name: Connection name. If None, uses auto connection

        Returns:
            True if successful, False otherwise

        Example:
            >>> # Set specific connection as active
            >>> success = manager.set_active_connection("prod")
            >>>
            >>> # Set auto connection as active
            >>> success = manager.set_active_connection()
        """
        connection = self.get_connection(name)
        if connection is None:
            return False

        # Disconnect previous active connection if different
        if (
            self._active_connection
            and self._active_connection != connection
            and self._active_connection.is_connected()
        ):
            self._active_connection.disconnect()

        self._active_connection = connection

        # Connect if not already connected
        if not connection.is_connected():
            try:
                connection.connect()
            except Exception as e:
                logger.error(f"Failed to connect: {e}")
                return False

        logger.info(f"Set active connection: {connection.credentials.name}")
        return True

    @contextmanager
    def connection(self, name: Optional[str] = None):
        """Context manager for temporary connection.

        Args:
            name: Connection name. If None, uses auto connection

        Yields:
            Connection object

        Example:
            >>> with manager.connection("prod") as conn:
            ...     result = conn.execute("SELECT COUNT(*) FROM transactions")
            ...     print(f"Total records: {result}")
        """
        connection = self.get_connection(name)
        if connection is None:
            raise ValueError(f"Connection '{name}' not found")

        was_connected = connection.is_connected()

        if not was_connected:
            connection.connect()

        try:
            yield connection
        finally:
            if not was_connected:
                connection.disconnect()

    def _create_credentials(self, **kwargs) -> AnyCredentials:
        """Create credentials object from parameters."""
        connection_type = kwargs.pop("connection_type")

        if connection_type == "chdb" or connection_type == ConnectionType.CHDB:
            return CHDBCredentials(connection_type=ConnectionType.CHDB, **kwargs)
        elif connection_type == "client" or connection_type == ConnectionType.CLIENT:
            return ClientCredentials(connection_type=ConnectionType.CLIENT, **kwargs)
        else:
            raise ValueError(f"Invalid connection type: {connection_type}")

    def _create_connection_object(self, credentials: AnyCredentials) -> BaseConnection:
        """Create connection object from credentials."""
        if credentials.connection_type == ConnectionType.CHDB:
            return CHDBConnection(credentials)
        elif credentials.connection_type == ConnectionType.CLIENT:
            return ClientConnection(credentials)
        else:
            raise ValueError(
                f"Unsupported connection type: {credentials.connection_type}"
            )


# Global connection manager instance
_manager = None


def get_manager() -> ConnectionManager:
    """Get global connection manager instance.

    Returns:
        Global ConnectionManager instance

    Example:
        >>> manager = get_manager()
        >>> connections = manager.list_connections()
    """
    global _manager
    if _manager is None:
        _manager = ConnectionManager()
    return _manager


def get_connection(name: Optional[str] = None) -> Optional[BaseConnection]:
    """Convenience function to get a connection.

    Args:
        name: Connection name. If None, uses auto connection

    Returns:
        Connection object or None if not found

    Example:
        >>> conn = get_connection("prod")
        >>> if conn:
        ...     result = conn.execute("SELECT 1")
    """
    return get_manager().get_connection(name)


def create_connection(name: str, connection_type: str, **kwargs) -> BaseConnection:
    """Convenience function to create a connection.

    Args:
        name: Connection name
        connection_type: Type of connection ("chdb", "client")
        **kwargs: Connection parameters

    Returns:
        Connection object

    Example:
        >>> conn = create_connection(
        ...     "dev",
        ...     "chdb"
        ... )
    """
    return get_manager().create_connection(name, connection_type, **kwargs)
