## FIELD FILTER API ASSISTANT — Request Input Template

Purpose: Standard input format for submitting any request to the Field Filter API Assistant.
Complete the section that matches your request type. Leave irrelevant sections blank.
Reference: `.github/agents/field-filter-api-assistant.agent.md`

---

## Request Type

Select one:
- [ ] FILTER_SUGGESTION — I have a use case and want the agent to recommend the right Filter API.
- [ ] FIELD_VISIBILITY_DEBUG — I want to know why a specific field appears or does not appear in the Filter API.
- [ ] FILTER_FIELD_LISTING — I want to query filterable fields for a module.
- [ ] HYBRID — My request clearly combines more than one of the above types (describe both needs in the relevant sections below).

---

## Section A — Common Fields (all request types)

- Module API Name:
  (The module's API-level name, e.g. `doctor`, `patient`, `payment`.)

---

## Section B — FILTER_SUGGESTION Fields

- Use Case:
  (Describe the goal or use case in natural language.
   Example: "I want to display fields in a form area for the doctor module.")

---

## Section C — FIELD_VISIBILITY_DEBUG Fields

- Field Name:
  (Exact field name that is missing or unexpected in the Filter API response, e.g. `specialist`.)

- Predicate (required):
  (The predicate the user tried, e.g. `specialist+eq+Cardiology`.)

- MySQL Credentials:
  (Resolve from environment: DB_HOST, DB_PORT, DB_NAME, DB_USER.
   Never include DB_PASSWORD in this template — supply it securely at runtime.)

---

## Section D — FILTER_FIELD_LISTING Fields

- Filter to Apply (optional):
  (Provide a predicate or MySQL query to filter results, e.g. `is_filterable+eq+1`.
   If a MySQL query is provided directly, the agent will execute it without conversion.)

- MySQL Credentials:
  (Same as Section C.)

---

## Input Examples

### Example 1 — FILTER_SUGGESTION

```
Request Type: FILTER_SUGGESTION
Module API Name: doctor
Use Case: I want to display fields in a form area for the doctor module.
```

### Example 2 — FIELD_VISIBILITY_DEBUG

```
Request Type: FIELD_VISIBILITY_DEBUG
Module API Name: patient
Field Name: date_of_birth
Predicate: date_of_birth+gte+19900101
MySQL Credentials: resolve from environment (DB_HOST, DB_PORT, DB_NAME, DB_USER)
```

### Example 3 — FILTER_FIELD_LISTING

```
Request Type: FILTER_FIELD_LISTING
Module API Name: payment
Filter to Apply: is_filterable+eq+1
MySQL Credentials: resolve from environment
```
