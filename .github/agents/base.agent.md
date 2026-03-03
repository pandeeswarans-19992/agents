## Base Agent -- Shared Contract

Purpose: Abstract base contract inherited by all agents in this repository.
Every agent must load this file before executing and must not duplicate its content.

This file contains **common knowledge only**. It does not implement any behavior.

---

### Knowledge Lens (Must Be Applied by All Agents)

Load and apply the following shared knowledge files before beginning any analysis.
These files are the single source of truth for shared context.

- Common knowledge (architecture principles, security baseline, evidence rules):
  `.github/knowledge/common-knowledge.md`
- Platform knowledge (runtime, framework, infrastructure, integration points):
  `.github/knowledge/platform-knowledge.md`
- Module knowledge (module inventory, dependency map, inter-module contracts):
  `.github/knowledge/module-knowledge.md`
- Field knowledge (domain glossary, business rules, data field definitions, state machines):
  `.github/knowledge/field-knowledge.md`
- Field context (CrmField MySQL schema, Java field API inventory, architecture files, Field Filter API guide):
  `.github/knowledge/field-context.md`

For every report, include evidence from:

- Architecture: style, boundaries, dependency direction, cross-cutting concerns
- Design patterns: useful patterns and anti-patterns
- Data structures: fitness for access/update/query workloads
- Algorithms: critical-path complexity and hotspot risks

---

### Escalation Rules (All Agents)

Set severity to CRITICAL when any of the following is found:

- Data corruption risk
- Security vulnerability
- Transaction inconsistency
- Schema-breaking risk
- Unbounded recursion in critical path
- Unhandled exception in core flow

---

### Report Output Contract (All Agents)

Save reports to:

`ai-research-report/<feature-name>/<report-name>_v<version-number>.md`

Version number must increment when the same feature + report type already exists.

---

### Governance Rules (All Agents)

- Do not assume missing facts
- Support claims with file-level and method-level evidence
- Prefer concrete recommendations over generic advice
- Use neutral, objective language
- Explicitly state unknowns and scope limits

---

### Determinism Checklist (All Agents)

- Fixed section ordering
- Stable severity scale
- Reproducible classification logic
- Evidence-backed conclusions
- Explicit classification reasoning

---

### Tool Availability and Auto-Install Protocol (All Agents)

Custom tools are provided by MCP servers located under the `.github/tools/` directory.
Each subdirectory is one MCP server:

| Server directory                      | Tool exposed            | Purpose |
|---------------------------------------|-------------------------|---------|
| `.github/tools/mcp-mysql-server/`     | `execute_mysql_query`   | Read-only MySQL SELECT execution |

**Before using any tool from the `.github/tools/` directory, verify it is available.**

#### Detection

A tool is considered unavailable when any of the following occurs:
- The tool call returns an error indicating the tool is not found or not registered.
- The MCP server process is not running.
- The required Python packages are not installed.

#### Auto-Install Steps (agents with terminal access)

When a tool is unavailable, execute the following steps **before retrying the
original task** (replace `<server-directory>` with the actual path from the table
above, e.g. `.github/tools/mcp-mysql-server`):

1. Navigate to the server directory.
2. Install Python dependencies:
   ```
   pip install -r <server-directory>/requirements.txt
   ```
3. Verify that the required environment variables are set.
   Consult the server's `README.md` and `.env` template for the full list.
   If any are missing, ask the user to supply them.
4. Start the MCP server in the background:
   ```
   python <server-directory>/server.py &
   ```
5. Re-attempt the original tool call.

If installation fails, inform the user of the error and stop.

#### Agents without terminal access

When a required tool is unavailable and the agent does not have access to a
terminal tool (`run_in_terminal`):
1. Inform the user that the MCP server must be started manually.
2. Provide the exact install and start commands from the server's `README.md`
   (e.g. for `.github/tools/mcp-mysql-server/`):
   ```
   pip install -r .github/tools/mcp-mysql-server/requirements.txt
   python .github/tools/mcp-mysql-server/server.py
   ```
3. Ask the user to restart the agent session after the server is running.
