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
  - `base.agent.md` – shared base contract (knowledge lens, governance, escalation rules)
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
6. Load the base agent contract (knowledge lens, governance, escalation rules) at the start of the agent file:
	- `.github/agents/base.agent.md`
7. Add template mappings inside the agent file.
8. Run one dry execution and verify evidence + output sections.

## Use This Repo in Existing Projects

### Option A (recommended): Add as a Git Submodule

From default branch of target project root:

1. Add the submodule (mounts this repo at `.github/`):
	```bash
	git submodule add <repo-url> .github
	```
2. Commit the changes (Git auto-creates a `.gitmodules` file):
	```bash
	git add .gitmodules .github
	git commit -m "Add agents repo as .github submodule"
	```
3. Resulting paths in the consuming project:
	- `.github/agents/`
	- `.github/docs/`
	- `.github/knowledge/`
	- `.github/templates/`
4. Point your IDE custom-agent configuration to the required agent file.

#### For collaborators cloning the project for the first time

```bash
git clone --recurse-submodules <project-url>
```

Or, if already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

#### Updating the submodule to the latest version

```bash
git submodule update --remote .github
git add .github
git commit -m "Update agents submodule to latest"
```

### Option B: Copy into target project `.github/`

1. Copy folders into target repository:
	- `.github/agents/`
	- `.github/docs/`
	- `.github/knowledge/`
	- `.github/templates/`
2. Keep relative paths unchanged so template and knowledge mappings remain valid.

> **Note:** With this option you must manually sync updates from the source repo.

## IDE Configuration (Detailed)

Menu names differ by IDE version/plugin. Use the steps below as a practical checklist.

> **Prerequisite:** Ensure the submodule is initialized before configuring your IDE:
> ```bash
> git submodule update --init --recursive
> ```

### VS Code (GitHub Copilot)

1. Open the target workspace.
2. Ensure workspace is trusted.
3. Open GitHub Copilot settings.
4. Add/register the agent instruction file path, for example:
	- `.github/agents/research.agent.md`
	- `.github/agents/field-filter-api-assistant.agent.md`
5. Confirm referenced templates and knowledge files are accessible from the same workspace:
	- `.github/templates/*.md`
	- `.github/knowledge/*.md`
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
	- `.github/agents/research.agent.md`
4. Ensure `.github` submodule is initialized and populated.
5. Run a sample prompt and confirm template references resolve.

Validation checklist:
- No unresolved template-path or knowledge-path warnings.
- Agent behavior follows selected analysis type.
- Report is written to expected output folder.

### Eclipse (Copilot-compatible plugin)

1. Install and enable the Copilot/custom prompt plugin.
2. Open Preferences for the plugin.
3. Set instruction/agent file location to:
	- `.github/agents/research.agent.md`
4. Verify plugin has workspace file read access.
5. Execute a sample analysis and verify report generation.

Validation checklist:
- Agent file is read successfully.
- Templates are reachable from configured root.
- Output file is generated under `ai-research-report/`.

## Troubleshooting

- Submodule folder (`.github/`) is empty:
  - Run `git submodule update --init --recursive`.
- Submodule not picking up latest changes:
  - Run `git submodule update --remote .github`, then commit the update.
- Template not found:
  - Check relative paths in agent mapping.
  - Ensure submodule/copy path matches README examples.
- Agent loads but output is incomplete:
	- Verify required assets exist for that agent (`input` + `report`).
  - Ensure request includes clear scope and expected output.
- Report not generated:
  - Confirm write permissions in project root.
  - Check whether `ai-research-report/` is ignored or blocked by tooling.