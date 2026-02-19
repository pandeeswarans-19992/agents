## FEATURE_ENHANCEMENT_ANALYSIS -- Analysis Steps Template

Purpose: Define the required case-specific research steps for FEATURE_ENHANCEMENT_ANALYSIS.
Use this with the report output template:
- .github/templates/feature-enhancement-report-template.md

## Case-Specific Required Steps

1. Baseline current-behavior trace
- Trace existing behavior from entry to persistence/response.
- Record known constraints and dependencies.

2. Change-delta definition
- Separate add/modify/retain behaviors clearly.
- Identify unchanged behavior requiring regression protection.

3. Impact-surface mapping
- Map impacted code paths, APIs, DB tables, configs, and integrations.
- Highlight dependency and boundary effects.

4. Regression-risk and boundary validation
- Identify likely breakage areas.
- Validate boundary compliance after enhancement.

5. Migration/versioning/feature-flag strategy
- Define versioning/flag approach if needed.
- Define compatibility and transition strategy.

6. Rollback and stability validation
- Specify rollback preconditions and fallback path.
- Verify operational safety under partial failure.

## Quality Gates

- Unchanged vs changed behavior is explicitly separated.
- Contract break risks are identified before recommendations.
- Rollback path is concrete and testable.
