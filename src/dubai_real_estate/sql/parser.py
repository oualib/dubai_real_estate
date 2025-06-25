"""
dubai_real_estate SQL Parser Module

Simple parser for SQL files organized by tables and functions.
Handles automatic prefix addition and file type routing.
"""

from pathlib import Path
from typing import List, Optional, Union
import os


class SQLParser:
    """Parser for SQL files organized in tables and functions folders."""

    def __init__(self, sql_root: Optional[Union[str, Path]] = None):
        """Initialize parser with SQL root directory.

        Args:
            sql_root: Optional path to the root SQL directory. If None, uses module_path/sql_files/
        """
        if sql_root is None:
            # Find the dubai_real_estate package root and append sql_files
            current_dir = Path(__file__).parent
            # Go up until we find the dubai_real_estate root (contains __init__.py and connection/)
            while (
                current_dir.name != "dubai_real_estate"
                and current_dir.parent != current_dir
            ):
                current_dir = current_dir.parent

            if current_dir.name == "dubai_real_estate":
                self.sql_root = current_dir / "sql_files"
            else:
                raise FileNotFoundError(
                    "Could not find dubai_real_estate package root directory"
                )
        else:
            self.sql_root = Path(sql_root)

        self.tables_path = self.sql_root / "tables"
        self.functions_path = self.sql_root / "functions"

        # Validate paths exist
        if not self.sql_root.exists():
            raise FileNotFoundError(f"SQL root directory not found: {self.sql_root}")
        if not self.tables_path.exists():
            raise FileNotFoundError(f"Tables directory not found: {self.tables_path}")
        if not self.functions_path.exists():
            raise FileNotFoundError(
                f"Functions directory not found: {self.functions_path}"
            )

    def get_table(self, table_name: str, option: str) -> str:
        """Get SQL content for a specific table and option.

        Args:
            table_name: Name of the table (prefix 'dld_' added automatically if missing)
            option: SQL file type (CREATE, INGEST, CLEAN, etc.)

        Returns:
            SQL file content as string

        Raises:
            FileNotFoundError: If table folder or SQL file doesn't exist

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> sql = parser.get_table("users", "CREATE")
            >>> sql = parser.get_table("dld_orders", "INGEST")  # prefix already present
        """
        # Add prefix if not present
        if not table_name.startswith("dld_"):
            table_name = f"dld_{table_name}"

        table_folder = self.tables_path / table_name
        if not table_folder.exists():
            raise FileNotFoundError(f"Table folder not found: {table_folder}")

        sql_file = table_folder / f"{option.lower()}.sql"
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL file not found: {sql_file}")

        return sql_file.read_text(encoding="utf-8")

    def get_function(self, function_type: str, function_name: str) -> str:
        """Get SQL content for a specific function.

        Args:
            function_type: Type of function (MAP, MATH, LANG, FORMAT, etc.)
            function_name: Name of the function file (without .sql extension)

        Returns:
            SQL file content as string

        Raises:
            FileNotFoundError: If function file doesn't exist

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> sql = parser.get_function("MATH", "calculate_total")
            >>> sql = parser.get_function("FORMAT", "format_date")
        """
        function_file = (
            self.functions_path / function_type.lower() / f"{function_name}.sql"
        )
        if not function_file.exists():
            raise FileNotFoundError(f"Function file not found: {function_file}")

        return function_file.read_text(encoding="utf-8")

    def list_tables(self) -> List[str]:
        """List all available table names.

        Returns:
            List of table folder names

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> tables = parser.list_tables()
            >>> print(tables)  # ['dld_users', 'dld_orders', 'dld_products']
        """
        return [folder.name for folder in self.tables_path.iterdir() if folder.is_dir()]

    def list_table_options(self, table_name: str) -> List[str]:
        """List all available SQL files for a specific table.

        Args:
            table_name: Name of the table (prefix added automatically)

        Returns:
            List of available SQL file names (without .sql extension)

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> options = parser.list_table_options("users")
            >>> print(options)  # ['create', 'ingest', 'clean']
        """
        # Add prefix if not present
        if not table_name.startswith("dld_"):
            table_name = f"dld_{table_name}"

        table_folder = self.tables_path / table_name
        if not table_folder.exists():
            raise FileNotFoundError(f"Table folder not found: {table_folder}")

        return [f.stem for f in table_folder.glob("*.sql")]

    def list_functions(self, function_type: Optional[str] = None) -> List[str]:
        """List all available functions.

        Args:
            function_type: Optional filter by function type (MAP, MATH, etc.)

        Returns:
            List of function file names (without .sql extension)

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> all_functions = parser.list_functions()
            >>> math_functions = parser.list_functions("MATH")
        """
        if function_type:
            function_folder = self.functions_path / function_type.lower()
            if not function_folder.exists():
                return []
            return [f.stem for f in function_folder.glob("*.sql")]
        else:
            # List all functions from all types
            functions = []
            for type_folder in self.functions_path.iterdir():
                if type_folder.is_dir():
                    functions.extend([f.stem for f in type_folder.glob("*.sql")])
            return functions

    def list_function_types(self) -> List[str]:
        """List all available function types.

        Returns:
            List of function type folder names

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> types = parser.list_function_types()
            >>> print(types)  # ['MAP', 'MATH', 'LANG', 'FORMAT']
        """
        return [
            folder.name for folder in self.functions_path.iterdir() if folder.is_dir()
        ]

    def get_all_table_files(self, table_name: str) -> List[str]:
        """Get all SQL files content for a specific table.

        Args:
            table_name: Name of the table (prefix added automatically)

        Returns:
            List of SQL file contents as strings

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> all_sql = parser.get_all_table_files("users")
            >>> for sql in all_sql:
            ...     print(f"--- SQL File ---\\n{sql}")
        """
        # Add prefix if not present
        if not table_name.startswith("dld_"):
            table_name = f"dld_{table_name}"

        table_folder = self.tables_path / table_name
        if not table_folder.exists():
            raise FileNotFoundError(f"Table folder not found: {table_folder}")

        sql_files = []
        for sql_file in table_folder.glob("*.sql"):
            sql_files.append(sql_file.read_text(encoding="utf-8"))

        return sql_files

    def get_all_functions(self, function_type: str) -> List[str]:
        """Get all SQL functions content for a specific type.

        Args:
            function_type: Type of functions (MAP, MATH, LANG, FORMAT, etc.)

        Returns:
            List of SQL function contents as strings

        Example:
            >>> parser = SQLParser("/path/to/sql")
            >>> math_functions = parser.get_all_functions("MATH")
            >>> for func in math_functions:
            ...     print(f"--- Function ---\\n{func}")
        """
        function_folder = self.functions_path / function_type.lower()
        if not function_folder.exists():
            raise FileNotFoundError(
                f"Function type folder not found: {function_folder}"
            )

        functions = []
        for sql_file in function_folder.glob("*.sql"):
            functions.append(sql_file.read_text(encoding="utf-8"))

        return functions


# Convenience functions for quick usage
def create_parser(sql_root: Optional[Union[str, Path]] = None) -> SQLParser:
    """Create a new SQL parser instance.

    Args:
        sql_root: Optional path to SQL root directory. If None, uses module_path/sql_files/

    Returns:
        SQLParser instance
    """
    return SQLParser(sql_root)


def get_table_sql(
    table_name: str, option: str, sql_root: Optional[Union[str, Path]] = None
) -> str:
    """Quick function to get table SQL.

    Args:
        table_name: Table name
        option: SQL option (CREATE, INGEST, etc.)
        sql_root: Optional path to SQL root directory. If None, uses module_path/sql_files/

    Returns:
        SQL content as string
    """
    parser = SQLParser(sql_root)
    return parser.get_table(table_name, option)


def get_function_sql(
    function_type: str, function_name: str, sql_root: Optional[Union[str, Path]] = None
) -> str:
    """Quick function to get function SQL.

    Args:
        function_type: Function type (MAP, MATH, etc.)
        function_name: Function name
        sql_root: Optional path to SQL root directory. If None, uses module_path/sql_files/

    Returns:
        SQL content as string
    """
    parser = SQLParser(sql_root)
    return parser.get_function(function_type, function_name)
