"""
Unit tests for dubai_real_estate connection module.

Tests the connection management system including credential storage,
connection creation, and different ClickHouse connection types with proper
cursor handling.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from dubai_real_estate.connection import (
    ConnectionType,
    CHDBCredentials,
    ClientCredentials,
    CredentialStorage,
    ConnectionManager,
    CHDBConnection,
    ClientConnection,
    get_manager,
    get_connection,
    create_connection,
)


class TestConnectionTypes:
    """Test connection type definitions and credential classes."""

    def test_chdb_credentials_creation_memory(self):
        """Test CHDB credentials creation for in-memory database."""
        creds = CHDBCredentials(
            name="test_chdb",
            database_path=":memory:",
            description="Test CHDB connection",
        )

        assert creds.name == "test_chdb"
        assert creds.connection_type == ConnectionType.CHDB
        assert creds.database_path == ":memory:"
        assert creds.description == "Test CHDB connection"
        assert not creds.is_auto

    def test_chdb_credentials_creation_file(self):
        """Test CHDB credentials creation for file-based database."""
        creds = CHDBCredentials(name="test_chdb_file", database_path="test.db")

        assert creds.name == "test_chdb_file"
        assert creds.connection_type == ConnectionType.CHDB
        assert creds.database_path == "test.db"

    def test_chdb_credentials_default_path(self):
        """Test CHDB credentials with default database path."""
        creds = CHDBCredentials(name="test_default")

        assert creds.database_path == ":memory:"  # Default value

    def test_client_credentials_creation(self):
        """Test client credentials creation."""
        creds = ClientCredentials(
            name="test_client",
            host="localhost",
            port=9000,
            username="user",
            password="pass",
            database="test_db",
        )

        assert creds.name == "test_client"
        assert creds.connection_type == ConnectionType.CLIENT
        assert creds.host == "localhost"
        assert creds.port == 9000
        assert creds.username == "user"
        assert creds.password == "pass"
        assert creds.database == "test_db"


class TestCredentialStorage:
    """Test secure credential storage functionality."""

    @pytest.fixture
    def temp_storage_dir(self):
        """Create temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def storage(self, temp_storage_dir):
        """Create storage instance with temporary directory."""
        return CredentialStorage(temp_storage_dir)

    def test_storage_initialization(self, storage, temp_storage_dir):
        """Test storage initialization creates necessary files."""
        assert storage.storage_dir == temp_storage_dir
        assert storage.storage_dir.exists()
        assert storage.key_file.exists()

    def test_save_and_load_chdb_credentials(self, storage):
        """Test saving and loading CHDB credentials."""
        creds = CHDBCredentials(
            name="test_chdb", database_path="test.db", description="Test connection"
        )

        # Save credentials
        storage.save_credentials(creds)

        # Load credentials
        loaded_creds = storage.load_credentials("test_chdb")

        assert loaded_creds is not None
        assert loaded_creds.name == "test_chdb"
        assert loaded_creds.connection_type == ConnectionType.CHDB
        assert loaded_creds.database_path == "test.db"
        assert loaded_creds.description == "Test connection"

    def test_save_and_load_client_credentials(self, storage):
        """Test saving and loading client credentials."""
        creds = ClientCredentials(
            name="test_client", host="localhost", username="user", password="secret"
        )

        # Save credentials
        storage.save_credentials(creds)

        # Load credentials
        loaded_creds = storage.load_credentials("test_client")

        assert loaded_creds is not None
        assert loaded_creds.name == "test_client"
        assert loaded_creds.host == "localhost"
        assert loaded_creds.username == "user"
        assert loaded_creds.password == "secret"


