# agents

Prompt assets for Copilot custom agents with separate analysis-step templates and report-output templates.

## Structure

- `.github/agents/research.agent.md`: main research-agent operating specification
- `.github/docs/*.guide.md`: per-agent implementation guides (`<agent>.guide.md`)
- `.github/templates/*-analysis-template.md`: required case-specific analysis steps
- `.github/templates/*-report-template.md`: final report output structure

## Agent + Guide Convention

For every new agent, add both files:

1. `.github/agents/<agent>.agent.md`
2. `.github/docs/<agent>.guide.md`

`<agent>.guide.md` must include:
- scope and responsibilities
- input checklist
- common workflow expectations
- template mapping
- quality gates and escalation rules

## Create More Agents

Use this repository as the source for additional specialized agents (security, performance, migration, API governance, etc.).

1. Create `.github/agents/<agent>.agent.md`.
2. Create `.github/docs/<agent>.guide.md`.
3. Define agent contract clearly:
   - mission and scope
   - supported analysis modes
   - required inputs
   - common workflow and quality gates
   - evidence and determinism rules
4. Choose or create template pairs:
   - `*-analysis-template.md` for required execution steps
   - `*-report-template.md` for final output format
5. Add template mapping in the agent file.
6. Run one dry analysis and verify output sections and evidence quality.


## Authoring Rule

When updating analysis procedure, change only the relevant `*-analysis-template.md` file.
When updating report layout/fields, change only the relevant `*-report-template.md` file.

## Clone and Use in Existing Projects

Recommended approach: pull this repository into the target project root, then configure your IDE to use the agent files.

### Option A: Clone into project root (your suggested flow)

From target project root:

1. `git clone <this-repo-url> agents`
2. Keep files at:
	 - `agents/.github/agents/`
	 - `agents/.github/docs/`
	 - `agents/.github/templates/`
3. Configure IDE custom-agent settings to point to the agent file(s), for example:
	 - `agents/.github/agents/research.agent.md`
4. Verify template paths in agent files are resolvable from your IDE/project context.

### Option B: Copy into target repository `.github/`

1. Copy required files into target repo:
	 - `.github/agents/*.agent.md`
	 - `.github/docs/*.guide.md`
	 - `.github/templates/*-analysis-template.md`
	 - `.github/templates/*-report-template.md`
2. Keep relative paths unchanged.
3. Run a dry analysis to verify classification, template selection, and output structure.

## IDE Configuration Notes

Exact menus can differ by plugin/version. Use your IDE's custom-agent or prompt-file configuration to register the agent markdown files.

- VS Code:
	- Open Copilot/agent settings.
	- Add agent file path(s), for example `agents/.github/agents/research.agent.md`.
	- Ensure workspace trust and file access permissions are enabled.

- IntelliJ IDEA:
	- Open GitHub Copilot plugin settings.
	- Register custom prompt/agent file path(s).
	- Confirm project root path resolution for template references.

- Eclipse:
	- Open Copilot/plugin preferences.
	- Configure custom instruction/agent file locations.
	- Validate relative path access to templates and docs.

## Recommended Rollout Pattern

- Phase 1: Add `research.agent.md` + `research.guide.md` + existing 4 template pairs.
- Phase 2: Add one new specialized agent (for example, security review).
- Phase 3: Standardize metadata and output location across all agents.
- Phase 4: Add CI checks for template path integrity and required sections.