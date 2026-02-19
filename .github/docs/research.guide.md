# Research Agent Guide

Input suggestion guide for `.github/agents/research.agent.md`.
This file is intentionally focused on **better input format only**.

## 1) Best Input Format (Use This Template)

Provide your request with these fields:

- Goal:
- Analysis Type (optional):
- Feature / Use Case Name:
- Scope In:
- Scope Out:
- Known Files / Modules:
- Constraints (security/performance/time):
- Expected Output:

## 2) Minimal Input Examples by Analysis Type

### CODEBASE_AUDIT

Goal: audit architecture and execution risks.
Feature / Use Case Name: order-processing
Scope In: `src/orders`, `src/payments`, `db/migrations`
Scope Out: tests, docs
Expected Output: risk matrix, maturity level, roadmap

### NEW_FEATURE_ANALYSIS

Goal: analyze implementation strategy for bulk invoice export.
Feature / Use Case Name: bulk-invoice-export
Known Files / Modules: `src/invoice`, `src/reporting`, `api/openapi.yaml`
Constraints: keep backward compatibility for current invoice APIs
Expected Output: architecture insertion points, API/schema delta, phased plan

### FEATURE_ENHANCEMENT_ANALYSIS

Goal: improve retry behavior in payment capture flow.
Feature / Use Case Name: payment-capture-retry
Scope In: `src/payments/capture*`, queue workers
Constraints: no schema breaking change
Expected Output: impact surface, regression risks, rollback strategy

### USE_CASE_ALIGNMENT_ANALYSIS

Goal: verify password-reset flow against use case document.
Feature / Use Case Name: password-reset
Known Files / Modules: `src/auth`, `src/notification`
Constraints: compliance and audit logging required
Expected Output: behavior-to-code mapping, coverage gaps, alignment score

## 3) Input Quality Checklist

Before sending a request, ensure:

- You state one clear goal.
- You mention feature/use-case name.
- You provide at least one scope/module hint.
- You include constraints (if any).
- You specify expected output.

## 4) Good vs Weak Input

### Weak

"Analyze this project."

### Good

"Run FEATURE_ENHANCEMENT_ANALYSIS for payment-capture-retry. Scope in `src/payments` and queue workers, scope out UI. Must keep backward compatibility and no schema breaking changes. Output risk matrix, rollback strategy, and phased roadmap."

## 5) Clarification Prompt (If Unsure)

If you are unsure about analysis type, use:

"Classify this request first, explain confidence, then proceed with analysis using the correct templates."

## 6) Where to Check the Report

Generated reports are saved at:

`ai-research-report/<feature-name>/<report-name>_v<version-number>.md`

Examples:

- `ai-research-report/payment-capture-retry/feature-enhancement-analysis_v1.md`
- `ai-research-report/password-reset/usecase-alignment-analysis_v2.md`

Quick checks:

- Open the `ai-research-report/` folder in your project root.
- Open the latest version file (`_v2`, `_v3`, etc.) for your feature.
