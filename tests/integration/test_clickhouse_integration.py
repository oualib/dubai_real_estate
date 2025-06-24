"""
Integration tests with real ClickHouse server.
Only runs when ClickHouse is available.
"""

import pytest
import os
from dubai_real_estate.connection import create_connection, get_connection


@pytest.mark.integration
def test_clickhouse_server_connection():
    """Test real ClickHouse server connection."""
    # Skip if no ClickHouse server available
    clickhouse_host = os.getenv("CLICKHOUSE_HOST", "localhost")
    if not clickhouse_host:
        pytest.skip("No ClickHouse server configured")

    # Create real connection
    conn = create_connection(
        name="integration_test",
        connection_type="client",
        host=clickhouse_host,
        port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
        username=os.getenv("CLICKHOUSE_USERNAME", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", ""),
        database=os.getenv("CLICKHOUSE_DATABASE", "default"),
        save=False,
    )
    conn.connect()

    # Test connection
    with conn:
        # Basic query
        cursor = conn.execute("SELECT 1 as test")
        result = cursor.fetchone()
        assert result == (1,)
        cursor.close()

        # Version query
        cursor = conn.execute("SELECT version()")
        version = cursor.fetchone()
        assert version is not None
        cursor.close()

        # Create test table
        conn.command(
            "CREATE TABLE IF NOT EXISTS test_table (id UInt32, name String) ENGINE = Memory"
        )

        # Insert data
        conn.command("INSERT INTO test_table VALUES (1, 'test')")

        # Query data
        cursor = conn.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        assert len(rows) >= 1
        cursor.close()

        # Cleanup
        conn.command("DROP TABLE IF EXISTS test_table")


@pytest.mark.integration
def test_chdb_connection():
    """Test CHDB in-memory connection."""
    if os.getenv("CI"):
        pytest.skip(
            "CHDB tests skipped in CI - connection lifecycle issues with chdb package"
        )

    conn = create_connection(
        name="chdb_integration_test",
        connection_type="chdb",
        database_path=":memory:",
        save=False,
    )

    conn.connect()
    cursor = conn.execute("SELECT 1 as test")
    result = cursor.fetchone()
    assert result == (1,)
    cursor.close()
    conn.disconnect()
