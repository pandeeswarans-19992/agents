# agents

Reusable custom-agent assets for repository research and structured reporting.

This repository follows a split-template model by default:
- `*-input-template.md` = type-specific request input format (one per analysis type)
- `*-report-template.md` = report output format

Agent-specific exception:
- `.github/agents/*.agent.md` uses in-agent deep workflow steps for execution logic.
- It still uses `*-input-template.md` and `*-report-template.md`.

Shared knowledge that all agents rely on lives in [.github/knowledge](.github/knowledge).
Detailed per-agent usage guidance lives in [.github/docs](.github/docs).

## Repository Layout

- `.github/agents/`
  - `base.agent.md` – shared base contract (knowledge lens, governance, escalation rules, tool auto-install protocol)
  - agent definitions (`*.agent.md`):
    - `research.agent.md` – call-hierarchy driven code analysis, impact assessment, migration audits
    - `field-filter-api-assistant.agent.md` – Filter API assistant (filter suggestion, field visibility debug, MySQL diagnostics, MCP escalation for unresolved queries)
- `.github/docs/`
  - per-agent guides (`*.guide.md`):
    - `research.guide.md` – example queries and tips for the research agent
    - `field-filter-api-assistant.guide.md` – example queries, credential setup, and MCP configuration for the Field Filter API assistant
- `.github/knowledge/`
  - shared knowledge files loaded by all agents:
    - `common-knowledge.md` – architecture principles, security baseline, evidence rules
    - `platform-knowledge.md` – runtime, framework, infrastructure, integration points
    - `module-knowledge.md` – module inventory, dependency map, inter-module contracts
    - `field-knowledge.md` – domain glossary, business rules, data field definitions
    - `field-context.md` – CrmField MySQL schema, Java field API inventory, architecture files, Field Filter API guide
    - `filter-knowledge.md` – Filter API field properties, operators, diagnostic query templates, and MCP integration contract
- `.github/templates/`
  - input templates (`*-input-template.md`) – one per analysis type plus a generic fallback:
    - `research-input-template.md` – generic fallback
    - `code-base-audit-input-template.md`
    - `new-feature-analysis-input-template.md`
    - `feature-enhancement-input-template.md`
    - `usecase-alignment-input-template.md`
    - `field-filter-api-assistant-input-template.md` – Filter API suggestion, field visibility debug, field listing
  - report templates (`*-report-template.md`):
    - `code-base-audit-report-template.md`
    - `new-feature-analysis-report-template.md`
    - `feature-enhancement-report-template.md`
    - `usecase-alignment-report-template.md`
- `tools/`
  - custom MCP tool servers – one subdirectory per server:
    - `mcp-mysql-server/` – MCP server exposing `execute_mysql_query` (read-only MySQL SELECT)

## Add a New Agent

1. Create agent file:
	- `.github/agents/<agent>.agent.md`
2. Create guide file:
	- `.github/docs/<agent>.guide.md`
3. Add or reuse input template (per agent, per analysis type):
	- `.github/templates/<type>-input-template.md`
4. Add or reuse output templates for the agent:
	- `.github/templates/<type>-report-template.md`
5. define deep execution steps directly inside the agent file
6. Load the base agent contract (knowledge lens, governance, escalation rules, tool auto-install protocol) at the start of the agent file:
	- `.github/agents/base.agent.md`
7. Add template mappings inside the agent file.
8. Run one dry execution and verify evidence + output sections.

## Add a New Tool Server

Each custom tool lives under `tools/<server-name>/` and follows the structure of
`tools/mcp-mysql-server/` as the reference implementation.

1. Create the server directory:
	- `tools/<server-name>/`
2. Add the required files:
	- `server.py` – MCP server entry point; expose tools using `FastMCP`.
	- `query_validator.py` (or equivalent) – input validation before execution.
	- `requirements.txt` – Python dependencies.
	- `package.json` – Server metadata, `start` and `install-deps` npm scripts, and `mcp` config block.
	- `README.md` – Setup instructions, tool list, and safety constraints.
	- `.env` – Credential/config template (tracked; real values must never be committed).
	- `.gitignore` – Exclude `.env.local`, `__pycache__`, and compiled files.
3. Register the new tool in the base agent contract:
	- `.github/agents/base.agent.md` → **Tool Availability and Auto-Install Protocol** table.
4. List the tool in any agent that needs it (front-matter `tools:` array).
5. Add auto-install steps to agents with terminal access; add the manual-install guidance to agents without terminal access.

## Use This Repo in Existing Projects

### Option A (recommended): Clone into project root

From target project root:

1. `git clone <repo-url> agents`
2. Keep paths unchanged:
	- `agents/.github/agents/`
	- `agents/.github/docs/`
	- `agents/.github/knowledge/`
	- `agents/.github/templates/`
3. Point your IDE custom-agent configuration to the required agent file.

