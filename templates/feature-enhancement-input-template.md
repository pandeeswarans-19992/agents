## FEATURE_ENHANCEMENT_ANALYSIS -- Request Input Template

Purpose: Standard input format for submitting a FEATURE_ENHANCEMENT_ANALYSIS request to the research agent.
Complete as many fields as possible to improve analysis accuracy and report quality.
Reference: .github/agents/research.agent.md

---

## Request Fields

- Goal:
  (Describe what you want to improve or change, e.g. "Improve retry behavior in payment capture flow.")

- Feature / Use Case Name:
  (Short kebab-case name used as the output folder name, e.g. `payment-capture-retry`.)

- Enhancement Type:
  (Select one or more: DEPRECATION | MODIFICATION | CLEANUP | UNIFICATION)
  (Use DEPRECATION when removing or phasing out existing behavior.)
  (Use MODIFICATION when altering logic, contracts, or structure of existing behavior.)
  (Use CLEANUP when removing dead code, unused config, or accumulated technical debt.)
  (Use UNIFICATION when merging diverged or duplicated implementations into one.)
  (Multiple values are allowed when the work spans more than one intent, e.g. MODIFICATION, CLEANUP.)

- Specific Files / Methods:
  (List the exact files or method signatures that are the primary target of the enhancement,
   e.g. `src/payments/capture.js::processCapture`, `src/jobs/retry-worker.js`.)

- Scope In:
  (List file paths, modules, or layers that must be included in the analysis.)

- Scope Out:
  (List file paths, modules, or layers that must be excluded from the analysis.)

- Current Behavior:
  (Briefly describe what the code does today, e.g. "Retries up to 3 times with fixed 1 s delay, no dead-letter queue.")

- Desired Change:
  (Briefly describe what the code should do after the enhancement, e.g. "Exponential back-off, max 5 retries, DLQ on final failure.")

- Migration Constraints:
  (State any constraints on the transition, e.g. "No schema breaking change", "Must be feature-flagged", "Zero downtime.")

- Rollback Requirements:
  (Describe what a safe rollback looks like, e.g. "Must be reversible by disabling feature flag without data loss.")

- Constraints:
  (Security, performance, backward compatibility, compliance, time-box, etc.)

- Expected Output:
  (Describe what deliverables you need, e.g. impact surface, regression risks, rollback strategy, phased plan.)

---

## Input Examples

### Behavior modification

Goal: Improve retry behavior in payment capture flow.
Feature / Use Case Name: payment-capture-retry
Enhancement Type: MODIFICATION
Specific Files / Methods: `src/payments/capture.js::processCapture`, `src/jobs/retry-worker.js`
Scope In: `src/payments/capture*`, queue workers
Scope Out: UI, reporting
Current Behavior: Retries up to 3 times with fixed 1 s delay; no dead-letter queue on final failure.
Desired Change: Exponential back-off with jitter, max 5 retries, route to DLQ after final failure.
Migration Constraints: No schema breaking change; must be feature-flagged.
Rollback Requirements: Disable feature flag reverts to current behavior without data loss.
Constraints: No schema breaking change. P99 latency must not increase.
Expected Output: impact surface, regression risks, rollback strategy, phased rollout plan

### Deprecation of legacy method

Goal: Remove the legacy synchronous payment processing path.
Feature / Use Case Name: legacy-sync-payment-removal
Enhancement Type: DEPRECATION
Specific Files / Methods: `src/payments/sync-processor.js`, `src/api/v1/payment.js::syncCharge`
Scope In: `src/payments`, `src/api/v1`
Current Behavior: Synchronous charge endpoint still active and used by two internal consumers.
Desired Change: Route all consumers to async endpoint, then remove sync path entirely.
Migration Constraints: Internal consumers must be migrated before removal. No external API break.
Rollback Requirements: Consumer migration must be individually reversible.
Expected Output: call-site inventory, consumer migration plan, removal sequence, regression checklist

### Code cleanup

Goal: Remove dead feature-flag checks for flags retired over 6 months ago.
Feature / Use Case Name: retired-flag-cleanup
Enhancement Type: CLEANUP
Scope In: `src/`, `config/`
Specific Files / Methods: Any file referencing `LEGACY_CHECKOUT_V1`, `OLD_PRICING_ENGINE`
Current Behavior: Dead code branches guarded by always-false flags bloat several critical-path methods.
Desired Change: Delete the flag references and unreachable branches.
Migration Constraints: Confirm flags are permanently disabled in all environments before removal.
Expected Output: affected file list, safe deletion sequence, test coverage gap analysis

### Combined modification and cleanup

Goal: Refactor the pricing engine to use the new strategy pattern and remove legacy override logic.
Feature / Use Case Name: pricing-engine-refactor
Enhancement Type: MODIFICATION, CLEANUP
Specific Files / Methods: `src/pricing/engine.js`, `src/pricing/legacy-overrides.js`
Scope In: `src/pricing`
Current Behavior: Engine has both new strategy-based path and old override-based path running in parallel under a feature flag.
Desired Change: Remove the feature flag, delete the legacy path, and ensure all callers use the strategy-based path.
Migration Constraints: Feature flag must be permanently enabled in all environments before cleanup. No schema changes.
Rollback Requirements: Revert commits; flag re-enable is not sufficient after cleanup.
Expected Output: impact surface, removal sequence, regression risk list, phased plan
