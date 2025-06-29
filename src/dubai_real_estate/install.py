"""
Dubai Real Estate Database Installation Module

This module provides functions to install the complete Dubai Real Estate database system:
1. Create database if it doesn't exist (default: 'dubai_real_estate')
2. Install all SQL functions (FORMAT, MATH, LANG, MAP)
3. Create all tables with proper schemas
4. Ingest data into staging tables
5. Create clean views with data transformations
6. Create final production views
7. Create production tables (CREATE_PROD + INGEST_PROD)
8. Clean up staging tables and views

The API automatically uses the auto connection when available, making it simple to use.

Usage:
    from dubai_real_estate.install import install_database, install_functions, install_tables
    from dubai_real_estate.connection import create_connection

    # Set up connection once
    create_connection("prod", "client", host="clickhouse.company.com", set_auto=True)

    # Now all install functions use the auto connection automatically
    success = install_database()  # Uses default database 'dubai_real_estate'
    success = install_database("dld_prod")  # Custom database name

    # Production deployment with cleanup
    success = install_database(include_prod_tables=True, cleanup_after_prod=True)

    # Install specific components
    install_functions()
    install_tables("dld_test", table_names=["dld_transactions", "dld_units"])
    install_prod_tables()  # Final production tables
    drop_staging_and_views()  # Cleanup

    # Get installation status
    status = get_installation_status()  # Uses default database
"""

import logging
import time
from typing import List, Optional, Dict, Any
from datetime import datetime

from .connection import get_connection, BaseConnection
from .sql import SQLParser, get_table_sql, get_function_sql

logger = logging.getLogger(__name__)

# Default database name
DEFAULT_DATABASE = "dubai_real_estate"

# Table installation order (dependencies matter)
TABLE_INSTALL_ORDER = [
    # Core reference tables (no dependencies)
    "dld_accredited_escrow_agents",
    "dld_licenced_owner_associations",
    # Building and property tables
    "dld_land_registry",
    "dld_buildings",
    "dld_units",
    # Project and development tables
    "dld_projects",
    "dld_developers",
    # Licensing tables
    "dld_brokers",
    "dld_offices",
    "dld_real_estate_licenses",
    "dld_valuator_licensing",
    "dld_free_zone_companies_licensing",
    # Transaction and activity tables
    "dld_transactions",
    "dld_valuation",
    "dld_real_estate_permits",
    "dld_map_requests",
    # Service and operational tables
    "dld_oa_service_charges",
    "dld_rent_contracts",  # Can be large - install last
]

# Function categories to install
FUNCTION_CATEGORIES = ["FORMAT", "MATH", "LANG", "MAP"]

# Referenced table variables for clean views
TABLE_VARIABLES = {
    "buildings": "dld_buildings",
    "units": "dld_units",
    "oa_service_charges": "dld_oa_service_charges",
    "land_registry": "dld_land_registry",
    "projects": "dld_projects",
}

# Maximum number of retries for data ingestion
# (sensitive to HTTP connection timeouts)
MAX_RETRY = 20


class InstallationError(Exception):
    """Raised when installation fails."""

    pass


def _get_connection() -> BaseConnection:
    """Get the auto connection or raise error if none available.

    Returns:
        ClickHouse connection

    Raises:
        InstallationError: If no connection is available
    """
    connection = get_connection()  # Gets auto connection
    if not connection:
        raise InstallationError(
            "No auto connection available. Please create a connection first:\n"
            "from dubai_real_estate.connection import create_connection\n"
            "create_connection('my_conn', 'client', host='localhost', set_auto=True)"
        )
    return connection


def _execute_sql(
    connection: BaseConnection, sql: str, description: str = "", dry_run: bool = False
) -> bool:
    """Execute SQL statement with error handling.

    Args:
        connection: ClickHouse connection
        sql: SQL statement to execute
        description: Human-readable description for logging
        dry_run: If True, log what would be executed without running

    Returns:
        True if successful, False if error
    """
    try:
        if dry_run:
            logger.info(f"DRY RUN: Would execute {description}")
            logger.debug(f"SQL: {sql[:100]}{'...' if len(sql) > 100 else ''}")
            return True

        # Split SQL into individual statements
        statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]

        for stmt in statements:
            if stmt:
                cursor = connection.execute(stmt)
                cursor.close()

        if description:
            logger.info(f"✓ {description}")
        return True

    except Exception as e:
        logger.error(f"✗ Failed to execute {description}: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Failed SQL: {sql}")
        return False


