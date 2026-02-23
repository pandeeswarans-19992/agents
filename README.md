# agents

Reusable custom-agent assets for repository research and structured reporting.

This repository follows a split-template model:
- `*-input-template.md` = type-specific request input format (one per analysis type)
- `*-analysis-template.md` = required execution steps
- `*-report-template.md` = report output format

Shared knowledge that all agents rely on lives in [.github/knowledge](.github/knowledge).
Detailed per-agent usage guidance lives in [.github/docs](.github/docs).

## Repository Layout

- `.github/agents/`
  - agent definitions (`*.agent.md`)
- `.github/docs/`
  - per-agent guides (`*.guide.md`)
- `.github/knowledge/`
  - shared knowledge files loaded by all agents:
    - `common-knowledge.md` – architecture principles, security baseline, evidence rules
    - `platform-knowledge.md` – runtime, framework, infrastructure, integration points
    - `module-knowledge.md` – module inventory, dependency map, inter-module contracts
    - `field-knowledge.md` – domain glossary, business rules, data field definitions
- `.github/templates/`
  - input templates (`*-input-template.md`) – one per analysis type plus a generic fallback
  - analysis templates (`*-analysis-template.md`)
  - report templates (`*-report-template.md`)

## Add a New Agent

1. Create agent file:
	- `.github/agents/<agent>.agent.md`
2. Create guide file:
	- `.github/docs/<agent>.guide.md`
3. Add or reuse input template (one per analysis type):
	- `.github/templates/code-base-audit-input-template.md`
	- `.github/templates/new-feature-analysis-input-template.md`
	- `.github/templates/feature-enhancement-input-template.md`
	- `.github/templates/usecase-alignment-input-template.md`
	- `.github/templates/research-input-template.md` (generic fallback)
4. Add or reuse analysis/report template pair:
	- `.github/templates/<type>-analysis-template.md`
	- `.github/templates/<type>-report-template.md`
5. Reference knowledge files inside the agent (do not duplicate their content):
	- `.github/knowledge/common-knowledge.md`
	- `.github/knowledge/platform-knowledge.md`
	- `.github/knowledge/module-knowledge.md`
	- `.github/knowledge/field-knowledge.md`
6. Add template and knowledge mappings inside the agent file.
7. Run one dry execution and verify evidence + output sections.

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
5. Confirm referenced templates and knowledge files are accessible from the same workspace:
	- `agents/.github/templates/*.md`
	- `agents/.github/knowledge/*.md`
6. Run a test request and verify report output path is created.

Validation checklist:
- Agent loads without path errors.
- Knowledge files are resolved and applied.
- Analysis/report templates are resolved.
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
  - Verify both template types exist (`analysis` + `report`).
  - Ensure request includes clear scope and expected output.
- Report not generated:
  - Confirm write permissions in project root.
  - Check whether `ai-research-report/` is ignored or blocked by tooling.