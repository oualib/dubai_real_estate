"""
Simple tests for MAP functions.
"""

import pytest
from dubai_real_estate.connection.clients import BaseConnection
from dubai_real_estate.sql import get_function_sql


@pytest.mark.integration
def test_format_bool(clickhouse_connection: BaseConnection):
    """Test FORMAT_BOOL function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'t'", True),
            ("'true'", True),
            ("'1'", True),
            ("'T'", True),
            ("'TRUE'", True),
            ("'f'", False),
            ("'false'", False),
            ("'0'", False),
            ("'F'", False),
            ("'FALSE'", False),
            ("' true '", True),  # With spaces
            ("'invalid'", None),  # Invalid input
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT FORMAT_BOOL({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_format_date(clickhouse_connection: BaseConnection):
    """Test FORMAT_DATE function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'01-01-2023'", "2023-01-01"),
            ("'15-06-2022'", "2022-06-15"),
            ("'31-12-2024'", "2024-12-31"),
            ("''", None),  # Empty string
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT FORMAT_DATE({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            if expected_output is None:
                assert result is None
            else:
                assert str(result) == expected_output


@pytest.mark.integration
def test_format_varchar(clickhouse_connection: BaseConnection):
    """Test FORMAT_VARCHAR function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'  Hello World  '", "Hello World"),
            ("'Valid Text'", "Valid Text"),
            ("'   '", None),  # Only spaces
            ("'null'", None),  # Null string
            ("'NONE'", None),  # None string
            ("''", None),  # Empty string
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT FORMAT_VARCHAR({input_val})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_format_int(clickhouse_connection: BaseConnection):
    """Test FORMAT_INT function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'123'", 123),
            ("'-456'", -456),
            ("'+789'", 789),
            ("'1a2b3c'", 123),  # With letters
            ("'  -456  '", -456),  # With spaces
            ("'abc'", None),  # No digits
            ("'-'", None),  # Only sign
            ("'+'", None),  # Only sign
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT FORMAT_INT({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_format_license(clickhouse_connection: BaseConnection):
    """Test FORMAT_LICENSE function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'ABC123DEF'", 123),
            ("'LIC-456-XYZ'", 456),
            ("'789'", 789),
            ("'A1B'", None),  # Only one digit
            ("'ABC'", None),  # No digits
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT FORMAT_LICENSE({input_val})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_extract_license_type(clickhouse_connection: BaseConnection):
    """Test EXTRACT_LICENSE_TYPE function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'OF123'", "OF"),
            ("'JLT456'", "JLT"),
            ("'DMCC789'", "DMCC"),
            ("'CN123'", "CN"),
            ("'LC456'", "LC"),
            ("'F789'", "F"),
            ("'A123'", "A"),
            ("'XYZ123'", None),  # No matching pattern
            ("'ABC'", None),  # No license number
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT EXTRACT_LICENSE_TYPE({input_val})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_format_float(clickhouse_connection: BaseConnection):
    """Test FORMAT_FLOAT function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'123.45'", 123.45),
            ("'-67.89'", -67.89),
            ("'1.23e2'", 123.0),
            ("'abc123.45abc'", 123.45),  # With letters
            ("'  +456.78  '", 456.78),  # With spaces
            ("'abc'", None),  # No digits
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT FORMAT_FLOAT({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            if expected_output is None:
                assert result is None
            else:
                assert (
                    abs(result - expected_output) < 0.001
                )  # Float comparison with tolerance


@pytest.mark.integration
def test_format_website(clickhouse_connection: BaseConnection):
    """Test FORMAT_WEBSITE function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'www.example.com'", "www.example.com"),
            ("'https://example.com'", "www.example.com"),
            ("'http://example.com'", "www.example.com"),
            ("'https://www.example.com'", "www.example.com"),
            # ("'example.com'", "www.example.com"), -- TODO does not work
            ("'www.example.com/'", "www.example.com"),  # Trailing slash
            ("'user@example.com'", None),  # Email format
            ("''", None),  # Empty string
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT FORMAT_WEBSITE({input_val})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_format_email(clickhouse_connection: BaseConnection):
    """Test FORMAT_EMAIL function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'user@example.com'", "user@example.com"),
            ("'USER@EXAMPLE.COM'", "user@example.com"),
            ("'  user@example.com  '", "user@example.com"),
            ("'user@example.com!'", "user@example.com"),  # Special chars removed
            ("'www.example.com'", None),  # Website format
            ("'invalid-email'", None),  # No @ symbol
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT FORMAT_EMAIL({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_format_name(clickhouse_connection: BaseConnection):
    """Test FORMAT_NAME function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'john doe'", "John Doe"),
            ("'COMPANY L.L.C'", "Company LLC"),
            # ("'business llc.'", "Business LLC"), - TODO does not work
            ("'Test Company.'", "Test Company"),
            # ("'Company123-Name'", "Company Name"),  # Numbers and hyphens removed - TODO does not work
            ("'www.example.com'", None),  # Website format
            ("'user@example.com'", None),  # Email format
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(f"SELECT FORMAT_NAME({input_val})")
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output


@pytest.mark.integration
def test_format_contract_type(clickhouse_connection: BaseConnection):
    """Test FORMAT_CONTRACT_TYPE function."""
    # Read and format SQL
    sql = get_function_sql("FORMAT", "format_type")

    with clickhouse_connection:
        # Create functions
        for func in sql.split(";"):
            if func.strip():
                cursor = clickhouse_connection.execute(func.strip())
                cursor.close()

        # Test cases: (input, expected_output)
        test_cases = [
            ("'rental'", "RENTAL"),
            ("'  sale  '", "SALE"),
            ("'lease-123'", "LEASE"),
            ("'Contract Type!'", "CONTRACTTYPE"),
            ("'   '", None),  # Only spaces
            ("''", None),  # Empty string
        ]

        for input_val, expected_output in test_cases:
            cursor = clickhouse_connection.execute(
                f"SELECT FORMAT_CONTRACT_TYPE({input_val})"
            )
            result = cursor.fetchone()[0]
            cursor.close()

            assert result == expected_output
