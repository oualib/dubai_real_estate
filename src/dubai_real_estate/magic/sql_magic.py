"""
ClickHouse SQL Magic Command for Jupyter Notebooks

Provides beautiful, feature-rich SQL magic commands for ClickHouse with:
- Multi-statement support (statements separated by ';')
- Pandas DataFrame integration
- Beautiful yellow/black themed output with ClickHouse branding
- Query performance metrics
- Connection management
- Result caching
- Export capabilities
- Error handling with syntax highlighting

Installation:
    %load_ext dubai_real_estate.sql

Usage:
    %sql SELECT * FROM table LIMIT 5
    %%sql
    SELECT count(*) as total FROM dld_transactions;
    SELECT avg(amount) as avg_amount FROM dld_transactions WHERE date > '2023-01-01';
"""

import re
import time
import warnings
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import pandas as pd
from IPython.core.magic import (
    Magics,
    line_magic,
    cell_magic,
    line_cell_magic,
    magics_class,
)
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import display, HTML, Markdown
from IPython.core.display import Javascript

try:
    from ..connection import get_connection, BaseConnection
except ImportError:
    # Fallback for direct import
    from dubai_real_estate.connection import get_connection, BaseConnection


@magics_class
class SQLMagic(Magics):
    """SQL Magic Commands for ClickHouse in Jupyter Notebooks."""

    def __init__(self, shell=None):
        super().__init__(shell)
        self.connection = None
        self.query_history = []
        self.result_cache = {}
        self.last_result = None
        self.isql_config = {
            "max_rows_display": 100,
            "show_execution_time": True,
            "show_row_count": True,
            "auto_limit": 1000,
            "minimal_mode": False,
            "cache_results": False,
            "export_format": "csv",
        }
        self._setup_styles()
        self._show_welcome_message()

    def _show_welcome_message(self):
        """Show welcome message when extension is loaded."""
        welcome_html = """
        <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin: 10px 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <svg style="width: 24px; height: 24px; margin-right: 10px;" viewBox="0 0 24 24" fill="none">
                    <path d="M21.333 10H24v4h-2.667ZM16 1.335h2.667v21.33H16Zm-5.333 0h2.666v21.33h-2.666ZM0 22.665V1.335h2.667v21.33zm5.333 -21.33H8v21.33H5.333Z" fill="#000000"/>
                </svg>
                <h3 style="margin: 0; color: #000; font-weight: 600;">Dubai Real Estate SQL Magic</h3>
            </div>
            <div style="color: #333; font-size: 14px; line-height: 1.5;">
                <strong>Available commands:</strong><br>
                🔌 <code>%sql_connect</code> - Manage ClickHouse Connections<br>
                📊 <code>%sql SELECT * FROM table LIMIT 5</code> - Execute SQL query<br>
                📝 <code>%%sql</code> - Execute multiple SQL queries (cell mode)<br>
                ⚙️ <code>%sql_config</code> - Configure settings<br>
                📋 <code>%sql_tables</code> - List available tables<br>
                📜 <code>%sql_history</code> - View query history<br><br>
                <strong>Available arguments:</strong> <code>max_rows_display</code>, <code>show_execution_time</code>, <code>show_row_count</code>, <code>auto_limit</code>, <code>minimal_mode</code>, <code>cache_results</code>, <code>export_format</code>
            </div>
        </div>
        """
        display(HTML(welcome_html))

    def _setup_styles(self):
        """Setup CSS styles for beautiful output."""
        css = """
        <style>
        .clickhouse-container {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 15px 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 1px solid #e2e8f0;
        }
        
        .clickhouse-header {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #000;
            padding: 12px 20px;
            font-weight: 600;
            display: flex;
            align-items: center;
            font-size: 14px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .clickhouse-logo {
            margin-right: 10px;
            width: 18px;
            height: 18px;
            flex-shrink: 0;
        }
        
        .clickhouse-minimal-header {
            background: #f8f9fa;
            border-left: 4px solid #FFD700;
            color: #333;
            padding: 10px 16px;
            font-weight: 500;
            font-size: 13px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .clickhouse-content {
            background: #fff;
        }
        
        .clickhouse-minimal-content {
            background: #fff;
            border-left: 4px solid #FFD700;
        }
        
        .clickhouse-stats {
            background: #2d3748;
            color: #FFD700;
            padding: 10px 20px;
            font-size: 12px;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid #e2e8f0;
        }
        
        .clickhouse-minimal-stats {
            background: #f8f9fa;
            color: #666;
            padding: 8px 16px;
            font-size: 11px;
            border-top: 1px solid #e2e8f0;
        }
        
        .clickhouse-error {
            background: #fff5f5;
            border: 1px solid #fed7d7;
            border-radius: 8px;
            padding: 16px;
            margin: 15px 0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        
        .clickhouse-error-header {
            color: #c53030;
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            font-size: 14px;
        }
        
        .clickhouse-error-message {
            color: #2d3748;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
            background: #f7fafc;
            padding: 12px;
            border-radius: 6px;
            border-left: 4px solid #c53030;
            line-height: 1.4;
        }
        
        .clickhouse-query {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 12px;
            margin: 10px 0;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
            color: #2d3748;
            overflow-x: auto;
            line-height: 1.4;
        }
        
        .clickhouse-results {
            padding: 0;
            overflow-x: auto;
            width: 100%;
        }
        
        .clickhouse-results table {
            width: 100% !important;
            border-collapse: collapse;
            font-size: 13px;
            margin: 0 !important;
            table-layout: auto !important;
            min-width: 100%;
        }
        
        .clickhouse-results th {
            background: #f8f9fa !important;
            color: #2d3748 !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
            text-align: left !important;
            border-bottom: 2px solid #e2e8f0 !important;
            border-right: 1px solid #e2e8f0 !important;
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap !important;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .clickhouse-results td {
            padding: 10px 16px !important;
            border-bottom: 1px solid #f1f5f9 !important;
            border-right: 1px solid #f1f5f9 !important;
            color: #4a5568 !important;
            vertical-align: top !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            max-width: 300px !important;
            min-width: 120px !important;
        }
        
        .clickhouse-results td.text-overflow {
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            max-width: 200px !important;
        }
        
        .clickhouse-results td.long-text {
            white-space: pre-wrap !important;
            word-break: break-word !important;
            max-width: 400px !important;
        }
        
        .clickhouse-results tr:nth-child(even) {
            background: #f8f9fa !important;
        }
        
        .clickhouse-results tr:hover {
            background: #e6fffa !important;
        }
        
        .clickhouse-results tbody tr:last-child td {
            border-bottom: none !important;
        }
        
        .clickhouse-results th:last-child,
        .clickhouse-results td:last-child {
            border-right: none !important;
        }
        
        .clickhouse-button {
            background: #FFD700;
            color: #000;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11px;
            cursor: pointer;
            margin-left: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .clickhouse-button:hover {
            background: #FFA500;
            transform: translateY(-1px);
        }
        
        .clickhouse-truncated {
            padding: 10px 20px;
            color: #666;
            font-size: 12px;
            background: #f8f9fa;
            border-top: 1px solid #e2e8f0;
            font-style: italic;
            text-align: center;
        }
        
        .clickhouse-success {
            padding: 16px 20px;
            color: #22543d;
            background: #f0fff4;
            border-left: 4px solid #38a169;
            font-weight: 500;
        }
        </style>
        """
        display(HTML(css))

    def _get_connection(self) -> BaseConnection:
        """Get ClickHouse connection."""
        if self.connection is None:
            self.connection = get_connection()
            if self.connection is None:
                raise RuntimeError(
                    "No ClickHouse connection available. Please create a connection first:\n"
                    "from dubai_real_estate.connection import create_connection\n"
                    "create_connection('my_conn', 'client', host='localhost', set_auto=True)"
                )
        return self.connection

    def _create_clickhouse_logo_svg(self) -> str:
        """Create ClickHouse logo SVG."""
        return """
        <svg class="clickhouse-logo" viewBox="0 0 24 24" fill="none">
            <path d="M21.333 10H24v4h-2.667ZM16 1.335h2.667v21.33H16Zm-5.333 0h2.666v21.33h-2.666ZM0 22.665V1.335h2.667v21.33zm5.333 -21.33H8v21.33H5.333Z" fill="#000000"/>
        </svg>
        """

    def _parse_sql_statements(self, sql: str) -> List[str]:
        """Parse SQL into individual statements, handling multi-statement queries."""
        # Remove comments
        sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
        sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)

        # Split by semicolon but be smart about it (avoid splitting inside strings)
        statements = []
        current_statement = ""
        in_string = False
        quote_char = None

        i = 0
        while i < len(sql):
            char = sql[i]

            if not in_string:
                if char in ('"', "'", "`"):
                    in_string = True
                    quote_char = char
                elif char == ";":
                    if current_statement.strip():
                        statements.append(current_statement.strip())
                    current_statement = ""
                    i += 1
                    continue
            else:
                if char == quote_char:
                    # Check if it's escaped
                    if i == 0 or sql[i - 1] != "\\":
                        in_string = False
                        quote_char = None

            current_statement += char
            i += 1

        # Add the last statement if it exists
        if current_statement.strip():
            statements.append(current_statement.strip())

        return [stmt for stmt in statements if stmt.strip()]

    def _execute_single_statement(
        self, sql: str, connection: BaseConnection
    ) -> Dict[str, Any]:
        """Execute a single SQL statement and return results."""
        start_time = time.time()

        try:
            with connection:
                cursor = connection.execute(sql)

                # Check if this is a statement that returns data
                sql_upper = sql.strip().upper()

                # Statements that return tabular data
                returns_data = (
                    sql_upper.startswith("SELECT")
                    or sql_upper.startswith("SHOW")
                    or sql_upper.startswith("DESCRIBE")
                    or sql_upper.startswith("DESC")
                    or sql_upper.startswith("EXPLAIN")
                    or "SELECT" in sql_upper
                )

                if returns_data:
                    # Fetch all results for data-returning statements
                    rows = cursor.fetchall()
                    columns = cursor.column_names()

                    # Create DataFrame
                    if rows and columns:
                        df = pd.DataFrame(rows, columns=columns)
                    else:
                        df = pd.DataFrame()

                    result = {
                        "type": "select",
                        "dataframe": df,
                        "row_count": len(rows),
                        "columns": columns,
                        "execution_time": time.time() - start_time,
                        "sql": sql,
                    }
                else:
                    # For non-data-returning statements (INSERT, UPDATE, DELETE, CREATE, etc.)
                    cursor.fetchall()  # Consume any results
                    result = {
                        "type": "command",
                        "dataframe": pd.DataFrame(),
                        "row_count": None,
                        "columns": [],
                        "execution_time": time.time() - start_time,
                        "sql": sql,
                        "message": f"Command executed successfully",
                    }

                cursor.close()
                return result

        except Exception as e:
            return {
                "type": "error",
                "error": str(e),
                "execution_time": time.time() - start_time,
                "sql": sql,
            }

    def _format_execution_time(self, seconds: float) -> str:
        """Format execution time in a human-readable way."""
        if seconds < 0.001:
            return f"{seconds*1000000:.0f}μs"
        elif seconds < 1:
            return f"{seconds*1000:.1f}ms"
        else:
            return f"{seconds:.2f}s"

    def _format_dataframe_for_display(self, df: pd.DataFrame) -> str:
        """Format DataFrame with proper text overflow handling."""
        if df.empty:
            return "<p>No data to display</p>"

        # Create custom HTML table with proper text handling
        html_parts = ["<table>"]

        # Header
        html_parts.append("<thead><tr>")
        for col in df.columns:
            html_parts.append(f"<th>{col}</th>")
        html_parts.append("</tr></thead>")

        # Body
        html_parts.append("<tbody>")
        for _, row in df.iterrows():
            html_parts.append("<tr>")
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    cell_content = "<em>NULL</em>"
                    cell_class = ""
                else:
                    value_str = str(value)
                    if len(value_str) > 100:
                        # Long text - use expandable format
                        short_text = value_str[:97] + "..."
                        cell_content = f'<span title="{value_str}">{short_text}</span>'
                        cell_class = 'class="long-text"'
                    elif len(value_str) > 50:
                        # Medium text - use ellipsis
                        cell_content = f'<span title="{value_str}">{value_str}</span>'
                        cell_class = 'class="text-overflow"'
                    else:
                        # Short text - display normally
                        cell_content = value_str
                        cell_class = ""

                html_parts.append(f"<td {cell_class}>{cell_content}</td>")
            html_parts.append("</tr>")
        html_parts.append("</tbody>")
        html_parts.append("</table>")

        return "".join(html_parts)

    def _display_result(
        self, result: Dict[str, Any], statement_num: int = 1, total_statements: int = 1
    ):
        """Display query result with beautiful formatting."""
        minimal_mode = self.isql_config.get("minimal_mode", False)

        if result["type"] == "error":
            self._display_error(result, statement_num, total_statements)
            return

        # Create container
        container_class = "clickhouse-container"
        header_class = (
            "clickhouse-minimal-header" if minimal_mode else "clickhouse-header"
        )
        content_class = (
            "clickhouse-minimal-content" if minimal_mode else "clickhouse-content"
        )
        stats_class = "clickhouse-minimal-stats" if minimal_mode else "clickhouse-stats"

        # Header
        if total_statements > 1:
            title = f"Query {statement_num}/{total_statements}"
        else:
            title = "ClickHouse Query Result"

        logo_html = "" if minimal_mode else self._create_clickhouse_logo_svg()

        html_parts = [f'<div class="{container_class}">']
        html_parts.append(f'<div class="{header_class}">{logo_html}{title}</div>')

        # Content
        html_parts.append(f'<div class="{content_class}">')

        if result["type"] == "select" and not result["dataframe"].empty:
            # Show SQL query if more than one statement
            if total_statements > 1:
                html_parts.append(
                    f'<div class="clickhouse-query">{result["sql"]}</div>'
                )

            # Display DataFrame
            df = result["dataframe"]
            max_rows = self.isql_config.get("max_rows_display", 100)

            if len(df) > max_rows:
                display_df = df.head(max_rows)
                truncated_msg = f'<div class="clickhouse-truncated">Showing first {max_rows} of {len(df)} rows</div>'
            else:
                display_df = df
                truncated_msg = ""

            # Use custom formatter for better display
            table_html = self._format_dataframe_for_display(display_df)

            html_parts.append('<div class="clickhouse-results">')
            html_parts.append(table_html)
            html_parts.append("</div>")
            html_parts.append(truncated_msg)

        elif result["type"] == "command":
            html_parts.append(f'<div class="clickhouse-success">')
            html_parts.append(f'<strong>✓ {result["message"]}</strong>')
            if total_statements > 1:
                html_parts.append(
                    f'<div class="clickhouse-query" style="margin-top: 8px;">{result["sql"]}</div>'
                )
            html_parts.append("</div>")

        # Stats footer
        if self.isql_config.get("show_execution_time", True) or self.isql_config.get(
            "show_row_count", True
        ):
            stats_parts = []

            if self.isql_config.get("show_execution_time", True):
                exec_time = self._format_execution_time(result["execution_time"])
                stats_parts.append(f"⚡ {exec_time}")

            if (
                self.isql_config.get("show_row_count", True)
                and result["row_count"] is not None
            ):
                if result["row_count"] == 1:
                    stats_parts.append(f"📊 {result['row_count']:,} row")
                else:
                    stats_parts.append(f"📊 {result['row_count']:,} rows")

            if result["type"] == "select" and not result["dataframe"].empty:
                # Add export button with unique ID
                export_id = f"export_{int(time.time() * 1000)}_{statement_num}"
                export_btn = f'<button class="clickhouse-button" onclick="downloadCSV(\'{export_id}\')">Export CSV</button>'
                stats_parts.append(export_btn)

                # Store DataFrame for export
                if not hasattr(self, "_export_data"):
                    self._export_data = {}
                self._export_data[export_id] = result["dataframe"]

            if stats_parts:
                stats_html = " • ".join(stats_parts)
                html_parts.append(f'<div class="{stats_class}">')
                html_parts.append(f"<span>{stats_html}</span>")
                html_parts.append("</div>")

        html_parts.append("</div>")  # Close content
        html_parts.append("</div>")  # Close container

        display(HTML("".join(html_parts)))

        # Add export functionality for DataFrames
        if result["type"] == "select" and not result["dataframe"].empty:
            export_id = f"export_{int(time.time() * 1000)}_{statement_num}"
            self._add_export_script(result["dataframe"], export_id)

    def _display_error(
        self, result: Dict[str, Any], statement_num: int = 1, total_statements: int = 1
    ):
        """Display error with beautiful formatting."""
        title = (
            f"Query {statement_num}/{total_statements} Error"
            if total_statements > 1
            else "Query Error"
        )

        html = f"""
        <div class="clickhouse-error">
            <div class="clickhouse-error-header">
                ❌ {title}
            </div>
            <div class="clickhouse-error-message">{result["error"]}</div>
            <div class="clickhouse-query">{result["sql"]}</div>
            <div style="margin-top: 8px; font-size: 11px; color: #666;">
                Execution time: {self._format_execution_time(result["execution_time"])}
            </div>
        </div>
        """
        display(HTML(html))

    def _add_export_script(self, df: pd.DataFrame, export_id: str):
        """Add JavaScript for CSV export functionality."""
        # Escape special characters properly
        csv_data = df.to_csv(index=False)
        # Escape for JavaScript string
        csv_escaped = (
            csv_data.replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("${", "\\${")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
        )

        js_code = f"""
        <script>
        function downloadCSV(exportId) {{
            const csvData = `{csv_escaped}`;
            const blob = new Blob([csvData], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            if (link.download !== undefined) {{
                const url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', 'clickhouse_query_result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv');
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
            }}
        }}
        </script>
        """
        display(HTML(js_code))

    @magic_arguments()
    @argument("--limit", "-l", type=int, help="Limit number of rows returned")
    @argument("--cache", "-c", action="store_true", help="Cache the result")
    @argument("--minimal", "-m", action="store_true", help="Use minimal display mode")
    @argument(
        "--export",
        "-e",
        type=str,
        choices=["csv", "json", "excel"],
        help="Auto-export format",
    )
    @argument("--connection", type=str, help="Use specific connection")
    @line_cell_magic
    def sql(self, line, cell=None):
        """
        Execute ClickHouse SQL query from line or cell magic.

        Usage:
            %sql SELECT * FROM table LIMIT 10
            %sql --limit 5 SELECT * FROM users
            %sql --minimal SELECT count(*) FROM transactions

            %%sql
            SELECT count(*) as total FROM transactions;
            SELECT avg(amount) as avg_amount FROM transactions WHERE date > '2023-01-01';
        """
        # Split line into arguments and SQL
        import shlex

        # Check if line contains arguments (starts with --)
        if line.strip().startswith("--"):
            # Parse arguments and extract SQL
            try:
                # Split the line into tokens
                tokens = shlex.split(line)

                # Find where SQL starts (first token that doesn't start with - and isn't a value for an argument)
                sql_start_idx = 0
                i = 0
                while i < len(tokens):
                    token = tokens[i]
                    if token.startswith("-"):
                        # This is an argument
                        if token in ["--limit", "-l", "--export", "-e", "--connection"]:
                            # These arguments take values, skip the next token too
                            i += 2
                        else:
                            # These are flag arguments (--cache, --minimal)
                            i += 1
                    else:
                        # This is where SQL starts
                        sql_start_idx = i
                        break

                # Reconstruct the argument line (everything before SQL)
                if sql_start_idx > 0:
                    arg_line = " ".join(tokens[:sql_start_idx])
                    sql = " ".join(tokens[sql_start_idx:])
                else:
                    arg_line = ""
                    sql = line

                # Parse arguments
                args = parse_argstring(self.sql, arg_line)

            except Exception:
                # If parsing fails, treat entire line as SQL with no arguments
                args = parse_argstring(self.sql, "")
                sql = line
        else:
            # No arguments, treat entire line as SQL
            args = parse_argstring(self.sql, "")
            sql = line

        # For cell magic, use cell content as SQL
        if cell is not None:
            sql = cell

        return self._execute_sql(sql, args)

    def _execute_sql(self, sql: str, args):
        """Execute SQL with given arguments."""
        if not sql.strip():
            display(
                HTML(
                    '<div style="color: #666; font-style: italic; padding: 10px;">No SQL provided</div>'
                )
            )
            return

        # Apply configurations from arguments
        original_config = self.isql_config.copy()

        if args.minimal:
            self.isql_config["minimal_mode"] = True
        if args.limit:
            self.isql_config["auto_limit"] = args.limit
        if args.cache:
            self.isql_config["cache_results"] = True

        try:
            # Get connection
            connection = self._get_connection()

            # Parse SQL statements
            statements = self._parse_sql_statements(sql)

            if not statements:
                display(
                    HTML(
                        '<div style="color: #666; font-style: italic; padding: 10px;">No valid SQL statements found</div>'
                    )
                )
                return

            # Execute statements
            results = []
            total_statements = len(statements)

            for i, statement in enumerate(statements, 1):
                # Apply auto-limit for SELECT statements if specified
                if (
                    args.limit
                    and statement.strip().upper().startswith("SELECT")
                    and "LIMIT" not in statement.upper()
                ):
                    statement = f"{statement.rstrip(';')} LIMIT {args.limit}"

                result = self._execute_single_statement(statement, connection)
                results.append(result)

                # Display result immediately
                self._display_result(result, i, total_statements)

                # Store in history
                self.query_history.append(
                    {"sql": statement, "result": result, "timestamp": datetime.now()}
                )

            # Return DataFrame(s) for further use
            if len(results) == 1 and results[0]["type"] == "select":
                self.last_result = results[0]["dataframe"]
                return results[0]["dataframe"]
            elif len(results) > 1:
                select_results = [
                    r["dataframe"]
                    for r in results
                    if r["type"] == "select" and not r["dataframe"].empty
                ]
                if select_results:
                    self.last_result = select_results
                    return select_results

            return None

        except Exception as e:
            error_html = f"""
            <div class="clickhouse-error">
                <div class="clickhouse-error-header">
                    ❌ Connection Error
                </div>
                <div class="clickhouse-error-message">{str(e)}</div>
            </div>
            """
            display(HTML(error_html))
            return None
        finally:
            # Restore original configuration
            self.isql_config = original_config

    @line_magic
    def sql_config(self, line):
        """
        Configure SQL magic settings.

        Usage:
            %sql_config max_rows_display=50
            %sql_config minimal_mode=True
            %sql_config show_execution_time=False
        """
        if not line.strip():
            # Show current configuration
            config_html = """
            <div class="clickhouse-container">
                <div class="clickhouse-header">
                    <svg class="clickhouse-logo" viewBox="0 0 24 24" fill="none">
                        <path d="M21.333 10H24v4h-2.667ZM16 1.335h2.667v21.33H16Zm-5.333 0h2.666v21.33h-2.666ZM0 22.665V1.335h2.667v21.33zm5.333 -21.33H8v21.33H5.333Z" fill="#000000"/>
                    </svg>
                    SQL Magic Configuration
                </div>
                <div class="clickhouse-content" style="padding: 20px;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #f8f9fa;">
                                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #e2e8f0;">Parameter</th>
                                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #e2e8f0;">Value</th>
                            </tr>
                        </thead>
                        <tbody>
            """

            # Access the configuration dictionary directly
            config_dict = getattr(self, "isql_config", {})

            for key, value in config_dict.items():
                config_html += f"""
                            <tr>
                                <td style="padding: 8px 10px; border-bottom: 1px solid #f1f5f9;"><strong>{key}</strong></td>
                                <td style="padding: 8px 10px; border-bottom: 1px solid #f1f5f9;"><code>{value}</code></td>
                            </tr>
                """
            config_html += """
                        </tbody>
                    </table>
                </div>
            </div>
            """
            display(HTML(config_html))
            return

        # Parse configuration changes
        config_dict = getattr(self, "isql_config", {})

        for item in line.split(","):
            if "=" in item:
                key, value = item.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Convert value to appropriate type
                if value.lower() in ("true", "false"):
                    value = value.lower() == "true"
                elif value.isdigit():
                    value = int(value)

                if key in config_dict:
                    config_dict[key] = value
                    print(f"✓ Set {key} = {value}")
                else:
                    print(f"✗ Unknown configuration key: {key}")
            else:
                print(f"✗ Invalid format: {item}. Use key=value format.")

    @line_magic
    def sql_history(self, line):
        """
        Show query history.

        Usage:
            %sql_history
            %sql_history 5  # Show last 5 queries
        """
        limit = int(line.strip()) if line.strip().isdigit() else 10

        if not self.query_history:
            display(
                HTML(
                    '<div style="color: #666; font-style: italic; padding: 10px;">No query history available</div>'
                )
            )
            return

        recent_queries = self.query_history[-limit:]

        html = """
        <div class="clickhouse-container">
            <div class="clickhouse-header">
                <svg class="clickhouse-logo" viewBox="0 0 24 24" fill="none">
                    <path d="M21.333 10H24v4h-2.667ZM16 1.335h2.667v21.33H16Zm-5.333 0h2.666v21.33h-2.666ZM0 22.665V1.335h2.667v21.33zm5.333 -21.33H8v21.33H5.333Z" fill="#000000"/>
                </svg>
                📜 Query History
            </div>
            <div class="clickhouse-content">
        """

        for i, entry in enumerate(reversed(recent_queries), 1):
            timestamp = entry["timestamp"].strftime("%H:%M:%S")
            sql_preview = (
                entry["sql"][:100] + "..." if len(entry["sql"]) > 100 else entry["sql"]
            )

            status = "✓" if entry["result"]["type"] != "error" else "✗"
            status_color = (
                "#22543d" if entry["result"]["type"] != "error" else "#c53030"
            )
            exec_time = self._format_execution_time(entry["result"]["execution_time"])

            html += f"""
            <div style="border-bottom: 1px solid #e2e8f0; padding: 12px 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="color: {status_color};"><strong>{status} Query {i}</strong> - {timestamp}</span>
                    <span style="font-size: 11px; color: #666; font-family: Monaco, monospace;">{exec_time}</span>
                </div>
                <div class="clickhouse-query" style="margin: 0;">{sql_preview}</div>
            </div>
            """

        html += "</div></div>"
        display(HTML(html))

    @line_magic
    def sql_tables(self, line):
        """
        Show available tables in the current database.

        Usage:
            %sql_tables
            %sql_tables database_name
        """
        database = line.strip() if line.strip() else "dubai_real_estate"

        sql = f"SHOW TABLES FROM `{database}`"
        return self._execute_sql(
            sql, type("Args", (), {"minimal": False, "limit": None, "cache": False})()
        )

    @line_magic
    def sql_connect(self, line):
        """
        Connect to a ClickHouse connection by name or manage connections.

        Usage:
            %sql_connect                    # Show current connection and available connections
            %sql_connect <connection_name>  # Connect to specific connection
            %sql_connect -l                 # List all available connections
            %sql_connect -s <name>          # Set connection as auto connection
            %sql_connect -d <name>          # Disconnect from specific connection
            %sql_connect -r                 # Reconnect current connection

        Examples:
            %sql_connect prod               # Connect to 'prod' connection
            %sql_connect cloud_staging      # Connect to 'cloud_staging' connection
            %sql_connect -l                 # List all connections
            %sql_connect -s prod            # Set 'prod' as auto connection
        """
        args = line.strip().split() if line.strip() else []

        # Get the connection manager
        try:
            from ..connection import get_manager

            manager = get_manager()
        except ImportError:
            from dubai_real_estate.connection import get_manager

            manager = get_manager()

        # No arguments - show current connection status
        if not args:
            self._show_connection_status(manager)
            return

        # Parse arguments
        if args[0] == "-l" or args[0] == "--list":
            self._show_connections_list(manager)
            return

        elif args[0] == "-s" or args[0] == "--set-auto":
            if len(args) < 2:
                display(
                    HTML(
                        '<div style="color: #c53030; padding: 10px;">Error: Connection name required for -s option</div>'
                    )
                )
                return
            connection_name = args[1]
            success = manager.set_auto_connection(connection_name)
            if success:
                display(
                    HTML(
                        f'<div style="color: #22543d; padding: 10px;">✓ Set "{connection_name}" as auto connection</div>'
                    )
                )
            else:
                display(
                    HTML(
                        f'<div style="color: #c53030; padding: 10px;">✗ Failed to set "{connection_name}" as auto connection</div>'
                    )
                )
            return

        elif args[0] == "-d" or args[0] == "--disconnect":
            if len(args) < 2:
                # Disconnect current connection
                if self.connection and self.connection.is_connected():
                    self.connection.disconnect()
                    display(
                        HTML(
                            '<div style="color: #22543d; padding: 10px;">✓ Disconnected from current connection</div>'
                        )
                    )
                else:
                    display(
                        HTML(
                            '<div style="color: #666; padding: 10px;">No active connection to disconnect</div>'
                        )
                    )
            else:
                connection_name = args[1]
                connection = manager.get_connection(connection_name)
                if connection and connection.is_connected():
                    connection.disconnect()
                    display(
                        HTML(
                            f'<div style="color: #22543d; padding: 10px;">✓ Disconnected from "{connection_name}"</div>'
                        )
                    )
                else:
                    display(
                        HTML(
                            f'<div style="color: #666; padding: 10px;">Connection "{connection_name}" is not active</div>'
                        )
                    )
            return

        elif args[0] == "-r" or args[0] == "--reconnect":
            if self.connection:
                try:
                    if self.connection.is_connected():
                        self.connection.disconnect()
                    self.connection.connect()
                    display(
                        HTML(
                            '<div style="color: #22543d; padding: 10px;">✓ Reconnected successfully</div>'
                        )
                    )
                except Exception as e:
                    display(
                        HTML(
                            f'<div style="color: #c53030; padding: 10px;">✗ Reconnection failed: {str(e)}</div>'
                        )
                    )
            else:
                display(
                    HTML(
                        '<div style="color: #666; padding: 10px;">No connection to reconnect</div>'
                    )
                )
            return

        # Connect to specific connection
        connection_name = args[0]

        try:
            # Get the connection
            connection = manager.get_connection(connection_name)

            if connection is None:
                display(
                    HTML(
                        f'<div style="color: #c53030; padding: 10px;">✗ Connection "{connection_name}" not found</div>'
                    )
                )
                self._show_connections_list(manager)
                return

            # Disconnect current connection if different
            if (
                self.connection
                and self.connection != connection
                and self.connection.is_connected()
            ):
                self.connection.disconnect()

            # Connect to the new connection
            if not connection.is_connected():
                connection.connect()

            # Set as current connection
            self.connection = connection

            # Show success message with connection details
            self._show_connection_success(connection)

        except Exception as e:
            error_html = f"""
            <div class="clickhouse-error">
                <div class="clickhouse-error-header">
                    ❌ Connection Error
                </div>
                <div class="clickhouse-error-message">Failed to connect to "{connection_name}": {str(e)}</div>
            </div>
            """
            display(HTML(error_html))

    def _show_connection_status(self, manager):
        """Show current connection status and available connections."""
        current_connection = self.connection
        auto_connection = manager._storage.get_auto_connection()

        html = f"""
        <div class="clickhouse-container">
            <div class="clickhouse-header">
                {self._create_clickhouse_logo_svg()}
                🔗 Connection Status
            </div>
            <div class="clickhouse-content" style="padding: 20px;">
        """

        # Current connection info
        if current_connection:
            conn_status = (
                "🟢 Connected"
                if current_connection.is_connected()
                else "🔴 Disconnected"
            )
            conn_type = current_connection.credentials.connection_type.value.upper()

            html += f"""
                <div style="margin-bottom: 20px;">
                    <h4 style="margin: 0 0 10px 0; color: #2d3748;">Current Connection</h4>
                    <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; border-left: 4px solid #FFD700;">
                        <strong>{current_connection.credentials.name}</strong> ({conn_type}) {conn_status}<br>
                        <small style="color: #666;">{current_connection.credentials.description or 'No description'}</small>
                    </div>
                </div>
            """
        else:
            html += """
                <div style="margin-bottom: 20px;">
                    <h4 style="margin: 0 0 10px 0; color: #2d3748;">Current Connection</h4>
                    <div style="background: #fff5f5; padding: 12px; border-radius: 6px; border-left: 4px solid #c53030;">
                        <em>No active connection</em>
                    </div>
                </div>
            """

        # Auto connection info
        html += f"""
            <div style="margin-bottom: 20px;">
                <h4 style="margin: 0 0 10px 0; color: #2d3748;">Auto Connection</h4>
                <div style="background: #f0fff4; padding: 12px; border-radius: 6px; border-left: 4px solid #38a169;">
                    {auto_connection or '<em>No auto connection set</em>'}
                </div>
            </div>
        """

        # Quick commands
        html += """
            <div>
                <h4 style="margin: 0 0 10px 0; color: #2d3748;">Quick Commands</h4>
                <div style="background: #fffbeb; padding: 12px; border-radius: 6px; border-left: 4px solid #FFA500;">
                    <code>%sql_connect -l</code> - List all connections<br>
                    <code>%sql_connect &lt;name&gt;</code> - Connect to specific connection<br>
                    <code>%sql_connect -s &lt;name&gt;</code> - Set auto connection<br>
                    <code>%sql_connect -r</code> - Reconnect current connection
                </div>
            </div>
        """

        html += "</div></div>"
        display(HTML(html))

    def _show_connections_list(self, manager):
        """Show list of available connections."""
        connections = manager.list_connections()

        html = f"""
        <div class="clickhouse-container">
            <div class="clickhouse-header">
                {self._create_clickhouse_logo_svg()}
                📋 Available Connections
            </div>
            <div class="clickhouse-content">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f8f9fa;">
                            <th style="padding: 12px; text-align: right; border-bottom: 2px solid #e2e8f0;">Name</th>
                            <th style="padding: 12px; text-align: right; border-bottom: 2px solid #e2e8f0;">Type</th>
                            <th style="padding: 12px; text-align: right; border-bottom: 2px solid #e2e8f0;">Status</th>
                            <th style="padding: 12px; text-align: right; border-bottom: 2px solid #e2e8f0;">Auto</th>
                            <th style="padding: 12px; text-align: right; border-bottom: 2px solid #e2e8f0;">Description</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        if not connections:
            html += """
                        <tr>
                            <td colspan="5" style="padding: 20px; text-align: center; color: #666; font-style: italic;">
                                No connections available
                            </td>
                        </tr>
            """
        else:
            for conn in connections:
                status_icon = "🟢" if conn["is_connected"] else "🔴"
                auto_icon = "⭐" if conn["is_auto"] else ""

                html += f"""
                        <tr style="border-bottom: 1px solid #f1f5f9;">
                            <td style="padding: 10px 12px;"><strong>{conn['name']}</strong></td>
                            <td style="padding: 10px 12px;"><code>{conn['type']}</code></td>
                            <td style="padding: 10px 12px;">{status_icon}</td>
                            <td style="padding: 10px 12px;">{auto_icon}</td>
                            <td style="padding: 10px 12px; color: #666;"><em>{conn['description'] or 'No description'}</em></td>
                        </tr>
                """

        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """

        display(HTML(html))

    def _show_connection_success(self, connection):
        """Show successful connection message with details."""
        conn_type = connection.credentials.connection_type.value.upper()

        # Get connection-specific details
        if hasattr(connection.credentials, "host"):
            detail = f"{connection.credentials.host}:{connection.credentials.port}"
        else:
            detail = f"Database: {connection.credentials.database_path}"

        html = f"""
        <div class="clickhouse-container">
            <div class="clickhouse-header">
                {self._create_clickhouse_logo_svg()}
                ✅ Connected Successfully
            </div>
            <div class="clickhouse-content" style="padding: 20px;">
                <div style="background: #f0fff4; padding: 16px; border-radius: 6px; border-left: 4px solid #38a169;">
                    <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px;">
                        {connection.credentials.name} ({conn_type})
                    </div>
                    <div style="color: #666; margin-bottom: 8px;">
                        {detail}
                    </div>
                    <div style="color: #666; font-size: 14px;">
                        {connection.credentials.description or 'No description'}
                    </div>
                </div>
            </div>
        </div>
        """

        display(HTML(html))


def load_ipython_extension(ipython):
    """Load the SQL magic extension."""
    magic_instance = SQLMagic(ipython)
    ipython.register_magic_function(magic_instance.sql, "line_cell", "sql")
    ipython.register_magic_function(magic_instance.sql_config, "line", "sql_config")
    ipython.register_magic_function(magic_instance.sql_history, "line", "sql_history")
    ipython.register_magic_function(magic_instance.sql_tables, "line", "sql_tables")
    ipython.register_magic_function(magic_instance.sql_connect, "line", "sql_connect")


def unload_ipython_extension(ipython):
    """Unload the SQL magic extension."""
    # Remove registered magic functions
    magic_manager = ipython.magics_manager
    if hasattr(magic_manager, "magics"):
        # Remove line and cell magics
        if "sql" in magic_manager.magics.get("line", {}):
            del magic_manager.magics["line"]["sql"]
        if "sql" in magic_manager.magics.get("cell", {}):
            del magic_manager.magics["cell"]["sql"]

        # Remove line magics
        for magic_name in ["sql_config", "sql_history", "sql_tables", "sql_connect"]:
            if magic_name in magic_manager.magics.get("line", {}):
                del magic_manager.magics["line"][magic_name]
