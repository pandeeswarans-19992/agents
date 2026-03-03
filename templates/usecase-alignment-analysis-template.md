## USE_CASE_ALIGNMENT_ANALYSIS -- Analysis Steps Template

Purpose: Define the required case-specific research steps for USE_CASE_ALIGNMENT_ANALYSIS.
Use this with the report output template:
- .github/templates/usecase-alignment-report-template.md

## Case-Specific Required Steps

1. Atomic behavior extraction
- Decompose the use case into atomic expected behaviors.
- Identify explicit constraints and acceptance conditions.

2. Behavior-to-code mapping
- Map each expected behavior to concrete code components.
- Mark explicit absence where behavior is not implemented.

3. Runtime flow verification per behavior
- Trace execution for mapped behaviors.
- Validate actual runtime path against expected intent.

4. Coverage classification
- Classify each behavior as full, partial, missing, or unexpected.
- Capture evidence for every classification.

5. Gap severity and impact assessment
- Rank gaps by severity and business impact.
- Distinguish functional mismatch vs architectural mismatch.

6. Alignment score calculation basis
- Define reproducible scoring rationale.
- Explain confidence and uncertainty factors.

## Quality Gates

- Every expected behavior has evidence or explicit absence.
- Functional and architectural mismatches are separated.
- Alignment score rationale is reproducible.
