## NEW_FEATURE_ANALYSIS -- Request Input Template

Purpose: Standard input format for submitting a NEW_FEATURE_ANALYSIS request to the research agent.
Complete as many fields as possible to improve analysis accuracy and report quality.
Reference: .github/agents/research.agent.md

---

## Request Fields

- Goal:
  (Describe the feature to be implemented, e.g. "Analyze implementation strategy for bulk invoice export.")

- Feature / Use Case Name:
  (Short kebab-case name used as the output folder name, e.g. `bulk-invoice-export`.)

- Use Case Document / Requirements:
  (Paste the use case description inline or provide a file path, e.g. `docs/use-cases/bulk-export.md`.)

- Target Modules / Layers:
  (List the modules or layers where the feature is expected to land, e.g. `src/invoice`, `src/reporting`.)

- Scope Out:
  (List file paths, modules, or layers that must be excluded from the analysis.)

- Known Files / Modules:
  (List any specific files or modules you already know are relevant, e.g. `api/openapi.yaml`.)

- API Contracts:
  (Describe or reference existing API contracts that this feature must conform to or extend.)

- Schema / Data Model Constraints:
  (List database tables, entity relationships, or data-model boundaries relevant to this feature.)

- Backward Compatibility Requirements:
  (State whether existing APIs or data structures must remain unchanged, e.g. "Keep backward compatibility for v1 invoice API.")

- Constraints:
  (Security, performance, compliance, time-box, or other non-functional requirements.)

- Expected Output:
  (Describe what deliverables you need, e.g. architecture insertion points, API/schema delta, phased plan.)

---

## Input Examples

### Standard new feature

Goal: Analyze implementation strategy for bulk invoice export.
Feature / Use Case Name: bulk-invoice-export
Use Case Document / Requirements: Users must be able to export up to 10,000 invoices as a single CSV or PDF. Export jobs must be async and notify the user by email on completion.
Target Modules / Layers: `src/invoice`, `src/reporting`
Known Files / Modules: `api/openapi.yaml`, `src/jobs/`
API Contracts: Must not change existing GET /invoices response shape.
Schema / Data Model Constraints: invoice table has 50 M rows; avoid full-table scans.
Backward Compatibility Requirements: Keep backward compatibility for current invoice APIs.
Constraints: Max response time for job submission 200 ms. No new infrastructure dependencies.
Expected Output: architecture insertion points, API/schema delta, phased implementation plan

### Feature with compliance requirement

Goal: Implement multi-factor authentication for admin users.
Feature / Use Case Name: admin-mfa
Use Case Document / Requirements: All admin logins must require a TOTP second factor. Recovery codes must be generated on enrollment.
Target Modules / Layers: `src/auth`, `src/admin`
Backward Compatibility Requirements: Existing session tokens must remain valid through the migration.
Constraints: OWASP compliance, no storage of plaintext secrets.
Expected Output: insertion point analysis, schema delta, security review checklist, rollout phases
