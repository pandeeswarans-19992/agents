## FILTER API AGENT — Request Input Template

Purpose: Standard input format for submitting any request to the Filter API agent.
Complete the section that matches your request type. Leave irrelevant sections blank.
Reference: `.github/agents/filter-api.agent.md`

---

## Request Type

Select one:
- [ ] FILTER_SUGGESTION — I have a use case and want the agent to recommend Filter API predicates and strategies.
- [ ] FIELD_VISIBILITY_DEBUG — I want to know why a specific field appears or does not appear in the Filter API.
- [ ] FILTER_FIELD_LISTING — I want a full inventory of filterable fields for a module.

---

## Section A — Common Fields (all request types)

- Module API Name:
  (The module's API-level name as used in Filter API URLs, e.g. `doctor`, `patient`, `payment`.)

- Expected Output:
  (Describe the deliverable you need, e.g. example predicates and URL, root cause analysis, filterable field list.)

---

## Section B — FILTER_SUGGESTION Fields

- Use Case / Search Requirement:
  (Describe the search or filter requirement in natural language.
   Example: "Find all active doctors specialising in Cardiology whose name starts with 'Dr.'")

- Known Fields to Filter On:
  (List any field names you already know are relevant, e.g. `specialist`, `name`, `is_active`.)

- Performance / Scale Constraints:
  (State any performance requirements, e.g. "table has 5 M rows; avoid full-table scans".)

- Backward Compatibility Requirements:
  (State whether existing Filter API callers must not be broken, e.g. "existing predicates must continue to work".)

---

## Section C — FIELD_VISIBILITY_DEBUG Fields

- Field Name:
  (Exact field name that is missing or unexpected in the Filter API response, e.g. `specialist`.)

- Predicate Attempted (optional):
  (The predicate the user tried that failed or returned unexpected results,
   e.g. `specialist+eq+Cardiology`.)

- Observed Behaviour:
  (What the Filter API actually returned, e.g. "field not found in field listing", "predicate rejected with 400".)

- Expected Behaviour:
  (What the Filter API should have done, e.g. "specialist should be filterable with eq and in operators".)

- MySQL Credentials:
  (Resolve from environment. If prompting: provide DB_HOST, DB_PORT, DB_NAME, DB_USER.
   Never include DB_PASSWORD in this template — supply it securely at runtime.)

- MCP Notification:
  (Should the agent post findings to the Fields team chat? yes / no.
   If yes: confirm MCP_SERVER_URL, MCP_AUTH_TOKEN, MCP_CHAT_ID are available in environment.)

---

## Section D — FILTER_FIELD_LISTING Fields

- Include Non-Filterable Fields:
  (yes / no — whether to also list active fields that are currently not filterable.)

- MySQL Credentials:
  (Same as Section C.)

- MCP Notification:
  (yes / no. Same as Section C.)

---

## Input Examples

### Example 1 — FILTER_SUGGESTION

```
Request Type: FILTER_SUGGESTION
Module API Name: doctor
Use Case: Find all active doctors specialising in Cardiology or Neurology whose
          name contains 'Singh', ordered by name.
Known Fields to Filter On: specialist, name, is_active
Performance Constraints: doctor table has 2 M rows; name is indexed.
Expected Output: example predicate URL, recommended strategy, risk notes
```

### Example 2 — FIELD_VISIBILITY_DEBUG

```
Request Type: FIELD_VISIBILITY_DEBUG
Module API Name: patient
Field Name: date_of_birth
Predicate Attempted: date_of_birth+gte+19900101
Observed Behaviour: Field 'date_of_birth' is not listed in the Filter API field response.
Expected Behaviour: date_of_birth should be filterable with gte, lte, eq operators.
MySQL Credentials: resolve from environment (DB_HOST, DB_PORT, DB_NAME, DB_USER)
MCP Notification: yes
Expected Output: root cause analysis, resolution SQL for DBA, MCP post confirmation
```

### Example 3 — FILTER_FIELD_LISTING

```
Request Type: FILTER_FIELD_LISTING
Module API Name: payment
Include Non-Filterable Fields: yes
MySQL Credentials: resolve from environment
MCP Notification: no
Expected Output: full field inventory with supported operators per field
```
