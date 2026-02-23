# Field Knowledge

Purpose: Document domain terminology, business rules, data field definitions,
and validation constraints that agents must understand to produce accurate findings.
Populate this file with project-specific domain context to avoid repeated discovery.

## Domain Glossary

Define key business terms used in code, APIs, and documentation.

| Term | Definition | Common Code Identifiers |
|------|------------|------------------------|
| (term) | (plain-language definition) | (variable/class names where this appears) |

## Core Business Rules

List rules that are non-negotiable from a business perspective and that any
analysis must treat as invariants.

- (Rule ID) – (description of rule and where it applies)

## Key Data Fields

Document important domain fields including their valid values, constraints, and
any business significance that affects implementation decisions.

| Field Name | Entity / Table | Type | Valid Values / Constraints | Business Significance |
|------------|---------------|------|---------------------------|----------------------|
| (field)    | (entity)      | (type) | (constraints)           | (why it matters)     |

## Validation Rules

Capture explicit validation rules that apply to fields or operations.
Agents should flag any code that bypasses or weakens these rules.

- (field or operation): (validation rule and enforcement expectation)

## State Machines

For entities that transition through states, document the allowed transitions.

### (Entity Name)

- States: (list of valid states)
- Allowed transitions: (from-state) -> (to-state): (trigger/condition)
- Terminal states: (states from which no further transition is permitted)

## Compliance and Regulatory Notes

Record any regulatory or compliance requirements that constrain field handling,
storage, or transmission.

- (requirement): (description and affected fields/flows)
