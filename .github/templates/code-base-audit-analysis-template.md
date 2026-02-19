## CODEBASE_AUDIT -- Analysis Steps Template

Purpose: Define the required case-specific research steps for CODEBASE_AUDIT.
Use this with the report output template:
- .github/templates/code-base-audit-report-template.md

## Case-Specific Required Steps

1. Module and layer inventory
- Identify top-level modules and ownership boundaries.
- Confirm layer responsibilities and coupling points.

2. Dependency direction and circularity checks
- Validate dependency flow direction.
- Detect circular dependencies and high-risk coupling chains.

3. Critical flow tracing
- Trace top-priority business flows from trigger to persistence/response.
- Capture control handoffs and side effects.

4. Persistence and transaction-safety analysis
- Identify transaction boundaries.
- Verify integrity guarantees and failure behavior.

5. Scalability bottleneck identification
- Detect throughput, concurrency, and resource hotspots.
- Identify growth constraints tied to architecture.

6. Architecture maturity assessment
- Classify maturity level and justify with evidence.

## Quality Gates

- Include at least one entry-point trace per major module.
- Include at least one persistence-path trace for each critical flow.
- Explicitly note constraints that block scale, safety, or maintainability.
