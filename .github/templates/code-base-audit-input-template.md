## CODEBASE_AUDIT -- Request Input Template

Purpose: Standard input format for submitting a CODEBASE_AUDIT request to the research agent.
Complete as many fields as possible to improve analysis accuracy and report quality.
Reference: .github/agents/research.agent.md

---

## Request Fields

- Goal:
  (Describe what you want the agent to audit, e.g. "Audit the payment module for architecture risks and deprecated patterns.")

- Feature / Use Case Name:
  (Short kebab-case name used as the output folder name, e.g. `order-processing`.)

- Scope In:
  (List file paths, modules, or layers that must be included in the audit.)

- Scope Out:
  (List file paths, modules, or layers that must be excluded from the audit.)

- Specific Files / Methods:
  (List any specific files or method signatures to focus the audit on, e.g. `src/payments/capture.js::processCapture`.)

- Change Intent:
  (Select one or more: DEPRECATION | MODIFICATION | CLEANUP | UNIFICATION | DISCOVERY_ONLY)
  (Use DEPRECATION when identifying code to be removed or phased out.)
  (Use MODIFICATION when assessing impact of planned structural changes.)
  (Use CLEANUP when targeting dead code, unused dependencies, or technical debt.)
  (Use UNIFICATION when consolidating duplicate or diverged implementations.)
  (Use DISCOVERY_ONLY when performing a neutral audit with no change plan yet.)

- Audit Focus:
  (Select one or more: ARCHITECTURE | SECURITY | PERFORMANCE | MAINTAINABILITY | ALL)

- Known Risk Areas:
  (List any areas you already suspect are problematic, e.g. circular dependencies, large classes.)

- Constraints:
  (Security, performance, backward compatibility, schema-breaking, time-box, etc.)

- Expected Output:
  (Describe what deliverables you need, e.g. risk matrix, maturity level, dependency map, roadmap.)

---

## Knowledge References

The agent will automatically load the following shared knowledge files.
You do not need to duplicate this information in your request.

- Common knowledge:   .github/knowledge/common-knowledge.md
- Platform knowledge: .github/knowledge/platform-knowledge.md
- Module knowledge:   .github/knowledge/module-knowledge.md
- Field knowledge:    .github/knowledge/field-knowledge.md

---

## Input Examples

### Deprecation audit

Goal: Identify all deprecated API methods in the payments module and assess removal impact.
Feature / Use Case Name: payments-deprecation-cleanup
Scope In: `src/payments`
Scope Out: tests, docs
Specific Files / Methods: `src/payments/legacy-api.js`, `src/payments/v1/`
Change Intent: DEPRECATION
Audit Focus: ARCHITECTURE, MAINTAINABILITY
Expected Output: deprecated symbol inventory, call-site impact map, removal sequence

### Architecture cleanup

Goal: Audit order-processing module for circular dependencies and dead code.
Feature / Use Case Name: order-processing-cleanup
Scope In: `src/orders`, `src/payments`, `db/migrations`
Scope Out: tests, docs
Change Intent: CLEANUP
Audit Focus: ARCHITECTURE
Known Risk Areas: suspected circular dependency between orders and payments
Expected Output: dependency graph, dead-code list, risk matrix, recommended refactor order

### Module unification

Goal: Assess feasibility of merging the two notification service implementations.
Feature / Use Case Name: notification-unification
Scope In: `src/notifications/v1`, `src/notifications/v2`
Change Intent: UNIFICATION
Audit Focus: ARCHITECTURE, MAINTAINABILITY
Expected Output: behavioral diff, shared interface proposal, migration risk, phased plan
