"""
Simple tests for create and ingest functions.
"""

from typing import Optional
import pytest
from datetime import datetime, date
from dubai_real_estate.connection.clients import BaseConnection
from dubai_real_estate.sql import get_function_sql, get_table_sql

# GLOBAL VARIABLES
DATABASE_TEST_NAME = "dld_test"
DLD_TABLE_BUILDINGS = "dld_buildings"
DLD_TABLE_UNITS = "dld_units"
DLD_TABLE_OA_SERVICE_CHARGES = "dld_oa_service_charges"
DLD_TABLE_LAND_REGISTRY = "dld_land_registry"
DLD_TABLE_PROJECTS = "dld_projects"


@pytest.mark.integration
@pytest.mark.parametrize(
    "db_name,table_name,date_col,expected_count,expected_min_date,expected_max_date",
    [
        (
            DATABASE_TEST_NAME,
            "dld_valuation",
            "instance_date",
            83426,
            date(2000, 5, 7),
            date(2025, 5, 30),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_brokers",
            "license_start_date",
            8425,
            date(2006, 9, 6),
            date(2025, 5, 31),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_developers",
            "license_issue_date",
            1968,
            date(1978, 3, 8),
            date(2025, 5, 26),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_valuator_licensing",
            "license_start_date",
            117,
            date(2007, 1, 1),
            date(2025, 5, 27),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_units",
            "creation_date",
            2198953,
            date(2008, 10, 14),
            date(2025, 5, 31),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_accredited_escrow_agents",
            None,
            25,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_buildings",
            "creation_date",
            222914,
            date(2008, 10, 14),
            date(2025, 6, 12),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_free_zone_companies_licensing",
            "license_issue_date",
            250,
            date(1995, 10, 14),
            date(2024, 12, 9),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_land_registry",
            None,
            226360,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_licenced_owner_associations",
            None,
            104,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_map_requests",
            "request_date",
            891041,
            date(2003, 2, 11),
            date(2025, 12, 6),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_oa_service_charges",
            None,
            91193,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_offices",
            "license_issue_date",
            4935,
            date(1975, 2, 19),
            date(2023, 9, 26),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_projects",
            "project_start_date",
            2838,
            date(2000, 1, 1),
            date(2026, 5, 1),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_real_estate_licenses",
            "issue_date",
            2788,
            date(1972, 5, 20),
            date(2022, 7, 18),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_real_estate_permits",
            "start_date",
            131529,
            date(2016, 6, 3),
            date(2025, 11, 7),
        ),
        # (
        #     DATABASE_TEST_NAME,
        #     "dld_rent_contracts",
        #     None,
        #     999999999999999,
        #     None,
        #     None,
        # ),
        (
            DATABASE_TEST_NAME,
            "dld_transactions",
            "instance_date",
            1475500,
            date(1970, 1, 1),
            date(2025, 6, 12),
        ),
    ],
)
def test_create_ingest_tables(
    clickhouse_connection: BaseConnection,
    db_name: str,
    table_name: str,
    date_col: Optional[str],
    expected_count: int,
    expected_min_date: date,
    expected_max_date: date,
):
    """Test for create and ingest functions."""
    # Read and format SQL
    sql_create_db = f"CREATE DATABASE IF NOT EXISTS {db_name};"
    sql_format = get_function_sql("FORMAT", "format_type")
    sql_math = get_function_sql("MATH", "cond")
    sql_create = get_table_sql(table_name, "CREATE")
    sql_ingest = get_table_sql(table_name, "INGEST")

    statements = [sql_create_db, sql_format, sql_math, sql_create, sql_ingest]

    with clickhouse_connection:
        # Create functions
        for sql in statements:
            for func in sql.split(";"):
                if func.strip():
                    cursor = clickhouse_connection.execute(
                        func.strip().format(dld_database=db_name, dld_table=table_name)
                    )
                    cursor.close()

        # Test the table
        if isinstance(date_col, str):
            sql = f"""SELECT COUNT(*), MIN("{date_col}"), MAX("{date_col}") FROM "{db_name}"."{table_name}_staging";"""
        else:
            sql = f"""SELECT COUNT(*), NULL, NULL FROM "{db_name}"."{table_name}_staging";"""

        cursor = clickhouse_connection.execute(sql)
        count, min_date, max_date = cursor.fetchone()
        cursor.close()

        assert expected_count <= count

        # Only check dates if expected dates are not None
        if expected_min_date is not None and expected_max_date is not None:
            # Convert to date objects for proper comparison
            min_date_obj = (
                min_date.date() if isinstance(min_date, datetime) else min_date
            )
            max_date_obj = (
                max_date.date() if isinstance(max_date, datetime) else max_date
            )

            assert min_date_obj == expected_min_date
            assert expected_max_date <= max_date_obj


