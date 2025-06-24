"""
Shared pytest fixtures for all tests.
"""

import os
import pytest
from dubai_real_estate.connection import create_connection


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "slow: marks tests as slow running")


@pytest.fixture
def clickhouse_connection():
    """Shared ClickHouse connection fixture."""
    clickhouse_host = os.getenv("CLICKHOUSE_HOST", "localhost")
    if not clickhouse_host:
        pytest.skip("No ClickHouse server configured")

    conn = create_connection(
        name="test_connection",
        connection_type="client",
        host=clickhouse_host,
        port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
        username=os.getenv("CLICKHOUSE_USERNAME", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", ""),
        database=os.getenv("CLICKHOUSE_DATABASE", "default"),
        save=False,
    )
    conn.connect()
    return conn


@pytest.fixture
def test_db(clickhouse_connection):
    """Test database name with auto-creation."""
    db_name = "test_db"

    # Create database if it doesn't exist
    with clickhouse_connection:
        clickhouse_connection.command(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    return db_name