### Option B: Copy into target project `.github/`

1. Copy folders into target repository:
	- `.github/agents/`
	- `.github/docs/`
	- `.github/knowledge/`
	- `.github/templates/`
2. Keep relative paths unchanged so template and knowledge mappings remain valid.

## IDE Configuration (Detailed)

Menu names differ by IDE version/plugin. Use the steps below as a practical checklist.

### VS Code (GitHub Copilot)

1. Open the target workspace.
2. Ensure workspace is trusted.
3. Open GitHub Copilot settings.
4. Add/register the agent instruction file path, for example:
	- `agents/.github/agents/research.agent.md`
	- `agents/.github/agents/field-filter-api-assistant.agent.md`
5. Confirm referenced templates and knowledge files are accessible from the same workspace:
	- `agents/.github/templates/*.md`
	- `agents/.github/knowledge/*.md`
6. Run a test request and verify report output path is created.

Validation checklist:
- Agent loads without path errors.
- Knowledge files are resolved and applied.
- Required template references are resolved for that agent mode.
- Output appears under `ai-research-report/`.

### IntelliJ IDEA (GitHub Copilot plugin)

1. Open project and enable GitHub Copilot plugin.
2. Open plugin settings / custom instructions area.
3. Register agent file path, for example:
	- `agents/.github/agents/research.agent.md`
4. Ensure project root includes the cloned `agents` folder (or copied `.github` paths).
5. Run a sample prompt and confirm template references resolve.

Validation checklist:
- No unresolved template-path or knowledge-path warnings.
- Agent behavior follows selected analysis type.
- Report is written to expected output folder.

### Eclipse (Copilot-compatible plugin)

1. Install and enable the Copilot/custom prompt plugin.
2. Open Preferences for the plugin.
3. Set instruction/agent file location to:
	- `agents/.github/agents/research.agent.md`
4. Verify plugin has workspace file read access.
5. Execute a sample analysis and verify report generation.

Validation checklist:
- Agent file is read successfully.
- Templates are reachable from configured root.
- Output file is generated under `ai-research-report/`.

## Troubleshooting

- Template not found:
  - Check relative paths in agent mapping.
  - Ensure clone/copy path matches README examples.
- Agent loads but output is incomplete:
	- Verify required assets exist for that agent (`input` + `report`).
  - Ensure request includes clear scope and expected output.
- Report not generated:
  - Confirm write permissions in project root.
  - Check whether `ai-research-report/` is ignored or blocked by tooling.
- MySQL credential errors (field-filter-api-assistant):
  - Ensure `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` are set as environment variables.
  - Use a **read-only** service account — the agent only executes `SELECT` queries.
  - Never paste the password into the agent chat; supply it only through the environment or a secrets manager.
  - If the connection fails, the agent will stop the diagnostic and offer to escalate via MCP.
- MCP escalation not working:
  - Ensure `MCP_SERVER_URL`, `MCP_OAUTH_TOKEN`, and `MCP_CHAT_ID` are set as environment variables.
  - The agent uses OAuth Bearer authentication; verify the token is valid and not expired.
  - If any MCP variable is missing, the agent informs the user and skips the escalation step.
- Agent delegates unexpectedly:
  - The research agent automatically delegates Filter API tasks to field-filter-api-assistant.
  - If you want to handle everything in one agent session, rephrase the request to avoid Filter API triggers
    or use the field-filter-api-assistant directly for pure Filter API queries.

## Runtime Modes (Research Agent)

The research agent supports forced classification modes. Use these when automatic classification
picks the wrong type:

| Mode | Usage |
|---|---|
| `AUTO` (default) | Agent classifies based on request keywords and context |
| `FORCE_AUDIT` | Forces CODEBASE_AUDIT regardless of request content |
| `FORCE_NEW_FEATURE` | Forces NEW_FEATURE_ANALYSIS |
| `FORCE_ENHANCEMENT` | Forces FEATURE_ENHANCEMENT_ANALYSIS |
| `FORCE_ALIGNMENT` | Forces USE_CASE_ALIGNMENT_ANALYSIS |
| `FORCE_HYBRID` | Forces HYBRID_ANALYSIS |
| `FORCE_MIGRATION_AUDIT` | Forces FEATURE_ENHANCEMENT_ANALYSIS with MIGRATION_AUDIT sub-type |

To activate, prefix your request with the mode name:
> `FORCE_MIGRATION_AUDIT: Analyze the custom actions migration from legacy to generic framework.`

## Agent Delegation

The agents support automatic delegation:

| From | To | Trigger |
|---|---|---|
| `research` | `field-filter-api-assistant` | Request includes Filter API suggestion or field visibility diagnosis |
| Any agent | `research` | Request requires deep call-hierarchy analysis or migration planning |

The delegating agent passes full context to the specialist and incorporates the result.
No manual agent switching is needed in most cases.
