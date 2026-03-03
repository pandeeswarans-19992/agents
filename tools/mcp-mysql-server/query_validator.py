"""
query_validator.py — Ensures only safe, read-only SELECT queries are executed.

Rules enforced:
  - Query must begin with SELECT (after stripping leading whitespace/comments).
  - Forbidden DML/DDL keywords (INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
    TRUNCATE, EXEC, EXECUTE) are rejected regardless of position.
  - Stacked queries separated by semicolons are rejected.
"""

import re

# Keywords that must never appear anywhere in the query.
_FORBIDDEN = re.compile(
    r'\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|EXEC|EXECUTE)\b',
    re.IGNORECASE,
)

# Strip single-line (--) and multi-line (/* */) SQL comments before checking.
_SINGLE_LINE_COMMENT = re.compile(r'--[^\n]*')
_MULTI_LINE_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)


def validate_query(query: str) -> None:
    """Raise ValueError if *query* is not a safe, read-only SELECT statement.

    Args:
        query: Raw SQL string supplied by the caller.

    Raises:
        ValueError: When the query violates any safety rule.
    """
    if not query or not query.strip():
        raise ValueError("Query must not be empty.")

    # Remove comments so they cannot mask forbidden keywords.
    cleaned = _SINGLE_LINE_COMMENT.sub(" ", query)
    cleaned = _MULTI_LINE_COMMENT.sub(" ", cleaned)
    stripped = cleaned.strip()

    # Must start with SELECT.
    if not stripped.upper().startswith("SELECT"):
        raise ValueError(
            f"Only SELECT queries are permitted. Received statement starting with: "
            f"'{stripped[:50]}'"
        )

    # Reject stacked queries (multiple statements).
    # A semicolon is only allowed at the very end (optional terminator).
    without_trailing = stripped.rstrip("; \t\n\r")
    if ";" in without_trailing:
        raise ValueError(
            "Stacked queries are not permitted. Remove the semicolon separating "
            "multiple statements."
        )

    # Reject forbidden DML/DDL keywords.
    match = _FORBIDDEN.search(stripped)
    if match:
        raise ValueError(
            f"Forbidden SQL keyword detected: '{match.group()}'. "
            "Only read-only SELECT queries are permitted."
        )
