# Research Agent Guide

Example user queries for `.github/agents/research.agent.md`.
This guide shows how to phrase requests to get the best output from the research agent.

---

## CODEBASE_AUDIT -- Example Queries

### Deprecation review

> "Audit `src/payments` for deprecated API methods. I need to know which methods are still called, by whom, and in what order they can be safely removed."

> "Find all dead code and unused dependencies in the order-processing module. Flag anything that blocks a future cleanup."

### Architecture review

> "Give me a full architecture audit of `src/orders` and `src/payments`. I'm looking for circular dependencies, tight coupling, and scalability bottlenecks. Output a risk matrix and a recommended refactor order."

### Security-focused audit

> "Audit the authentication module for security vulnerabilities, unvalidated inputs, and missing error handling. I need a severity-ranked list with file and line evidence."

### Unification feasibility

> "We have two notification service implementations under `src/notifications/v1` and `src/notifications/v2`. Assess whether they can be merged and what the risks are."

---

## NEW_FEATURE_ANALYSIS -- Example Queries

> "Analyze how to add bulk invoice export to the system. Jobs must be async, support CSV and PDF, and notify users by email. I need the best insertion points, any API or schema changes, and a phased plan."

> "We want to add multi-factor authentication for admin users using TOTP. Where should it live in the current architecture? What schema changes are needed? Keep existing sessions valid."

> "Plan the implementation of a real-time stock reservation feature at checkout. It must integrate with the existing order and payment flows without breaking backward compatibility."

---

## FEATURE_ENHANCEMENT_ANALYSIS -- Example Queries

### Modification

> "The payment capture retry logic retries 3 times with a fixed 1-second delay and has no dead-letter queue. I want exponential back-off, 5 retries max, and a DLQ on final failure — behind a feature flag. Give me the impact surface and a rollback strategy."

> "Improve the search API to support pagination and sorting. It currently returns all results at once. Show me what changes and what regression risks exist."

### Cleanup

> "Remove all code paths guarded by feature flags `LEGACY_CHECKOUT_V1` and `OLD_PRICING_ENGINE` — both flags have been permanently disabled. Identify all affected files and give me a safe deletion sequence."

### Deprecation removal

> "The synchronous payment endpoint in `src/api/v1/payment.js` is still active but should be replaced by the async flow. Map all its callers, plan their migration, and then show how to safely remove the sync path."

---

## USE_CASE_ALIGNMENT_ANALYSIS -- Example Queries

> "Verify the password-reset flow against our use case doc at `docs/use-cases/password-reset.md`. I specifically want to confirm: token expiry after 15 minutes, single-use links, and failed-attempt logging. We require full audit logging."

> "Check whether the checkout flow in `src/checkout` matches the use case spec below. I need a behavior-to-code mapping, a gap list with severity, and an alignment score. [paste use case here]"

> "Validate the admin MFA flow against OWASP ASVS Level 2. Map each requirement to the code that satisfies it and flag anything that is missing or only partially covered."

---

## Tips for Better Queries

- **Name the feature**: include a short kebab-case name so the agent can name the output folder correctly (e.g. `payment-capture-retry`).
- **Be specific about files or methods**: the more precise the scope, the deeper and more accurate the analysis.
- **State the change intent**: DEPRECATION, MODIFICATION, CLEANUP, or UNIFICATION helps the agent focus its analysis.
- **Include constraints**: "no schema breaking change", "must be feature-flagged", "zero downtime" all have direct impact on the recommendations.
- **Specify the output you need**: risk matrix, phased plan, rollback strategy, alignment score — tell the agent what you want.

---

## Where to Check the Report

Generated reports are saved at:

`ai-research-report/<feature-name>/<report-name>_v<version-number>.md`

Examples:

- `ai-research-report/payment-capture-retry/feature-enhancement-analysis_v1.md`
- `ai-research-report/password-reset/usecase-alignment-analysis_v2.md`