@pytest.mark.integration
@pytest.mark.parametrize(
    "db_name,table_name,date_col,expected_count,expected_min_date,expected_max_date",
    [
        (
            DATABASE_TEST_NAME,
            "dld_valuation",
            "instance_date",
            83426,
            date(2000, 5, 7),
            date(2025, 5, 30),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_brokers",
            "license_start_date",
            8425,
            date(2006, 9, 6),
            date(2025, 5, 31),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_developers",
            "license_issue_date",
            1968,
            date(1978, 3, 8),
            date(2025, 5, 26),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_valuator_licensing",
            "license_start_date",
            117,
            date(2007, 1, 1),
            date(2025, 5, 27),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_units",
            "creation_date",
            2198953,
            date(2008, 10, 14),
            date(2025, 5, 31),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_buildings",
            "creation_date",
            222914,
            date(2008, 10, 14),
            date(2025, 6, 12),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_free_zone_companies_licensing",
            "license_issue_date",
            250,
            date(1995, 10, 14),
            date(2024, 12, 9),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_land_registry",
            None,
            226360,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_licenced_owner_associations",
            None,
            104,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_map_requests",
            "request_date",
            891041,
            date(2003, 2, 11),
            date(2025, 12, 6),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_oa_service_charges",
            None,
            91193,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_offices",
            "license_issue_date",
            4935,
            date(1975, 2, 19),
            date(2023, 9, 26),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_projects",
            "project_start_date",
            2838,
            date(2000, 1, 1),
            date(2026, 5, 1),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_real_estate_licenses",
            "license_issue_date",
            2788,
            date(1972, 5, 20),
            date(2022, 7, 18),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_real_estate_permits",
            "start_date",
            131529,
            date(2016, 6, 3),
            date(2025, 11, 7),
        ),
        # (
        #     DATABASE_TEST_NAME,
        #     "dld_rent_contracts",
        #     None,
        #     999999999999999,
        #     None,
        #     None,
        # ),
        (
            DATABASE_TEST_NAME,
            "dld_transactions",
            "instance_date",
            1475500,
            date(1970, 1, 1),
            date(2025, 6, 12),
        ),
    ],
)
def test_clean_views(
    clickhouse_connection: BaseConnection,
    db_name: str,
    table_name: str,
    date_col: Optional[str],
    expected_count: int,
    expected_min_date: date,
    expected_max_date: date,
):
    """Test for create and ingest functions."""
    # Read and format SQL
    sql_clean = get_table_sql(table_name, "CLEAN_VIEW")

    statements = [sql_clean]

    with clickhouse_connection:
        # Create functions
        for sql in statements:
            for func in sql.split(";"):
                if func.strip():
                    cursor = clickhouse_connection.execute(
                        func.strip().format(
                            dld_database=db_name,
                            dld_table=table_name,
                            buildings=DLD_TABLE_BUILDINGS,
                            units=DLD_TABLE_UNITS,
                            oa_service_charges=DLD_TABLE_OA_SERVICE_CHARGES,
                            land_registry=DLD_TABLE_LAND_REGISTRY,
                            projects=DLD_TABLE_PROJECTS,
                        )
                    )
                    cursor.close()

        # Test the table
        if isinstance(date_col, str):
            sql = f"""SELECT COUNT(*), MIN("{date_col}"), MAX("{date_col}") FROM "{db_name}"."{table_name}_staging_clean";"""
        else:
            sql = f"""SELECT COUNT(*), NULL, NULL FROM "{db_name}"."{table_name}_staging_clean";"""

        cursor = clickhouse_connection.execute(sql)
        count, min_date, max_date = cursor.fetchone()
        cursor.close()

        assert expected_count <= count

        # Only check dates if expected dates are not None
        if expected_min_date is not None and expected_max_date is not None:
            # Convert to date objects for proper comparison
            min_date_obj = (
                min_date.date() if isinstance(min_date, datetime) else min_date
            )
            max_date_obj = (
                max_date.date() if isinstance(max_date, datetime) else max_date
            )

            assert min_date_obj == expected_min_date
            assert expected_max_date <= max_date_obj


