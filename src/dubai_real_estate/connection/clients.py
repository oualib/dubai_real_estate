"""
ClickHouse client implementations for different connection types.

This module provides concrete implementations of ClickHouse connections:
- CHDB: In-memory ClickHouse using chdb.connect() and cursors
- Client: ClickHouse client using clickhouse-connect (server or cloud)
"""

import logging
from typing import Any, Dict, Optional, List, Tuple, Iterator
from abc import ABC, abstractmethod

from .types import CHDBCredentials, ClientCredentials

logger = logging.getLogger(__name__)


class BaseConnection(ABC):
    """Abstract base class for ClickHouse connections."""

    def __init__(self, credentials):
        """Initialize connection with credentials.

        Args:
            credentials: Connection credentials object
        """
        self.credentials = credentials
        self._connected = False

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to ClickHouse."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to ClickHouse."""
        pass

    @abstractmethod
    def execute(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> "BaseCursor":
        """Execute a query and return cursor."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connection is active."""
        pass

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


class BaseCursor(ABC):
    """Abstract base class for database cursors."""

    @abstractmethod
    def fetchone(self) -> Optional[Tuple]:
        """Fetch one row."""
        pass

    @abstractmethod
    def fetchmany(self, size: int) -> List[Tuple]:
        """Fetch multiple rows."""
        pass

    @abstractmethod
    def fetchall(self) -> List[Tuple]:
        """Fetch all rows."""
        pass

    @abstractmethod
    def column_names(self) -> List[str]:
        """Get column names."""
        pass

    @abstractmethod
    def column_types(self) -> List[str]:
        """Get column types."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close cursor."""
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Tuple]:
        """Make cursor iterable."""
        pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class CHDBConnection(BaseConnection):
    """CHDB (in-memory ClickHouse) connection implementation.

    Uses chdb.connect() and cursor pattern for database operations.
    Perfect for development and testing.
    """

    def __init__(self, credentials: CHDBCredentials):
        """Initialize CHDB connection.

        Args:
            credentials: CHDB credentials object

        Example:
            >>> from dubai_real_estate.connection.types import CHDBCredentials
            >>> creds = CHDBCredentials(name="dev", database_path=":memory:")
            >>> conn = CHDBConnection(creds)
        """
        super().__init__(credentials)
        self._connection = None

    def connect(self) -> None:
        """Establish CHDB connection.

        Creates connection using chdb.connect() with specified database path.

        Raises:
            ConnectionError: If CHDB connection fails
            ImportError: If chdb package is not installed

        Example:
            >>> conn.connect()
            >>> print("CHDB connected")
        """
        try:
            import chdb
        except ImportError:
            raise ImportError(
                "chdb package is required for CHDB connections. "
                "Install with: pip install chdb"
            )

        try:
            # Create connection using chdb.connect()
            self._connection = chdb.connect(self.credentials.database_path)

            # Test connection with a simple query
            test_cursor = self._connection.cursor()
            test_cursor.execute("SELECT 1")
            test_result = test_cursor.fetchone()
            if not test_result:
                raise Exception("Connection test failed")

            self._connected = True

            logger.info(
                f"CHDB connection '{self.credentials.name}' established "
                f"(database: {self.credentials.database_path})"
            )

        except Exception as e:
            raise ConnectionError(f"Failed to connect to CHDB: {e}")

    def disconnect(self) -> None:
        """Close CHDB connection.

        Properly closes the CHDB connection and releases resources.

        Example:
            >>> conn.disconnect()
        """
        if self.is_connected():
            try:
                self._connection.close()
            except:
                pass  # Ignore close errors
            self._connection = None

        self._connected = False
        logger.info(f"CHDB connection '{self.credentials.name}' disconnected")

    def execute(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> "CHDBCursor":
        """Execute a query on CHDB and return cursor.

        Args:
            query: SQL query to execute
            parameters: Optional query parameters (not supported in CHDB yet)

        Returns:
            CHDB cursor for fetching results

        Raises:
            ConnectionError: If not connected
            RuntimeError: If query execution fails

        Example:
            >>> cursor = conn.execute("SELECT number FROM system.numbers LIMIT 3")
            >>> print(cursor.fetchone())  # (0,)
            >>> cursor.close()
        """
        if not (self.is_connected()):
            try:
                self.connect()
            except Exception as e:
                raise ConnectionError(f"Not connected to CHDB: {e}")

        try:
            if parameters:
                logger.warning("CHDB doesn't support query parameters yet")

            # Create cursor and execute query
            cursor = self._connection.cursor()
            cursor.execute(query)

            return CHDBCursor(cursor)

        except Exception as e:
            raise RuntimeError(f"Query execution failed: {e}")

    def is_connected(self) -> bool:
        """Check if CHDB connection is active.

        Returns:
            True if connected, False otherwise

        Example:
            >>> if conn.is_connected():
            ...     print("CHDB is ready")
        """
        return self._connected and self._connection is not None


class CHDBCursor(BaseCursor):
    """CHDB cursor implementation wrapping chdb cursor."""

    def __init__(self, chdb_cursor):
        """Initialize CHDB cursor wrapper.

        Args:
            chdb_cursor: Native CHDB cursor object
        """
        self._cursor = chdb_cursor
        self._closed = False

    def fetchone(self) -> Optional[Tuple]:
        """Fetch one row from the result set.

        Returns:
            Single row as tuple or None if no more rows

        Example:
            >>> row = cursor.fetchone()
            >>> print(row)  # (0, '0')
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        try:
            return self._cursor.fetchone()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch row: {e}")

    def fetchmany(self, size: int) -> List[Tuple]:
        """Fetch multiple rows from the result set.

        Args:
            size: Number of rows to fetch

        Returns:
            List of rows as tuples

        Example:
            >>> rows = cursor.fetchmany(2)
            >>> print(rows)  # [(1, '1'), (2, '2')]
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        try:
            return self._cursor.fetchmany(size)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch rows: {e}")

    def fetchall(self) -> List[Tuple]:
        """Fetch all remaining rows from the result set.

        Returns:
            List of all rows as tuples

        Example:
            >>> rows = cursor.fetchall()
            >>> print(rows)  # [(0, '0'), (1, '1'), (2, '2')]
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        try:
            return self._cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch all rows: {e}")

    def column_names(self) -> List[str]:
        """Get column names from the result set.

        Returns:
            List of column names

        Example:
            >>> names = cursor.column_names()
            >>> print(names)  # ['number', 'str']
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        try:
            return self._cursor.column_names()
        except Exception as e:
            raise RuntimeError(f"Failed to get column names: {e}")

    def column_types(self) -> List[str]:
        """Get column types from the result set.

        Returns:
            List of column type names

        Example:
            >>> types = cursor.column_types()
            >>> print(types)  # ['UInt64', 'String']
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        try:
            return self._cursor.column_types()
        except Exception as e:
            raise RuntimeError(f"Failed to get column types: {e}")

    def close(self) -> None:
        """Close the cursor and release resources.

        Example:
            >>> cursor.close()
        """
        if not self._closed and self._cursor:
            try:
                self._cursor.close()
            except:
                pass  # Ignore close errors
            self._closed = True

    def __iter__(self) -> Iterator[Tuple]:
        """Make cursor iterable for row-by-row processing.

        Yields:
            Row tuples one by one

        Example:
            >>> for row in cursor:
            ...     print(row)  # (0,), (1,), (2,)
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        try:
            return iter(self._cursor)
        except Exception as e:
            raise RuntimeError(f"Failed to iterate cursor: {e}")


class ClientConnection(BaseConnection):
    """ClickHouse Client connection implementation.

    Uses clickhouse-connect for both server and cloud connections.
    Follows the official ClickHouse Connect API documentation.
    """

    def __init__(self, credentials: ClientCredentials):
        """Initialize client connection.

        Args:
            credentials: Client credentials object

        Example:
            >>> from dubai_real_estate.connection.types import ClientCredentials
            >>> creds = ClientCredentials(
            ...     name="prod",
            ...     host="localhost",
            ...     username="user",
            ...     password="pass"
            ... )
            >>> conn = ClientConnection(creds)
        """
        super().__init__(credentials)
        self._client = None

    def connect(self) -> None:
        """Establish client connection using clickhouse_connect.get_client().

        Uses the official ClickHouse Connect API with proper parameter names:
        - host, port, username, password, database, secure
        - Automatically sets interface based on secure flag
        - Uses HTTP (8123) or HTTPS (8443) based on secure setting

        Raises:
            ConnectionError: If client connection fails
            ImportError: If clickhouse-connect package is not installed

        Example:
            >>> conn.connect()
            >>> print("ClickHouse client connected")
        """
        try:
            import clickhouse_connect
        except ImportError:
            raise ImportError(
                "clickhouse-connect package is required for client connections. "
                "Install with: pip install clickhouse-connect"
            )

        try:
            # Prepare connection parameters according to ClickHouse Connect API
            connection_params = {
                "host": self.credentials.host,
                "port": self.credentials.port,
                "username": self.credentials.username,  # Note: API uses 'username', not 'user'
                "password": self.credentials.password,
                "database": self.credentials.database,
                "secure": self.credentials.secure,
            }

            # Create client using official API
            self._client = clickhouse_connect.get_client(**connection_params)

            # Test connection with a simple command
            self._client.command("SELECT 1")
            self._connected = True

            interface = "https" if self.credentials.secure else "http"
            logger.info(
                f"ClickHouse client connection '{self.credentials.name}' established "
                f"({interface}://{self.credentials.host}:{self.credentials.port})"
            )

        except Exception as e:
            raise ConnectionError(f"Failed to connect to ClickHouse: {e}")

    def disconnect(self) -> None:
        """Close client connection.

        Properly closes the ClickHouse Connect client.

        Example:
            >>> conn.disconnect()
            >>> print("ClickHouse client disconnected")
        """
        if self.is_connected():
            try:
                self._client.close()
            except:
                pass  # Ignore close errors
            self._client = None

        self._connected = False
        logger.info(
            f"ClickHouse client connection '{self.credentials.name}' disconnected"
        )

    def execute(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> "ClientCursor":
        """Execute a query on ClickHouse client and return cursor.

        Uses clickhouse_connect.query() method which returns a QueryResult.

        Args:
            query: SQL query to execute
            parameters: Optional query parameters for parameterized queries

        Returns:
            Client cursor for fetching results

        Raises:
            ConnectionError: If not connected
            RuntimeError: If query execution fails

        Example:
            >>> cursor = conn.execute("SELECT version()")
            >>> row = cursor.fetchone()
            >>> cursor.close()
            >>>
            >>> # Parameterized query
            >>> cursor = conn.execute(
            ...     "SELECT * FROM users WHERE age > {age:UInt8}",
            ...     parameters={'age': 25}
            ... )
        """
        if not (self.is_connected()):
            try:
                self.connect()
            except Exception as e:
                raise ConnectionError(f"Not connected to ClickHouse: {e}")

        try:
            # Use clickhouse_connect query method
            if parameters:
                result = self._client.query(query, parameters=parameters)
            else:
                result = self._client.query(query)

            return ClientCursor(result)

        except Exception as e:
            raise RuntimeError(f"Query execution failed: {e}")

    def command(self, cmd: str) -> Any:
        """Execute a command that doesn't return a result set.

        This is useful for DDL statements, configuration commands, etc.

        Args:
            cmd: ClickHouse command to execute

        Returns:
            Command result (usually string or None)

        Example:
            >>> result = conn.command("SELECT timezone()")
            >>> print(result)  # 'UTC'
            >>>
            >>> conn.command("CREATE DATABASE IF NOT EXISTS test")
        """
        if not (self.is_connected()):
            try:
                self.connect()
            except Exception as e:
                raise ConnectionError(f"Not connected to ClickHouse: {e}")

        try:
            return self._client.command(cmd)
        except Exception as e:
            raise RuntimeError(f"Command execution failed: {e}")

    def is_connected(self) -> bool:
        """Check if client connection is active.

        Tests connection with a simple command.

        Returns:
            True if connected, False otherwise

        Example:
            >>> if conn.is_connected():
            ...     print("ClickHouse client is ready")
        """
        if not self._connected or not self._client:
            return False

        try:
            # Test with a simple command
            self._client.command("SELECT 1")
            return True
        except:
            self._connected = False
            return False

    @property
    def server_version(self) -> str:
        """Get ClickHouse server version.

        Returns:
            Server version string

        Example:
            >>> print(conn.server_version)  # '22.10.1.98'
        """
        if not (self.is_connected()):
            try:
                self.connect()
            except Exception as e:
                raise ConnectionError(f"Not connected to ClickHouse: {e}")

        return self._client.server_version


class ClientCursor(BaseCursor):
    """ClickHouse client cursor implementation wrapping query result."""

    def __init__(self, query_result):
        """Initialize client cursor wrapper.

        Args:
            query_result: ClickHouse query result object
        """
        self._result = query_result
        self._rows = (
            query_result.result_rows if hasattr(query_result, "result_rows") else []
        )
        self._columns = (
            query_result.column_names if hasattr(query_result, "column_names") else []
        )
        self._types = (
            query_result.column_types if hasattr(query_result, "column_types") else []
        )
        self._position = 0
        self._closed = False

    def fetchone(self) -> Optional[Tuple]:
        """Fetch one row from the result set.

        Returns:
            Single row as tuple or None if no more rows
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        if self._position >= len(self._rows):
            return None

        row = self._rows[self._position]
        self._position += 1
        return tuple(row) if isinstance(row, (list, tuple)) else (row,)

    def fetchmany(self, size: int) -> List[Tuple]:
        """Fetch multiple rows from the result set.

        Args:
            size: Number of rows to fetch

        Returns:
            List of rows as tuples
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        end_pos = min(self._position + size, len(self._rows))
        rows = self._rows[self._position : end_pos]
        self._position = end_pos

        return [
            tuple(row) if isinstance(row, (list, tuple)) else (row,) for row in rows
        ]

    def fetchall(self) -> List[Tuple]:
        """Fetch all remaining rows from the result set.

        Returns:
            List of all remaining rows as tuples
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        rows = self._rows[self._position :]
        self._position = len(self._rows)

        return [
            tuple(row) if isinstance(row, (list, tuple)) else (row,) for row in rows
        ]

    def column_names(self) -> List[str]:
        """Get column names from the result set.

        Returns:
            List of column names
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        return list(self._columns)

    def column_types(self) -> List[str]:
        """Get column types from the result set.

        Returns:
            List of column type names
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        # Convert ClickHouse types to string representation
        return [str(col_type) for col_type in self._types]

    def close(self) -> None:
        """Close the cursor and release resources."""
        self._closed = True
        self._result = None
        self._rows = []

    def __iter__(self) -> Iterator[Tuple]:
        """Make cursor iterable for row-by-row processing.

        Yields:
            Row tuples one by one
        """
        if self._closed:
            raise RuntimeError("Cursor is closed")

        for i in range(self._position, len(self._rows)):
            row = self._rows[i]
            yield tuple(row) if isinstance(row, (list, tuple)) else (row,)

        self._position = len(self._rows)