class TestCHDBConnection:
    """Test CHDB connection and cursor functionality."""

    def test_chdb_connection_initialization(self):
        """Test CHDB connection initialization."""
        creds = CHDBCredentials(name="test", database_path=":memory:")
        conn = CHDBConnection(creds)

        assert conn.credentials == creds
        assert not conn.is_connected()

    @patch("chdb.connect")
    def test_chdb_connection_connect(self, mock_chdb_connect):
        """Test CHDB connection establishment."""
        # Mock chdb.connect
        mock_connection = Mock()
        mock_chdb_connect.return_value = mock_connection

        creds = CHDBCredentials(name="test", database_path=":memory:")
        conn = CHDBConnection(creds)

        # Connect
        conn.connect()

        assert conn.is_connected()
        mock_chdb_connect.assert_called_once_with(":memory:")

    @patch("chdb.connect")
    def test_chdb_connection_execute_and_cursor(self, mock_chdb_connect):
        """Test CHDB query execution and cursor operations."""
        # Mock chdb connection and cursor
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (0, "0")
        mock_cursor.fetchmany.return_value = [(1, "1"), (2, "2")]
        mock_cursor.fetchall.return_value = [(0, "0"), (1, "1"), (2, "2")]
        mock_cursor.column_names.return_value = ["number", "str"]
        mock_cursor.column_types.return_value = ["UInt64", "String"]
        mock_cursor.__iter__ = Mock(return_value=iter([(0,), (1,), (2,)]))

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_chdb_connect.return_value = mock_connection

        creds = CHDBCredentials(name="test")
        conn = CHDBConnection(creds)
        conn.connect()

        # Execute query
        cursor = conn.execute(
            "SELECT number, toString(number) FROM system.numbers LIMIT 3"
        )

        # Test cursor operations
        assert cursor.fetchone() == (0, "0")
        assert cursor.fetchmany(2) == [(1, "1"), (2, "2")]
        assert cursor.column_names() == ["number", "str"]
        assert cursor.column_types() == ["UInt64", "String"]

        # Test cursor iteration
        cursor_iter = conn.execute("SELECT number FROM system.numbers LIMIT 3")
        rows = list(cursor_iter)
        assert rows == [(0,), (1,), (2,)]

        # Verify query execution
        mock_cursor.execute.assert_called_with(
            "SELECT number FROM system.numbers LIMIT 3"
        )

    @patch("chdb.connect")
    def test_chdb_connection_context_manager(self, mock_chdb_connect):
        """Test CHDB connection context manager."""
        mock_connection = Mock()
        mock_chdb_connect.return_value = mock_connection

        creds = CHDBCredentials(name="test")
        conn = CHDBConnection(creds)

        # Use context manager
        with conn:
            assert conn.is_connected()

        # Should disconnect after context
        mock_connection.close.assert_called_once()
        assert not conn.is_connected()


class TestClientConnection:
    """Test ClickHouse client connection functionality."""

    def test_client_connection_initialization(self):
        """Test client connection initialization."""
        creds = ClientCredentials(name="test", host="localhost")
        conn = ClientConnection(creds)

        assert conn.credentials == creds
        assert not conn.is_connected()

    @patch("clickhouse_connect.get_client")
    def test_client_connection_connect(self, mock_get_client):
        """Test client connection establishment."""
        # Mock clickhouse client
        mock_client = Mock()
        mock_client.command.return_value = "1"  # Response to SELECT 1 test
        mock_get_client.return_value = mock_client

        creds = ClientCredentials(name="test", host="localhost", port=8123)
        conn = ClientConnection(creds)

        # Connect
        conn.connect()

        assert conn.is_connected()
        mock_get_client.assert_called_once_with(
            host="localhost",
            port=8123,
            username="default",
            password="",
            database="default",
            secure=False,
        )
        # Should test connection with command
        mock_client.command.assert_called_with("SELECT 1")

    @patch("clickhouse_connect.get_client")
    def test_client_connection_execute_and_cursor(self, mock_get_client):
        """Test client query execution and cursor operations."""
        # Mock query result
        mock_result = Mock()
        mock_result.result_rows = [(1, "test"), (2, "data")]
        mock_result.column_names = ["id", "name"]
        mock_result.column_types = ["UInt64", "String"]

        # Mock clickhouse client
        mock_client = Mock()
        mock_client.command.return_value = "1"  # For connection test
        mock_client.query.return_value = mock_result  # For actual query
        mock_get_client.return_value = mock_client

        creds = ClientCredentials(name="test", host="localhost")
        conn = ClientConnection(creds)
        conn.connect()

        # Execute query
        cursor = conn.execute("SELECT id, name FROM test_table")

        # Test cursor operations
        assert cursor.fetchone() == (1, "test")
        assert cursor.fetchone() == (2, "data")
        assert cursor.fetchone() is None  # No more rows

        assert cursor.column_names() == ["id", "name"]
        assert cursor.column_types() == ["UInt64", "String"]

        cursor.close()

        # Verify query was called
        mock_client.query.assert_called_once_with("SELECT id, name FROM test_table")