@pytest.mark.integration
@pytest.mark.parametrize(
    "db_name,table_name,date_col,expected_count,expected_min_date,expected_max_date",
    [
        (
            DATABASE_TEST_NAME,
            "dld_valuation",
            "instance_date",
            83426,
            date(2000, 5, 7),
            date(2025, 5, 30),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_brokers",
            "license_start_date",
            8425,
            date(2006, 9, 6),
            date(2025, 5, 31),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_developers",
            "license_issue_date",
            1968,
            date(1978, 3, 8),
            date(2025, 5, 26),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_valuator_licensing",
            "license_start_date",
            117,
            date(2007, 1, 1),
            date(2025, 5, 27),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_units",
            "creation_date",
            2198953,
            date(2008, 10, 14),
            date(2025, 5, 31),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_buildings",
            "creation_date",
            222914,
            date(2008, 10, 14),
            date(2025, 6, 12),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_free_zone_companies_licensing",
            "license_issue_date",
            250,
            date(1995, 10, 14),
            date(2024, 12, 9),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_land_registry",
            None,
            226360,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_licenced_owner_associations",
            None,
            104,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_map_requests",
            "request_date",
            891041,
            date(2003, 2, 11),
            date(2025, 12, 6),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_oa_service_charges",
            None,
            91193,
            None,
            None,
        ),
        (
            DATABASE_TEST_NAME,
            "dld_offices",
            "license_issue_date",
            4935,
            date(1975, 2, 19),
            date(2023, 9, 26),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_projects",
            "project_start_date",
            2838,
            date(2000, 1, 1),
            date(2026, 5, 1),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_real_estate_licenses",
            "license_issue_date",
            2788,
            date(1972, 5, 20),
            date(2022, 7, 18),
        ),
        (
            DATABASE_TEST_NAME,
            "dld_real_estate_permits",
            "start_date",
            131529,
            date(2016, 6, 3),
            date(2025, 11, 7),
        ),
        # (
        #     DATABASE_TEST_NAME,
        #     "dld_rent_contracts",
        #     None,
        #     999999999999999,
        #     None,
        #     None,
        # ),
        (
            DATABASE_TEST_NAME,
            "dld_transactions",
            "instance_date",
            1475500,
            date(1970, 1, 1),
            date(2025, 6, 12),
        ),
    ],
)
def test_prod_views(
    clickhouse_connection: BaseConnection,
    db_name: str,
    table_name: str,
    date_col: Optional[str],
    expected_count: int,
    expected_min_date: date,
    expected_max_date: date,
):
    """Test for create and ingest functions."""
    # Read and format SQL
    sql_clean = get_table_sql(table_name, "PROD_VIEW")

    statements = [sql_clean]

    with clickhouse_connection:
        # Create functions
        for sql in statements:
            for func in sql.split(";"):
                if func.strip():
                    cursor = clickhouse_connection.execute(
                        func.strip().format(
                            dld_database=db_name,
                            dld_table=table_name,
                        )
                    )
                    cursor.close()

        # Test the table
        if isinstance(date_col, str):
            sql = f"""SELECT COUNT(*), MIN("{date_col}"), MAX("{date_col}") FROM "{db_name}"."{table_name}_view";"""
        else:
            sql = (
                f"""SELECT COUNT(*), NULL, NULL FROM "{db_name}"."{table_name}_view";"""
            )

        cursor = clickhouse_connection.execute(sql)
        count, min_date, max_date = cursor.fetchone()
        cursor.close()

        assert expected_count <= count

        # Only check dates if expected dates are not None
        if expected_min_date is not None and expected_max_date is not None:
            # Convert to date objects for proper comparison
            min_date_obj = (
                min_date.date() if isinstance(min_date, datetime) else min_date
            )
            max_date_obj = (
                max_date.date() if isinstance(max_date, datetime) else max_date
            )

            assert min_date_obj == expected_min_date
            assert expected_max_date <= max_date_obj