def create_database(
    database_name: str = DEFAULT_DATABASE, dry_run: bool = False
) -> bool:
    """Create database if it doesn't exist.

    Args:
        database_name: Database name to create (default: 'dubai_real_estate')
        dry_run: If True, show what would be done without executing

    Returns:
        True if successful, False if error

    Example:
        >>> from dubai_real_estate.install import create_database
        >>> success = create_database()  # Creates 'dubai_real_estate' database
        >>> success = create_database("dld_production")  # Custom name
    """
    connection = _get_connection()
    logger.info(f"Creating database: {database_name}")

    create_sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}`"

    with connection:
        return _execute_sql(
            connection, create_sql, f"Create database '{database_name}'", dry_run
        )


def install_functions(
    categories: Optional[List[str]] = None, dry_run: bool = False
) -> Dict[str, Any]:
    """Install SQL functions using auto connection.

    Args:
        categories: Function categories to install (default: all)
        dry_run: If True, show what would be done without executing

    Returns:
        Dict with installation results and statistics

    Example:
        >>> from dubai_real_estate.install import install_functions
        >>> result = install_functions(categories=["FORMAT", "MAP"])
        >>> print(f"Installed {result['functions_installed']} functions")
    """
    connection = _get_connection()

    if categories is None:
        categories = FUNCTION_CATEGORIES

    logger.info(f"Installing SQL functions: {categories}")

    sql_parser = SQLParser()
    stats = {"functions_installed": 0, "errors": 0, "categories": []}

    with connection:
        for category in categories:
            try:
                logger.info(f"Installing {category} functions...")

                # Get function types in this category
                function_types = sql_parser.list_function_types()
                if category.lower() not in [ft.lower() for ft in function_types]:
                    logger.warning(f"Function category '{category}' not found")
                    continue

                # Install all functions in category
                functions = sql_parser.list_functions(category)
                category_stats = {"category": category, "functions": 0, "errors": 0}

                for func_name in functions:
                    try:
                        sql = get_function_sql(category, func_name)
                        if _execute_sql(
                            connection,
                            sql,
                            f"Install {category}.{func_name} function",
                            dry_run,
                        ):
                            stats["functions_installed"] += 1
                            category_stats["functions"] += 1
                        else:
                            stats["errors"] += 1
                            category_stats["errors"] += 1
                    except Exception as e:
                        logger.error(
                            f"Failed to load function {category}.{func_name}: {e}"
                        )
                        stats["errors"] += 1
                        category_stats["errors"] += 1

                # Install by category file (for multi-function files)
                try:
                    category_functions = sql_parser.get_all_functions(category)
                    for sql in category_functions:
                        if _execute_sql(
                            connection, sql, f"Install {category} functions", dry_run
                        ):
                            stats["functions_installed"] += 1
                            category_stats["functions"] += 1
                        else:
                            stats["errors"] += 1
                            category_stats["errors"] += 1
                except Exception as e:
                    logger.debug(f"No category file for {category}: {e}")

                stats["categories"].append(category_stats)

            except Exception as e:
                logger.error(f"Failed to install {category} functions: {e}")
                stats["errors"] += 1

    logger.info(f"Functions installed: {stats['functions_installed']}")
    return stats


def install_tables(
    database_name: str = DEFAULT_DATABASE,
    table_names: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Install staging tables (CREATE + INGEST) using auto connection.

    Args:
        database_name: Target database name (default: 'dubai_real_estate')
        table_names: Specific tables to install (default: all in order)
        dry_run: If True, show what would be done without executing

    Returns:
        Dict with installation results and statistics

    Example:
        >>> from dubai_real_estate.install import install_tables
        >>> result = install_tables(table_names=["dld_transactions", "dld_units"])
        >>> print(f"Created {result['tables_created']} tables")
    """
    connection = _get_connection()

    if table_names is None:
        table_names = TABLE_INSTALL_ORDER

    logger.info(f"Installing staging tables in database: {database_name}")

    stats = {"tables_created": 0, "tables_ingested": 0, "errors": 0, "tables": []}

    with connection:
        # Create database first
        create_database_sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}`"
        if not _execute_sql(
            connection,
            create_database_sql,
            f"Create database '{database_name}'",
            dry_run,
        ):
            raise InstallationError(f"Failed to create database '{database_name}'")

        # Install tables
        for table_name in table_names:
            table_stats = {
                "table": table_name,
                "created": False,
                "ingested": False,
                "error": None,
            }

            try:
                logger.info(f"Installing staging table: {table_name}")

                # 1. Create table structure
                create_sql = get_table_sql(table_name, "CREATE")
                formatted_sql = create_sql.format(
                    dld_database=database_name, dld_table=table_name
                )

                if _execute_sql(
                    connection, formatted_sql, f"Create table {table_name}", dry_run
                ):
                    stats["tables_created"] += 1
                    table_stats["created"] = True
                else:
                    stats["errors"] += 1
                    table_stats["error"] = "Failed to create table"
                    continue

                # 2. Ingest data
                ingest_sql = get_table_sql(table_name, "INGEST")
                formatted_sql = ingest_sql.format(
                    dld_database=database_name, dld_table=table_name
                )

                # Retry multiple times as ingestion may be interrupted
                # by HTTP connection timeouts
                tentative = 0
                while tentative < MAX_RETRY:
                    result = _execute_sql(
                        connection,
                        formatted_sql,
                        f"Ingest data into {table_name}",
                        dry_run,
                    )
                    if result:
                        tentative = MAX_RETRY
                    else:
                        tentative += 1

                if result:
                    stats["tables_ingested"] += 1
                    table_stats["ingested"] = True
                else:
                    stats["errors"] += 1
                    table_stats["error"] = "Failed to ingest data"

            except Exception as e:
                logger.error(f"Failed to install table {table_name}: {e}")
                stats["errors"] += 1
                table_stats["error"] = str(e)

            stats["tables"].append(table_stats)

    logger.info(f"Staging tables created: {stats['tables_created']}")
    logger.info(f"Staging tables ingested: {stats['tables_ingested']}")
    return stats


