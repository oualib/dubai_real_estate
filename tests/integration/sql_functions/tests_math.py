"""
Simple tests for MAP functions.
"""

import pytest
from dubai_real_estate.connection.clients import BaseConnection
from dubai_real_estate.sql import get_function_sql


@pytest.mark.integration
def test_nullifneg(clickhouse_connection: BaseConnection):
    """Test NULLIFNEG function."""
    # Read and format SQL
    sql = get_function_sql("MATH", "cond")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            (5, 5),  # Positive number
            (0, 0),  # Zero (should return 0)
            (-1, None),  # Negative number (should return NULL)
            (-10, None),  # Negative number (should return NULL)
            (100, 100),  # Large positive number
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT NULLIFNEG({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_nullifnegs(clickhouse_connection: BaseConnection):
    """Test NULLIFNEGS function."""
    # Read and format SQL
    sql = get_function_sql("MATH", "cond")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            (5, 5),  # Positive number
            (0, None),  # Zero (should return NULL - strict version)
            (-1, None),  # Negative number (should return NULL)
            (-10, None),  # Negative number (should return NULL)
            (100, 100),  # Large positive number
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT NULLIFNEGS({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output
