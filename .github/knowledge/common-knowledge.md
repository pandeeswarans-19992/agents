# Common Knowledge

Purpose: Define shared knowledge applied by all agents regardless of analysis type.
All agents must load and apply this knowledge before executing any analysis.

## Architecture Principles

- Prefer explicit boundaries between modules over implicit coupling.
- Dependencies must flow in one direction: outer layers depend on inner layers, never the reverse.
- Side effects (DB writes, external calls, events) must be isolated and auditable.
- Every critical flow must have a documented failure path and rollback strategy.

## Design Pattern Expectations

- Prefer composition over inheritance for extensibility.
- Apply the single-responsibility principle at module and function level.
- Avoid god objects and oversized service classes.
- Use the repository pattern to isolate persistence from business logic.
- Flag observer/event patterns that lack error-handling guarantees.

## Data Integrity Standards

- Write operations touching more than one table must run inside a transaction.
- External API calls must not be placed inside open database transactions.
- All user-supplied input must be validated before reaching persistence or business logic.
- Sensitive data must not appear in logs or error messages.

## Security Baseline

- Authentication must be enforced at the entry point of every protected flow.
- Authorization checks must occur at the service layer, not only at the API layer.
- Secrets and credentials must never be hardcoded or committed.
- All deserialization of external input must be treated as untrusted.

## Observability Standards

- Critical operations must emit structured log entries with correlation identifiers.
- Errors must be categorized (transient vs permanent) and surfaced with enough context to reproduce.
- Performance-sensitive paths must have latency budgets documented or measurable.

## Evidence Requirements

- Every finding must cite at least one concrete file or code location.
- Confidence scores below 0.75 require explicit acknowledgement of ambiguity.
- Unverified assumptions must be labelled `[ASSUMPTION]` in findings.
- Missing evidence must be recorded as `Not Found in Scope`.