def install_views(
    database_name: str = DEFAULT_DATABASE,
    view_type: str = "both",
    table_names: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Install clean and/or production views using auto connection.

    Args:
        database_name: Target database name (default: 'dubai_real_estate')
        view_type: Type of views to create ("clean", "prod", or "both")
        table_names: Specific tables to create views for (default: all)
        dry_run: If True, show what would be done without executing

    Returns:
        Dict with installation results and statistics

    Example:
        >>> from dubai_real_estate.install import install_views
        >>> result = install_views(view_type="clean")
        >>> print(f"Created {result['clean_views_created']} clean views")
    """
    connection = _get_connection()

    if table_names is None:
        table_names = TABLE_INSTALL_ORDER

    if view_type not in ("clean", "prod", "both"):
        raise ValueError("view_type must be 'clean', 'prod', or 'both'")

    logger.info(f"Installing {view_type} views in database: {database_name}")

    sql_parser = SQLParser()
    stats = {
        "clean_views_created": 0,
        "prod_views_created": 0,
        "errors": 0,
        "views": [],
    }

    with connection:
        for table_name in table_names:
            view_stats = {
                "table": table_name,
                "clean_created": False,
                "prod_created": False,
                "errors": [],
            }

            # Create clean view
            if view_type in ("clean", "both"):
                try:
                    options = sql_parser.list_table_options(table_name)
                    if "clean_view" in [opt.lower() for opt in options]:
                        clean_sql = get_table_sql(table_name, "CLEAN_VIEW")
                        formatted_sql = clean_sql.format(
                            dld_database=database_name,
                            dld_table=table_name,
                            **TABLE_VARIABLES,
                        )

                        if _execute_sql(
                            connection,
                            formatted_sql,
                            f"Create clean view for {table_name}",
                            dry_run,
                        ):
                            stats["clean_views_created"] += 1
                            view_stats["clean_created"] = True
                        else:
                            stats["errors"] += 1
                            view_stats["errors"].append("Failed to create clean view")
                    else:
                        logger.debug(f"No clean view SQL for {table_name}")

                except Exception as e:
                    logger.error(f"Failed to create clean view for {table_name}: {e}")
                    stats["errors"] += 1
                    view_stats["errors"].append(f"Clean view error: {e}")

            # Create production view
            if view_type in ("prod", "both"):
                try:
                    options = sql_parser.list_table_options(table_name)
                    if "prod_view" in [opt.lower() for opt in options]:
                        prod_sql = get_table_sql(table_name, "PROD_VIEW")
                        formatted_sql = prod_sql.format(
                            dld_database=database_name, dld_table=table_name
                        )

                        if _execute_sql(
                            connection,
                            formatted_sql,
                            f"Create prod view for {table_name}",
                            dry_run,
                        ):
                            stats["prod_views_created"] += 1
                            view_stats["prod_created"] = True
                        else:
                            stats["errors"] += 1
                            view_stats["errors"].append("Failed to create prod view")
                    else:
                        logger.debug(f"No prod view SQL for {table_name}")

                except Exception as e:
                    logger.error(f"Failed to create prod view for {table_name}: {e}")
                    stats["errors"] += 1
                    view_stats["errors"].append(f"Prod view error: {e}")

            stats["views"].append(view_stats)

    logger.info(f"Clean views created: {stats['clean_views_created']}")
    logger.info(f"Production views created: {stats['prod_views_created']}")
    return stats


def install_prod_tables(
    database_name: str = DEFAULT_DATABASE,
    table_names: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Install production tables (CREATE_PROD + INGEST_PROD) using auto connection.

    Args:
        database_name: Target database name (default: 'dubai_real_estate')
        table_names: Specific tables to install (default: all in order)
        dry_run: If True, show what would be done without executing

    Returns:
        Dict with installation results and statistics

    Example:
        >>> from dubai_real_estate.install import install_prod_tables
        >>> result = install_prod_tables(table_names=["dld_transactions", "dld_units"])
        >>> print(f"Created {result['prod_tables_created']} production tables")
    """
    connection = _get_connection()

    if table_names is None:
        table_names = TABLE_INSTALL_ORDER

    logger.info(f"Installing production tables in database: {database_name}")

    sql_parser = SQLParser()
    stats = {
        "prod_tables_created": 0,
        "prod_tables_ingested": 0,
        "errors": 0,
        "tables": [],
    }

    with connection:
        # Install production tables
        for table_name in table_names:
            table_stats = {
                "table": table_name,
                "created": False,
                "ingested": False,
                "error": None,
            }

            try:
                # Check if CREATE_PROD exists
                options = sql_parser.list_table_options(table_name)
                if "create_prod" not in [opt.lower() for opt in options]:
                    logger.debug(f"No CREATE_PROD SQL for {table_name}")
                    continue

                logger.info(f"Installing production table: {table_name}")

                # 1. Create production table structure
                create_sql = get_table_sql(table_name, "CREATE_PROD")
                formatted_sql = create_sql.format(
                    dld_database=database_name, dld_table=table_name
                )

                if _execute_sql(
                    connection,
                    formatted_sql,
                    f"Create production table {table_name}",
                    dry_run,
                ):
                    stats["prod_tables_created"] += 1
                    table_stats["created"] = True
                else:
                    stats["errors"] += 1
                    table_stats["error"] = "Failed to create production table"
                    continue

                # 2. Ingest data into production table
                # Check if INGEST_PROD exists
                if "ingest_prod" in [opt.lower() for opt in options]:
                    ingest_sql = get_table_sql(table_name, "INGEST_PROD")
                    formatted_sql = ingest_sql.format(
                        dld_database=database_name, dld_table=table_name
                    )

                    if _execute_sql(
                        connection,
                        formatted_sql,
                        f"Ingest data into production table {table_name}",
                        dry_run,
                    ):
                        stats["prod_tables_ingested"] += 1
                        table_stats["ingested"] = True
                    else:
                        stats["errors"] += 1
                        table_stats["error"] = (
                            "Failed to ingest data into production table"
                        )
                else:
                    logger.debug(f"No INGEST_PROD SQL for {table_name}")

            except Exception as e:
                logger.error(f"Failed to install production table {table_name}: {e}")
                stats["errors"] += 1
                table_stats["error"] = str(e)

            stats["tables"].append(table_stats)

    logger.info(f"Production tables created: {stats['prod_tables_created']}")
    logger.info(f"Production tables ingested: {stats['prod_tables_ingested']}")
    return stats


def drop_staging_and_views(
    database_name: str = DEFAULT_DATABASE,
    table_names: Optional[List[str]] = None,
    drop_staging: bool = True,
    drop_views: bool = True,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Drop staging tables and views to clean up after production deployment.

    Args:
        database_name: Target database name (default: 'dubai_real_estate')
        table_names: Specific tables to clean up (default: all)
        drop_staging: Whether to drop staging tables (default: True)
        drop_views: Whether to drop views (default: True)
        dry_run: If True, show what would be done without executing

    Returns:
        Dict with cleanup results and statistics

    Example:
        >>> from dubai_real_estate.install import drop_staging_and_views
        >>> # Drop everything except production tables
        >>> result = drop_staging_and_views()
        >>> print(f"Dropped {result['staging_dropped']} staging tables")
        >>>
        >>> # Drop only views, keep staging for debugging
        >>> result = drop_staging_and_views(drop_staging=False, drop_views=True)
    """
    connection = _get_connection()

    if table_names is None:
        table_names = TABLE_INSTALL_ORDER

    logger.info(f"Cleaning up database: {database_name}")
    if drop_staging:
        logger.info("Will drop staging tables")
    if drop_views:
        logger.info("Will drop views")

    stats = {
        "staging_dropped": 0,
        "clean_views_dropped": 0,
        "prod_views_dropped": 0,
        "errors": 0,
        "tables": [],
    }

    with connection:
        for table_name in table_names:
            table_stats = {
                "table": table_name,
                "staging_dropped": False,
                "clean_view_dropped": False,
                "prod_view_dropped": False,
                "errors": [],
            }

            # Drop clean view
            if drop_views:
                try:
                    drop_sql = f"DROP VIEW IF EXISTS `{database_name}`.`{table_name}_staging_clean`"
                    if _execute_sql(
                        connection,
                        drop_sql,
                        f"Drop clean view {table_name}_staging_clean",
                        dry_run,
                    ):
                        stats["clean_views_dropped"] += 1
                        table_stats["clean_view_dropped"] = True
                    else:
                        stats["errors"] += 1
                        table_stats["errors"].append("Failed to drop clean view")
                except Exception as e:
                    logger.error(f"Failed to drop clean view for {table_name}: {e}")
                    stats["errors"] += 1
                    table_stats["errors"].append(f"Clean view drop error: {e}")

            # Drop prod view
            if drop_views:
                try:
                    drop_sql = (
                        f"DROP VIEW IF EXISTS `{database_name}`.`{table_name}_view`"
                    )
                    if _execute_sql(
                        connection,
                        drop_sql,
                        f"Drop prod view {table_name}_view",
                        dry_run,
                    ):
                        stats["prod_views_dropped"] += 1
                        table_stats["prod_view_dropped"] = True
                    else:
                        stats["errors"] += 1
                        table_stats["errors"].append("Failed to drop prod view")
                except Exception as e:
                    logger.error(f"Failed to drop prod view for {table_name}: {e}")
                    stats["errors"] += 1
                    table_stats["errors"].append(f"Prod view drop error: {e}")

            # Drop staging table
            if drop_staging:
                try:
                    drop_sql = (
                        f"DROP TABLE IF EXISTS `{database_name}`.`{table_name}_staging`"
                    )
                    if _execute_sql(
                        connection,
                        drop_sql,
                        f"Drop staging table {table_name}_staging",
                        dry_run,
                    ):
                        stats["staging_dropped"] += 1
                        table_stats["staging_dropped"] = True
                    else:
                        stats["errors"] += 1
                        table_stats["errors"].append("Failed to drop staging table")
                except Exception as e:
                    logger.error(f"Failed to drop staging table for {table_name}: {e}")
                    stats["errors"] += 1
                    table_stats["errors"].append(f"Staging table drop error: {e}")

            stats["tables"].append(table_stats)

    logger.info(f"Staging tables dropped: {stats['staging_dropped']}")
    logger.info(f"Clean views dropped: {stats['clean_views_dropped']}")
    logger.info(f"Production views dropped: {stats['prod_views_dropped']}")
    return stats


def install_database(
    database_name: str = DEFAULT_DATABASE,
    include_functions: bool = True,
    include_tables: bool = True,
    include_views: bool = True,
    include_prod_tables: bool = True,
    cleanup_after_prod: bool = True,
    table_names: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Complete database installation using auto connection.

    Args:
        database_name: Target database name (default: 'dubai_real_estate')
        include_functions: Whether to install SQL functions
        include_tables: Whether to create and ingest staging tables
        include_views: Whether to create clean and production views
        include_prod_tables: Whether to create final production tables
        cleanup_after_prod: Whether to drop staging/views after creating prod tables
        table_names: Specific tables to install (default: all)
        dry_run: If True, show what would be done without executing

    Returns:
        Dict with complete installation results and statistics

    Example:
        >>> from dubai_real_estate.install import install_database
        >>>
        >>> # Complete staging installation
        >>> result = install_database()
        >>>
        >>> # Full production deployment with cleanup
        >>> result = install_database(
        ...     include_prod_tables=True,
        ...     cleanup_after_prod=True
        ... )
        >>>
        >>> # Development setup (no prod tables)
        >>> result = install_database(
        ...     "dld_dev",
        ...     include_views=False,
        ...     table_names=["dld_transactions", "dld_units"]
        ... )
    """
    connection = _get_connection()

    logger.info(f"Starting Dubai Real Estate database installation")
    logger.info(f"Database: {database_name}")
    logger.info(f"Connection: {connection.credentials.name}")
    logger.info(f"Dry run: {dry_run}")
    logger.info("-" * 60)

    start_time = time.time()
    overall_stats = {
        "database_name": database_name,
        "connection_name": connection.credentials.name,
        "dry_run": dry_run,
        "start_time": start_time,
        "end_time": None,
        "duration": None,
        "success": False,
        "database_created": False,
        "total_errors": 0,
        "functions": None,
        "tables": None,
        "views": None,
        "prod_tables": None,
        "cleanup": None,
        "validation": None,
    }

    try:
        # Create database first
        logger.info("Phase 0: Creating database...")
        database_created = create_database(database_name, dry_run=dry_run)
        if not database_created:
            raise InstallationError(f"Failed to create database '{database_name}'")
        overall_stats["database_created"] = True

        # Install functions
        if include_functions:
            logger.info("Phase 1: Installing SQL functions...")
            func_result = install_functions(dry_run=dry_run)
            overall_stats["functions"] = func_result
            overall_stats["total_errors"] += func_result["errors"]

        # Install tables
        if include_tables:
            logger.info("Phase 2: Installing staging tables...")
            table_result = install_tables(database_name, table_names, dry_run=dry_run)
            overall_stats["tables"] = table_result
            overall_stats["total_errors"] += table_result["errors"]

        # Install views
        if include_views:
            logger.info("Phase 3: Installing views...")
            view_result = install_views(
                database_name, "both", table_names, dry_run=dry_run
            )
            overall_stats["views"] = view_result
            overall_stats["total_errors"] += view_result["errors"]

        # Install production tables
        if include_prod_tables:
            logger.info("Phase 4: Installing production tables...")
            prod_result = install_prod_tables(
                database_name, table_names, dry_run=dry_run
            )
            overall_stats["prod_tables"] = prod_result
            overall_stats["total_errors"] += prod_result["errors"]

        # Cleanup staging and views after production tables
        if cleanup_after_prod and include_prod_tables:
            logger.info("Phase 5: Cleaning up staging tables and views...")
            cleanup_result = drop_staging_and_views(
                database_name,
                table_names,
                drop_staging=True,
                drop_views=True,
                dry_run=dry_run,
            )
            overall_stats["cleanup"] = cleanup_result
            overall_stats["total_errors"] += cleanup_result["errors"]

        # Validate installation (smart validation based on what should exist)
        if not dry_run and (include_tables or include_prod_tables):
            phase_num = (
                6
                if (include_prod_tables and cleanup_after_prod)
                else 5 if include_prod_tables else 4
            )
            logger.info(f"Phase {phase_num}: Validating installation...")

            # Determine what to validate based on what was installed and cleaned up
            check_staging = include_tables and not (
                cleanup_after_prod and include_prod_tables
            )
            check_prod = include_prod_tables

            validation_result = validate_installation(
                database_name,
                table_names,
                check_staging=check_staging,
                check_prod=check_prod,
            )
            overall_stats["validation"] = validation_result

        overall_stats["success"] = overall_stats["total_errors"] == 0

    except Exception as e:
        logger.error(f"Installation failed: {e}")
        overall_stats["error"] = str(e)
        overall_stats["success"] = False

    finally:
        overall_stats["end_time"] = time.time()
        overall_stats["duration"] = overall_stats["end_time"] - start_time

        _print_installation_summary(overall_stats)

    return overall_stats


def validate_installation(
    database_name: str = DEFAULT_DATABASE,
    table_names: Optional[List[str]] = None,
    check_staging: bool = True,
    check_prod: bool = True,
) -> Dict[str, Any]:
    """Validate installation by checking table counts using auto connection.

    Args:
        database_name: Database to validate (default: 'dubai_real_estate')
        table_names: Tables to check (default: all)
        check_staging: Whether to check staging tables (default: True)
        check_prod: Whether to check production tables (default: True)

    Returns:
        Dict with validation results

    Example:
        >>> from dubai_real_estate.install import validate_installation
        >>> result = validate_installation()  # Uses default database
        >>> for table in result['tables']:
        ...     print(f"{table['name']}: {table['staging_count']:,} rows")
    """
    connection = _get_connection()

    if table_names is None:
        table_names = TABLE_INSTALL_ORDER

    logger.info("Validating installation...")

    validation_result = {
        "database_name": database_name,
        "tables_checked": 0,
        "tables_with_data": 0,
        "tables_empty": 0,
        "total_staging_rows": 0,
        "total_prod_rows": 0,
        "tables": [],
    }

    with connection:
        for table_name in table_names:
            table_result = {
                "name": table_name,
                "staging_count": None,
                "staging_exists": False,
                "clean_count": None,
                "prod_count": None,
                "prod_table_count": None,
                "prod_table_exists": False,
                "has_data": False,
                "validation_errors": [],
            }

            # Check staging table if requested
            if check_staging:
                try:
                    # First check if staging table exists
                    cursor = connection.execute(
                        f"EXISTS TABLE `{database_name}`.`{table_name}_staging`"
                    )
                    staging_exists = bool(cursor.fetchone()[0])
                    cursor.close()
                    table_result["staging_exists"] = staging_exists

                    if staging_exists:
                        cursor = connection.execute(
                            f"SELECT COUNT(*) FROM `{database_name}`.`{table_name}_staging`"
                        )
                        staging_count = cursor.fetchone()[0]
                        cursor.close()

                        table_result["staging_count"] = staging_count
                        table_result["has_data"] = staging_count > 0
                        validation_result["total_staging_rows"] += staging_count

                        if staging_count > 0:
                            validation_result["tables_with_data"] += 1
                            logger.info(
                                f"✓ {table_name}_staging: {staging_count:,} rows"
                            )
                        else:
                            validation_result["tables_empty"] += 1
                            logger.warning(f"⚠ {table_name}_staging: No data")
                    else:
                        logger.debug(f"- {table_name}_staging: Does not exist")

                except Exception as e:
                    error_msg = f"Failed to validate {table_name}_staging: {e}"
                    logger.error(error_msg)
                    table_result["validation_errors"].append(error_msg)

            # Check production table if requested
            if check_prod:
                try:
                    # First check if prod table exists
                    cursor = connection.execute(
                        f"EXISTS TABLE `{database_name}`.`{table_name}`"
                    )
                    prod_table_exists = bool(cursor.fetchone()[0])
                    cursor.close()
                    table_result["prod_table_exists"] = prod_table_exists

                    if prod_table_exists:
                        cursor = connection.execute(
                            f"SELECT COUNT(*) FROM `{database_name}`.`{table_name}`"
                        )
                        prod_table_count = cursor.fetchone()[0]
                        cursor.close()
                        table_result["prod_table_count"] = prod_table_count
                        validation_result["total_prod_rows"] += prod_table_count

                        # If no staging data but prod data exists, mark as having data
                        if not table_result["has_data"] and prod_table_count > 0:
                            table_result["has_data"] = True
                            validation_result["tables_with_data"] += 1
                            if (
                                table_result["staging_count"] is None
                            ):  # No staging checked
                                validation_result["tables_empty"] = max(
                                    0, validation_result["tables_empty"]
                                )

                        logger.info(f"✓ {table_name} (prod): {prod_table_count:,} rows")
                    else:
                        logger.debug(f"- {table_name} (prod): Does not exist")

                except Exception as e:
                    error_msg = f"Failed to validate {table_name} (prod): {e}"
                    logger.error(error_msg)
                    table_result["validation_errors"].append(error_msg)

            # Check clean view if exists (optional)
            try:
                cursor = connection.execute(
                    f"EXISTS TABLE `{database_name}`.`{table_name}_staging_clean`"
                )
                clean_view_exists = bool(cursor.fetchone()[0])
                cursor.close()

                if clean_view_exists:
                    cursor = connection.execute(
                        f"SELECT COUNT(*) FROM `{database_name}`.`{table_name}_staging_clean`"
                    )
                    clean_count = cursor.fetchone()[0]
                    cursor.close()
                    table_result["clean_count"] = clean_count
            except:
                pass  # View doesn't exist or error - not critical

            # Check prod view if exists (optional)
            try:
                cursor = connection.execute(
                    f"EXISTS TABLE `{database_name}`.`{table_name}_view`"
                )
                prod_view_exists = bool(cursor.fetchone()[0])
                cursor.close()

                if prod_view_exists:
                    cursor = connection.execute(
                        f"SELECT COUNT(*) FROM `{database_name}`.`{table_name}_view`"
                    )
                    prod_count = cursor.fetchone()[0]
                    cursor.close()
                    table_result["prod_count"] = prod_count
            except:
                pass  # View doesn't exist or error - not critical

            validation_result["tables"].append(table_result)
            validation_result["tables_checked"] += 1

    # Summary logging
    if check_staging and check_prod:
        logger.info(
            f"Validation complete: {validation_result['tables_with_data']}/{validation_result['tables_checked']} tables have data"
        )
        logger.info(f"Total staging rows: {validation_result['total_staging_rows']:,}")
        logger.info(f"Total production rows: {validation_result['total_prod_rows']:,}")
    elif check_staging:
        logger.info(
            f"Staging validation complete: {validation_result['tables_with_data']}/{validation_result['tables_checked']} tables have data"
        )
        logger.info(f"Total staging rows: {validation_result['total_staging_rows']:,}")
    elif check_prod:
        logger.info(
            f"Production validation complete: {validation_result['tables_with_data']}/{validation_result['tables_checked']} tables have data"
        )
        logger.info(f"Total production rows: {validation_result['total_prod_rows']:,}")

    return validation_result


def get_installation_status(database_name: str = DEFAULT_DATABASE) -> Dict[str, Any]:
    """Get current installation status using auto connection.

    Args:
        database_name: Database to check (default: 'dubai_real_estate')

    Returns:
        Dict with current installation status

    Example:
        >>> from dubai_real_estate.install import get_installation_status
        >>> status = get_installation_status()  # Uses default database
        >>> print(f"Database exists: {status['database_exists']}")
        >>> print(f"Tables installed: {status['tables_installed']}/{status['tables_expected']}")
    """
    connection = _get_connection()

    status = {
        "database_name": database_name,
        "connection_name": connection.credentials.name,
        "database_exists": False,
        "tables_expected": len(TABLE_INSTALL_ORDER),
        "tables_installed": 0,
        "prod_tables_installed": 0,
        "functions_available": {},
        "tables": {},
    }

    with connection:
        # Check if database exists
        try:
            cursor = connection.execute(f"EXISTS DATABASE `{database_name}`")
            status["database_exists"] = bool(cursor.fetchone()[0])
            cursor.close()
        except:
            status["database_exists"] = False

        if not status["database_exists"]:
            return status

        # Check tables
        for table_name in TABLE_INSTALL_ORDER:
            table_status = {
                "staging_exists": False,
                "clean_view_exists": False,
                "prod_view_exists": False,
                "prod_table_exists": False,
                "row_count": 0,
                "prod_table_count": 0,
            }

            # Check staging table
            try:
                cursor = connection.execute(
                    f"EXISTS TABLE `{database_name}`.`{table_name}_staging`"
                )
                table_status["staging_exists"] = bool(cursor.fetchone()[0])
                cursor.close()

                if table_status["staging_exists"]:
                    status["tables_installed"] += 1

                    # Get row count
                    cursor = connection.execute(
                        f"SELECT COUNT(*) FROM `{database_name}`.`{table_name}_staging`"
                    )
                    table_status["row_count"] = cursor.fetchone()[0]
                    cursor.close()
            except:
                pass

            # Check clean view
            try:
                cursor = connection.execute(
                    f"EXISTS TABLE `{database_name}`.`{table_name}_staging_clean`"
                )
                table_status["clean_view_exists"] = bool(cursor.fetchone()[0])
                cursor.close()
            except:
                pass

            # Check prod view
            try:
                cursor = connection.execute(
                    f"EXISTS TABLE `{database_name}`.`{table_name}_view`"
                )
                table_status["prod_view_exists"] = bool(cursor.fetchone()[0])
                cursor.close()
            except:
                pass

            # Check prod table
            try:
                cursor = connection.execute(
                    f"EXISTS TABLE `{database_name}`.`{table_name}`"
                )
                table_status["prod_table_exists"] = bool(cursor.fetchone()[0])
                cursor.close()

                if table_status["prod_table_exists"]:
                    status["prod_tables_installed"] += 1

                    # Get prod table row count
                    cursor = connection.execute(
                        f"SELECT COUNT(*) FROM `{database_name}`.`{table_name}`"
                    )
                    table_status["prod_table_count"] = cursor.fetchone()[0]
                    cursor.close()
            except:
                pass

            status["tables"][table_name] = table_status

        # Check functions (sample a few key ones)
        test_functions = ["FORMAT_DATE", "MAP_AREA_NAME_EN", "IS_EN", "NULLIFNEG"]

        for func_name in test_functions:
            try:
                cursor = connection.execute(f"SELECT {func_name}('test')")
                cursor.close()
                status["functions_available"][func_name] = True
            except:
                status["functions_available"][func_name] = False

    return status


def _print_installation_summary(stats: Dict[str, Any]):
    """Print installation summary."""
    logger.info("-" * 60)
    logger.info("INSTALLATION SUMMARY")
    logger.info("-" * 60)
    logger.info(f"Database: {stats['database_name']}")
    logger.info(f"Connection: {stats['connection_name']}")
    if stats.get("database_created"):
        logger.info("✓ Database created successfully")
    logger.info(f"Duration: {stats.get('duration', 0):.1f} seconds")

    if stats.get("functions"):
        logger.info(f"Functions installed: {stats['functions']['functions_installed']}")

    if stats.get("tables"):
        logger.info(f"Staging tables created: {stats['tables']['tables_created']}")
        logger.info(f"Staging tables ingested: {stats['tables']['tables_ingested']}")

    if stats.get("views"):
        logger.info(f"Clean views created: {stats['views']['clean_views_created']}")
        logger.info(f"Production views created: {stats['views']['prod_views_created']}")

    if stats.get("prod_tables"):
        logger.info(
            f"Production tables created: {stats['prod_tables']['prod_tables_created']}"
        )
        logger.info(
            f"Production tables ingested: {stats['prod_tables']['prod_tables_ingested']}"
        )

    if stats.get("cleanup"):
        logger.info(f"Staging tables dropped: {stats['cleanup']['staging_dropped']}")
        logger.info(
            f"Views dropped: {stats['cleanup']['clean_views_dropped'] + stats['cleanup']['prod_views_dropped']}"
        )

    if stats.get("validation"):
        val = stats["validation"]
        logger.info(f"Tables validated: {val['tables_checked']}")
        logger.info(f"Tables with data: {val['tables_with_data']}")
        if val["total_staging_rows"] > 0:
            logger.info(f"Total staging rows: {val['total_staging_rows']:,}")
        if val["total_prod_rows"] > 0:
            logger.info(f"Total production rows: {val['total_prod_rows']:,}")

    logger.info(f"Total errors: {stats['total_errors']}")

    if stats["success"]:
        logger.info("✓ Installation completed successfully!")
    else:
        logger.warning(f"⚠ Installation completed with {stats['total_errors']} errors")

    logger.info("-" * 60)


# Convenience exports
__all__ = [
    "DEFAULT_DATABASE",
    "create_database",
    "install_database",
    "install_functions",
    "install_tables",
    "install_views",
    "install_prod_tables",
    "drop_staging_and_views",
    "validate_installation",
    "get_installation_status",
    "TABLE_INSTALL_ORDER",
    "FUNCTION_CATEGORIES",
    "InstallationError",
]
