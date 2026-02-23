## Research Agent -- Request Input Template

Purpose: Standard input format for submitting requests to the research agent.
Complete as many fields as possible to improve classification accuracy and report quality.
Reference: .github/agents/research.agent.md

---

## Request Fields

- Goal:
  (Describe what you want the agent to investigate or produce.)

- Analysis Type (optional):
  (One of: CODEBASE_AUDIT | NEW_FEATURE_ANALYSIS | FEATURE_ENHANCEMENT_ANALYSIS | USE_CASE_ALIGNMENT_ANALYSIS | HYBRID_ANALYSIS)
  (Leave blank to let the agent classify automatically.)

- Feature / Use Case Name:
  (Short kebab-case name used as the output folder name, e.g. `payment-capture-retry`.)

- Scope In:
  (List file paths, modules, or layers that must be included in the analysis.)

- Scope Out:
  (List file paths, modules, or layers that must be excluded from the analysis.)

- Known Files / Modules:
  (List any specific files or modules you already know are relevant.)

- Constraints:
  (Security, performance, backward compatibility, schema-breaking, time-box, etc.)

- Expected Output:
  (Describe what deliverables you need, e.g. risk matrix, architecture diagram, phased plan.)

---

## Minimal Input Examples by Analysis Type

### CODEBASE_AUDIT

Goal: Audit architecture and execution risks.
Feature / Use Case Name: order-processing
Scope In: `src/orders`, `src/payments`, `db/migrations`
Scope Out: tests, docs
Expected Output: risk matrix, maturity level, roadmap

### NEW_FEATURE_ANALYSIS

Goal: Analyze implementation strategy for bulk invoice export.
Feature / Use Case Name: bulk-invoice-export
Known Files / Modules: `src/invoice`, `src/reporting`, `api/openapi.yaml`
Constraints: Keep backward compatibility for current invoice APIs.
Expected Output: architecture insertion points, API/schema delta, phased plan

### FEATURE_ENHANCEMENT_ANALYSIS

Goal: Improve retry behavior in payment capture flow.
Feature / Use Case Name: payment-capture-retry
Scope In: `src/payments/capture*`, queue workers
Constraints: No schema breaking change.
Expected Output: impact surface, regression risks, rollback strategy

### USE_CASE_ALIGNMENT_ANALYSIS

Goal: Verify password-reset flow against use case document.
Feature / Use Case Name: password-reset
Known Files / Modules: `src/auth`, `src/notification`
Constraints: Compliance and audit logging required.
Expected Output: behavior-to-code mapping, coverage gaps, alignment score

---

