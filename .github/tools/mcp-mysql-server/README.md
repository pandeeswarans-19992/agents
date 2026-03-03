# mcp-mysql-server — MCP MySQL Tool Server

A lightweight [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server
that exposes a single, read-only MySQL query tool to GitHub Copilot agents.

---

## Tool Provided

| Tool name             | Description |
|-----------------------|-------------|
| `execute_mysql_query` | Executes a `SELECT` query against the configured MySQL database and returns results as a Markdown table. All other statement types are rejected. |

---

## Quick Start

### 1. Install Python dependencies

```bash
cd .github/tools/mcp-mysql-server
pip install -r requirements.txt
```

Or using the npm alias:

```bash
npm run install-deps
```

### 2. Configure credentials

Copy `.env` and fill in your values (never commit the filled file):

```bash
cp .env .env.local   # or edit .env directly for local dev
```

| Variable      | Required | Default | Description |
|---------------|----------|---------|-------------|
| `DB_HOST`     | ✅       | —       | MySQL server hostname or IP |
| `DB_PORT`     | ❌       | `3306`  | MySQL port |
| `DB_NAME`     | ✅       | —       | Target database name |
| `DB_USER`     | ✅       | —       | Read-only service account username |
| `DB_PASSWORD` | ✅       | —       | Service account password (never log or expose) |

> **Security note:** Always use a **read-only** MySQL account. The server enforces
> `SELECT`-only at the application layer (`query_validator.py`), but a read-only
> database account provides an additional defence-in-depth layer.

### 3. Start the server

```bash
python server.py
```

Or using the npm alias:

```bash
npm start
```

The server communicates over **stdio** using the MCP protocol. Register it in your
IDE's MCP configuration (see below).

---

## IDE Registration

### VS Code — GitHub Copilot (`.vscode/mcp.json`)

```json
{
  "servers": {
    "mcp-mysql-server": {
      "command": "python",
      "args": [".github/tools/mcp-mysql-server/server.py"],
      "env": {
        "DB_HOST": "${env:DB_HOST}",
        "DB_PORT": "${env:DB_PORT}",
        "DB_NAME": "${env:DB_NAME}",
        "DB_USER": "${env:DB_USER}",
        "DB_PASSWORD": "${env:DB_PASSWORD}"
      }
    }
  }
}
```

---

## File Structure

```
.github/tools/mcp-mysql-server/
├── server.py            # MCP server entry point; exposes execute_mysql_query
├── query_validator.py   # Validates queries are SELECT-only before execution
├── requirements.txt     # Python dependencies
├── package.json         # Server metadata, npm start/install-deps scripts, MCP config
├── README.md            # This file
├── .env                 # Environment variable template (do not commit filled values)
└── .gitignore           # Excludes .env, __pycache__, and compiled Python files
```

---

## Safety Constraints

The server enforces the following constraints via `query_validator.py`:

1. Query **must start with `SELECT`** — no DML or DDL.
2. **Forbidden keywords** (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`,
   `TRUNCATE`, `EXEC`, `EXECUTE`) are rejected wherever they appear.
3. **Stacked queries** (multiple statements separated by `;`) are rejected.
4. SQL comments are stripped before validation so they cannot mask forbidden keywords.

---

## Agent Integration

Agents reference this server's tool as `execute_mysql_query` in their tool list.
If the tool is unavailable during agent execution, the agent must auto-install
and start the server before retrying (see `.github/agents/base.agent.md` for
the auto-install protocol).
