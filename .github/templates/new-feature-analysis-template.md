## NEW_FEATURE_ANALYSIS -- Analysis Steps Template

Purpose: Define the required case-specific research steps for NEW_FEATURE_ANALYSIS.
Use this with the report output template:
- .github/templates/new-feature-analysis-report-template.md

## Case-Specific Required Steps

1. Use-case decomposition
- Decompose actors, triggers, constraints, and edge cases.
- Separate functional and non-functional requirements.

2. Architecture insertion-point identification
- Identify best-fit modules/layers for new behavior.
- Validate boundary and dependency direction impact.

3. Contract/API/schema delta definition
- Define new or changed API contracts.
- Define schema/data model implications and compatibility boundaries.

4. Reuse vs new-component decisions
- Assess reusable components and their limits.
- Justify where new components are required.

5. Migration and backward-compatibility strategy
- Define migration sequence and compatibility approach.
- Identify rollout constraints and data transition risks.

6. Phased implementation planning
- Provide staged implementation order.
- Include verification checkpoints per phase.

## Quality Gates

- Existing components are classified as reusable or insufficient with rationale.
- Contract changes preserve backward compatibility boundaries or explicitly justify breaks.
- Rollout sequence minimizes operational and integration risk.
