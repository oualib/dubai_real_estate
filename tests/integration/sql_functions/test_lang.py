"""
Simple tests for MAP functions.
"""

import pytest
from dubai_real_estate.connection.clients import BaseConnection
from dubai_real_estate.sql import get_function_sql


@pytest.mark.integration
def test_is_en(clickhouse_connection: BaseConnection):
    """Test IS_EN function."""
    # Read and format SQL
    sql = get_function_sql("LANG", "check")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'Hello'", True),  # English word
            ("'Test123'", True),  # English with numbers
            ("'Hello World'", True),  # English phrase
            ("'مرحبا'", False),  # Arabic word
            ("'123456'", False),  # Only numbers
            ("'!@#$%'", False),  # Only symbols
            ("'Hello مرحبا'", True),  # Mixed with English
            ("'123 مرحبا'", False),  # Mixed without English
            ("''", False),  # Empty string
            ("'   '", False),  # Only spaces
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT IS_EN({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_first_en(clickhouse_connection: BaseConnection):
    """Test FIRST_EN function."""
    # Read and format SQL
    sql = get_function_sql("LANG", "check")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input_x, input_y, input_z, expected_output)
        test_cases = [
            ("'Hello'", "'مرحبا'", "'Bonjour'", "Hello"),  # First is English
            ("'مرحبا'", "'World'", "'Bonjour'", "World"),  # Second is English
            ("'مرحبا'", "'123'", "'Test'", "Test"),  # Third is English
            ("'Hello'", "'World'", "'Test'", "Hello"),  # All English, returns first
            ("'مرحبا'", "'123'", "'456'", None),  # None are English
            ("''", "'Hello'", "'مرحبا'", "Hello"),  # Empty first, second is English
            ("'Hello World'", "'مرحبا'", "'123'", "Hello World"),  # English phrase
            ("'123 Test'", "'مرحبا'", "'456'", "123 Test"),  # Mixed with English
        ]

        for input_x, input_y, input_z, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT FIRST_EN({input_x}, {input_y}, {input_z})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_first_ar(clickhouse_connection: BaseConnection):
    """Test FIRST_AR function."""
    # Read and format SQL
    sql = get_function_sql("LANG", "check")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input_x, input_y, input_z, expected_output)
        test_cases = [
            ("'مرحبا'", "'Hello'", "'Bonjour'", "مرحبا"),  # First is Arabic
            ("'Hello'", "'مرحبا'", "'Bonjour'", "مرحبا"),  # Second is Arabic
            ("'Hello'", "'World'", "'مرحبا'", "مرحبا"),  # Third is Arabic
            ("'مرحبا'", "'عالم'", "'أهلا'", "مرحبا"),  # All Arabic, returns first
            ("'Hello'", "'World'", "'Test'", None),  # None are Arabic
            ("''", "'مرحبا'", "'Hello'", ""),  # Empty first (not English)
            ("'123'", "'مرحبا'", "'Hello'", "123"),  # Numbers (not English)
            ("'!@#'", "'Hello'", "'مرحبا'", "!@#"),  # Symbols (not English)
            (
                "'123 مرحبا'",
                "'Hello'",
                "'World'",
                "123 مرحبا",
            ),  # Mixed without English letters
        ]

        for input_x, input_y, input_z, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT FIRST_AR({input_x}, {input_y}, {input_z})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output
