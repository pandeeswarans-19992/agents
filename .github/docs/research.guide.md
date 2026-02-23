# Research Agent Guide

Input suggestion guide for `.github/agents/research.agent.md`.
This file is intentionally focused on **better input format only**.

## 1) Best Input Format

Each analysis type has its own input template with type-specific fields.
Use the template that matches your intended analysis type:

| Analysis Type | Input Template |
|---|---|
| CODEBASE_AUDIT | `.github/templates/code-base-audit-input-template.md` |
| NEW_FEATURE_ANALYSIS | `.github/templates/new-feature-analysis-input-template.md` |
| FEATURE_ENHANCEMENT_ANALYSIS | `.github/templates/feature-enhancement-input-template.md` |
| USE_CASE_ALIGNMENT_ANALYSIS | `.github/templates/usecase-alignment-input-template.md` |
| Unknown / auto-classify | `.github/templates/research-input-template.md` |

Open the matching template, fill in the required fields, and paste the completed form as your request.

---

## 2) CODEBASE_AUDIT Input

Key fields beyond the common set:

- **Specific Files / Methods** – files or method signatures to focus on
- **Change Intent** – DEPRECATION | MODIFICATION | CLEANUP | UNIFICATION | DISCOVERY_ONLY
- **Audit Focus** – ARCHITECTURE | SECURITY | PERFORMANCE | MAINTAINABILITY | ALL
- **Known Risk Areas** – suspected hot spots

Example:

Goal: Audit payment module for deprecated patterns and circular dependencies.
Feature / Use Case Name: payments-deprecation-cleanup
Scope In: `src/payments`
Specific Files / Methods: `src/payments/legacy-api.js`
Change Intent: DEPRECATION
Audit Focus: ARCHITECTURE, MAINTAINABILITY
Expected Output: deprecated symbol inventory, call-site impact map, removal sequence

---

## 3) NEW_FEATURE_ANALYSIS Input

Key fields beyond the common set:

- **Use Case Document / Requirements** – inline text or file path
- **Target Modules / Layers** – where the feature should land
- **API Contracts** – contracts to conform to or extend
- **Schema / Data Model Constraints** – relevant tables or boundaries
- **Backward Compatibility Requirements** – what must not break

Example:

Goal: Analyze implementation strategy for bulk invoice export.
Feature / Use Case Name: bulk-invoice-export
Use Case Document / Requirements: docs/use-cases/bulk-export.md
Target Modules / Layers: `src/invoice`, `src/reporting`
Known Files / Modules: `api/openapi.yaml`
Backward Compatibility Requirements: Keep backward compatibility for current invoice APIs.
Expected Output: architecture insertion points, API/schema delta, phased plan

---

## 4) FEATURE_ENHANCEMENT_ANALYSIS Input

Key fields beyond the common set:

- **Enhancement Type** – DEPRECATION | MODIFICATION | CLEANUP | UNIFICATION
- **Specific Files / Methods** – primary targets of the change
- **Current Behavior** – what the code does today
- **Desired Change** – what it should do after the enhancement
- **Migration Constraints** – e.g. no schema breaking change, must be feature-flagged
- **Rollback Requirements** – what a safe rollback looks like

Example:

Goal: Improve retry behavior in payment capture flow.
Feature / Use Case Name: payment-capture-retry
Enhancement Type: MODIFICATION
Specific Files / Methods: `src/payments/capture.js::processCapture`
Scope In: `src/payments/capture*`, queue workers
Current Behavior: Retries up to 3 times with fixed 1 s delay; no dead-letter queue.
Desired Change: Exponential back-off, max 5 retries, DLQ on final failure.
Migration Constraints: No schema breaking change; must be feature-flagged.
Rollback Requirements: Disable feature flag reverts to current behavior without data loss.
Expected Output: impact surface, regression risks, rollback strategy

---

## 5) USE_CASE_ALIGNMENT_ANALYSIS Input

Key fields beyond the common set:

- **Use Case Document** – inline text or file path
- **Specific Behaviors to Verify** – individual expected behaviors (optional; agent extracts from doc if omitted)
- **Compliance / Audit Requirements** – regulatory or internal compliance needs
- **Coverage Threshold** – minimum acceptable alignment score

Example:

Goal: Verify password-reset flow against use case document.
Feature / Use Case Name: password-reset
Use Case Document: docs/use-cases/password-reset.md
Specific Behaviors to Verify:
  - Token must expire after 15 minutes.
  - Reset link must be single-use.
Known Implementation Files: `src/auth`, `src/notification`
Compliance / Audit Requirements: Compliance and audit logging required.
Expected Output: behavior-to-code mapping, coverage gaps, alignment score

---

## 6) Input Quality Checklist

Before sending a request, ensure:

- You select and fill the template matching your analysis type.
- You state one clear goal.
- You mention feature/use-case name.
- You provide at least one scope/module hint.
- You include constraints (if any).
- You specify expected output.

---

## 7) Good vs Weak Input

### Weak

"Analyze this project."

### Good

"Run FEATURE_ENHANCEMENT_ANALYSIS for payment-capture-retry. Enhancement Type: MODIFICATION. Specific Files: `src/payments/capture.js`. Scope in `src/payments` and queue workers, scope out UI. Current behavior: fixed retry delay, no DLQ. Desired change: exponential back-off with DLQ. Must keep backward compatibility and no schema breaking changes. Output risk matrix, rollback strategy, and phased roadmap."

---

## 8) Clarification Prompt (If Unsure)

If you are unsure about analysis type, use:

"Classify this request first, explain confidence, then proceed with analysis using the correct templates."

---

## 9) Where to Check the Report

Generated reports are saved at:

`ai-research-report/<feature-name>/<report-name>_v<version-number>.md`

Examples:

- `ai-research-report/payment-capture-retry/feature-enhancement-analysis_v1.md`
- `ai-research-report/password-reset/usecase-alignment-analysis_v2.md`

Quick checks:

- Open the `ai-research-report/` folder in your project root.
- Open the latest version file (`_v2`, `_v3`, etc.) for your feature.
