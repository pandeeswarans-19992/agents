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