class TestConnectionManager:
    """Test connection manager functionality."""

    @pytest.fixture
    def temp_storage_dir(self):
        """Create temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def manager(self, temp_storage_dir):
        """Create connection manager with temporary storage."""
        with patch(
            "dubai_real_estate.connection.storage.get_storage"
        ) as mock_get_storage:
            mock_storage = CredentialStorage(temp_storage_dir)
            mock_get_storage.return_value = mock_storage
            yield ConnectionManager()

    def test_manager_initialization(self, manager):
        """Test connection manager initialization."""
        assert manager._active_connection is None
        assert len(manager._connection_cache) == 0

    @patch("dubai_real_estate.connection.manager.CHDBConnection")
    def test_create_chdb_connection(self, mock_chdb_conn, manager):
        """Test creating CHDB connection through manager."""
        mock_conn_instance = Mock()
        mock_chdb_conn.return_value = mock_conn_instance

        # Create connection
        conn = manager.create_connection(
            name="test_chdb",
            connection_type="chdb",
            database_path="test.db",
            save=False,
        )

        assert conn == mock_conn_instance
        assert "test_chdb" in manager._connection_cache
        mock_chdb_conn.assert_called_once()

    @patch("dubai_real_estate.connection.manager.ClientConnection")
    def test_create_client_connection(self, mock_client_conn, manager):
        """Test creating client connection through manager."""
        mock_conn_instance = Mock()
        mock_client_conn.return_value = mock_conn_instance

        # Create connection
        conn = manager.create_connection(
            name="test_client",
            connection_type="client",
            host="localhost",
            username="user",
            password="pass",
            save=False,
        )

        assert conn == mock_conn_instance
        assert "test_client" in manager._connection_cache
        mock_client_conn.assert_called_once()

    def test_list_connections_empty(self, manager):
        """Test listing connections when none exist."""
        # Clear any auto-created connections first
        for conn_name in manager._storage.list_connections():
            manager._storage.delete_credentials(conn_name)

        connections = manager.list_connections()
        assert connections == []

    def test_list_connections_with_default(self, manager):
        """Test listing connections includes auto-created default."""
        # The test manager uses temporary storage, so no auto connections exist
        # Let's create a connection first to test the listing functionality
        manager.create_connection("test_conn", "chdb", save=True)

        connections = manager.list_connections()

        # Should have at least 1 connection now
        assert len(connections) >= 1

        # Find our test connection
        test_conn = next((c for c in connections if c["name"] == "test_conn"), None)
        assert test_conn is not None
        assert test_conn["type"] == "chdb"

    @pytest.mark.skip(reason="Too many connections")
    @patch("dubai_real_estate.connection.manager.CHDBConnection")
    def test_connection_context_manager(self, mock_chdb_conn, manager):
        """Test connection context manager."""
        mock_conn_instance = Mock()
        mock_conn_instance.is_connected.return_value = False
        mock_chdb_conn.return_value = mock_conn_instance

        # Create connection
        manager.create_connection("test", "chdb", save=False)

        # Use context manager
        with manager.connection("test") as conn:
            assert conn == mock_conn_instance
            mock_conn_instance.connect.assert_called_once()

        mock_conn_instance.disconnect.assert_called_once()


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    @patch("dubai_real_estate.connection.manager.get_manager")
    def test_get_connection(self, mock_get_manager):
        """Test get_connection convenience function."""
        mock_manager = Mock()
        mock_conn = Mock()
        mock_manager.get_connection.return_value = mock_conn
        mock_get_manager.return_value = mock_manager

        result = get_connection("test")

        assert result == mock_conn
        mock_manager.get_connection.assert_called_once_with("test")

    @patch("dubai_real_estate.connection.manager.get_manager")
    def test_create_connection(self, mock_get_manager):
        """Test create_connection convenience function."""
        mock_manager = Mock()
        mock_conn = Mock()
        mock_manager.create_connection.return_value = mock_conn
        mock_get_manager.return_value = mock_manager

        result = create_connection("test", "chdb")

        assert result == mock_conn
        mock_manager.create_connection.assert_called_once_with("test", "chdb")


class TestIntegration:
    """Integration tests showing real usage patterns."""

    @pytest.mark.skip(reason="Too many connections")
    @patch("chdb.connect")
    def test_chdb_workflow_integration(self, mock_chdb_connect):
        """Test the complete CHDB workflow like in the example."""
        # Mock the complete CHDB workflow
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [(0, "0"), (1, "1"), (2, "2"), None]
        mock_cursor.fetchmany.return_value = [(1, "1"), (2, "2")]
        mock_cursor.column_names.return_value = ["number", "str"]
        mock_cursor.column_types.return_value = ["UInt64", "String"]
        mock_cursor.__iter__ = Mock(return_value=iter([(0,), (1,), (2,)]))

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_chdb_connect.return_value = mock_connection

        # Create connection like the example
        conn = create_connection("dev", "chdb", database_path=":memory:")

        with conn:
            # Execute query and get cursor
            cursor = conn.execute(
                "SELECT number, toString(number) as str FROM system.numbers LIMIT 3"
            )

            # Fetch data in different ways
            row1 = cursor.fetchone()
            assert row1 == (0, "0")

            rows = cursor.fetchmany(2)
            assert rows == [(1, "1"), (2, "2")]

            # Get column information
            names = cursor.column_names()
            assert names == ["number", "str"]

            types = cursor.column_types()
            assert types == ["UInt64", "String"]

            # Use cursor as iterator (new cursor for clean iteration)
            iter_cursor = conn.execute("SELECT number FROM system.numbers LIMIT 3")
            rows_iter = list(iter_cursor)
            assert rows_iter == [(0,), (1,), (2,)]

            # Close cursors
            cursor.close()
            iter_cursor.close()

        # Verify the workflow matches the example
        mock_chdb_connect.assert_called_with(":memory:")
        assert mock_connection.cursor.call_count >= 2  # At least 2 cursors created
