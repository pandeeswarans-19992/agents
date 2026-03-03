#!/usr/bin/env python3
"""
server.py — MCP MySQL Server

Exposes a single MCP tool:
  - execute_mysql_query(query): Executes a read-only SELECT query against the
    configured MySQL database and returns the results as a Markdown table.

Configuration is read from environment variables (see .env for the full list).
Only SELECT statements are permitted; the query_validator module enforces this.

Start the server:
  python server.py

Or via npm:
  npm start
"""

import os
import json

import mysql.connector
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from query_validator import validate_query

# Load .env file when present (development convenience; production should
# supply env vars through the runtime environment directly).
load_dotenv()

mcp = FastMCP(
    name="mcp-mysql-server",
    instructions=(
        "Provides read-only MySQL query execution for agents. "
        "Only SELECT statements are permitted."
    ),
)


def _get_connection() -> mysql.connector.MySQLConnection:
    """Return a new MySQL connection using environment-supplied credentials.

    Raises:
        EnvironmentError: If any required credential variable is missing.
        mysql.connector.Error: If the connection cannot be established.
    """
    required = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Set them in the .env file or the process environment."
        )

    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "3306")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connection_timeout=10,
    )


def _rows_to_markdown(rows: list[dict]) -> str:
    """Format a list of row dicts as a Markdown table string."""
    if not rows:
        return "No rows found"

    headers = list(rows[0].keys())
    header_row = "| " + " | ".join(headers) + " |"
    separator = "|" + "|".join(["---"] * len(headers)) + "|"
    data_rows = "\n".join(
        "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |"
        for row in rows
    )
    return "\n".join([header_row, separator, data_rows])


@mcp.tool()
def execute_mysql_query(query: str) -> str:
    """Execute a read-only MySQL SELECT query and return results as a Markdown table.

    Args:
        query: A SQL SELECT statement to execute against the configured database.
               INSERT, UPDATE, DELETE, DROP, ALTER, and other write/DDL statements
               are rejected.

    Returns:
        Query results formatted as a Markdown table, or "No rows found" when the
        result set is empty.

    Raises:
        ValueError: If the query violates the SELECT-only constraint.
        EnvironmentError: If required credential environment variables are missing.
        mysql.connector.Error: If the database connection or query execution fails.
    """
    # Validate before touching the database.
    validate_query(query)

    conn = _get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        return _rows_to_markdown(rows)
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")
