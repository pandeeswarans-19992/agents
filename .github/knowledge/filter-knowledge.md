# Filter Knowledge

Purpose: Define what the Filter API is, how fields become filterable, the predicate
model, the MySQL schema that controls field filter visibility, and the rules agents
must apply when diagnosing filter API behaviour or suggesting filtering strategies.
Agents must load this file alongside `field-knowledge.md` and `module-knowledge.md`
whenever a task involves the Filter API.

---

## What Is the Filter API?

The **Filter API** is a platform-level query interface that lets callers retrieve
module records matching one or more field-level conditions called **predicates**.
A single Filter API request may combine multiple predicates joined by logical
operators (`AND` / `OR`).

Key characteristics:

- Every filterable field in a module is addressable by its `field_name`.
- Each field supports a fixed set of comparison operators determined by its field type.
- Only fields explicitly marked as filterable in the database appear in Filter API
  responses and are accepted as predicate targets.
- Fields that are hidden, disabled, or not marked filterable are silently excluded;
  no error is raised for a missing field in a filter response listing.

---

## Filter API Request Structure

```
GET /filter/{module}?predicate=<field_name>+<operator>+<value>[&predicate=...]&logic=AND|OR
```

| Parameter   | Description |
|-------------|-------------|
| `module`    | Module API name (e.g. `doctor`, `patient`, `payment`) |
| `predicate` | One or more `field_name operator value` conditions |
| `logic`     | `AND` (default) or `OR` to join multiple predicates |
| `fields`    | Comma-separated list of field names to return in the response |
| `page`      | 1-based page number for pagination |
| `per_page`  | Records per page (default 20, max 200) |

---

## Predicate Operators by Field Type

The set of valid comparison operators depends on the logical field type.
Agents must use this table when suggesting or validating filter predicates.

| Field Type | Supported Operators                          | Notes |
|------------|----------------------------------------------|-------|
| long       | `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `in`, `not_in` | Includes PK and FK fields |
| number     | `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `in`, `not_in` | |
| boolean    | `eq`, `ne`                                   | Value must be `true` or `false` |
| singleline | `eq`, `ne`, `contains`, `starts_with`, `ends_with`, `in`, `not_in` | Case-insensitive by default |
| textarea   | `contains`                                   | Full-text style; expensive on large tables |
| picklist   | `eq`, `ne`, `in`, `not_in`                   | Value must match a valid `picklist_value.value_key` |

Operators not in the list above are rejected with a `400 Bad Request`.

---

## Field Filter Properties (MySQL)

### Table: `CrmField`

Each row in the `CrmField` table represents one field belonging to a module.
The columns relevant to Filter API behaviour are:

| Column              | Type            | Description |
|---------------------|-----------------|-------------|
| `FIELDID`           | BIGINT(19) PK   | Surrogate key |
| `MODULEID`          | BIGINT(19) FK   | References `ZD_Modules.MODULEID` |
| `APINAME`           | VARCHAR(255)    | API-level name used in predicates |
| `UITYPE`            | INT(10)         | Numeric UI type that determines valid filter operators |
| `PRESENCE`          | BIGINT(19)      | `1` = field is active/present; `0` = field is inactive (excluded from Filter API) |
| `ISPRESENCE`        | TINYINT(1)      | `1` = field is present in the Filter API response; `0` = field is hidden from the filter listing |
| `SHOWTYPE`          | INT(10)         | Bitmask controlling where the field is shown (default `7` = all contexts); filter visibility requires the filter bit to be set |
| `IS_INTERNAL_STATE` | TINYINT(1)      | `1` = internal state field; excluded from Filter API by default |
| `IS_COMPUTED`       | TINYINT(1)      | `1` = computed field; cannot be used in filter predicates |
| `IS_BASIC`          | TINYINT(1)      | `1` = basic/system field |
| `ISMANDATORY`       | TINYINT(1)      | `1` = required on record creation; does not affect filter visibility |

### Table: `ZD_Modules`

| Column       | Type           | Description |
|--------------|----------------|-------------|
| `MODULEID`   | BIGINT(19) PK  | Surrogate key |
| `NAME`       | VARCHAR(255)   | Module display name |
| `SYSTEMNAME` | VARCHAR(255)   | System/API name used in Filter API URLs |
| `PRESENCE`   | TINYINT(4)     | `1` = module is active; `0` = module is disabled globally |
| `SHOWTYPE`   | TINYINT(4)     | Bitmask controlling module visibility |

---

## Why a Field May Not Appear in the Filter API

Use this checklist when diagnosing field visibility issues.
Agents must walk through all conditions before concluding a root cause.

| # | Condition | Diagnostic Query | Resolution |
|---|-----------|-----------------|------------|
| 1 | `CrmField.PRESENCE = 0` | `SELECT PRESENCE FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | Field is inactive; re-activate or use a replacement field |
| 2 | `CrmField.ISPRESENCE = 0` | `SELECT ISPRESENCE FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | Field is not present in Filter API; enable ISPRESENCE after platform review |
| 3 | `CrmField.SHOWTYPE` filter bit not set | `SELECT SHOWTYPE FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | SHOWTYPE bitmask does not include filter visibility; update after platform review |
| 4 | `ZD_Modules.PRESENCE = 0` | `SELECT PRESENCE FROM ZD_Modules WHERE SYSTEMNAME = ?` | Module is globally disabled |
| 5 | `CrmField.IS_INTERNAL_STATE = 1` | `SELECT IS_INTERNAL_STATE FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | Internal state field; excluded from Filter API by design |
| 6 | `CrmField.IS_COMPUTED = 1` | `SELECT IS_COMPUTED FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | Computed field; cannot be used in filter predicates |
| 7 | Operator not supported for UITYPE | Check `CrmField.UITYPE` vs operator used in predicate | Use a supported operator from the table above |

---

## Filtering Strategies

Agents must recommend the appropriate strategy based on the use case.

### Strategy 1 — Exact Match Filter

Use when: the predicate value must equal a stored value exactly.
Best for: `long` (ID lookups), `boolean` flags, `picklist` controlled vocabularies.

```
predicate=specialist+eq+Cardiology
```

### Strategy 2 — Range Filter

Use when: the query targets a numeric or identifier range.
Best for: `number`, `long` date-encoded timestamps.

```
predicate=age+gte+30&predicate=age+lte+60&logic=AND
```

### Strategy 3 — Text Search Filter

Use when: the caller needs partial text matching.
Best for: `singleline` fields; avoid `textarea` on large tables unless indexed.

```
predicate=name+contains+Smith
```

### Strategy 4 — Set Filter

Use when: the caller wants to match any value from a known set.
Best for: `picklist`, `long` FK fields, `singleline` with a known enumeration.

```
predicate=specialist+in+Cardiology,Neurology,Orthopedics
```

### Strategy 5 — Compound Filter

Use when: multiple conditions must all be true (AND) or any one can be true (OR).
Best for: search screens combining status + category + text filters.

```
predicate=is_active+eq+true&predicate=specialist+eq+Cardiology&logic=AND
```

### Strategy Selection Guide

| Use Case Pattern | Recommended Strategy |
|-----------------|---------------------|
| Find record by ID or FK reference | Strategy 1 (Exact Match) |
| Date or numeric range search | Strategy 2 (Range) |
| Partial name / keyword search | Strategy 3 (Text Search) |
| Dropdown multi-select filter | Strategy 4 (Set Filter) |
| Multi-criteria search form | Strategy 5 (Compound) |
| Status + category dashboard filter | Strategy 5 (Compound) |

---

## MySQL Diagnostic Query Templates

Agents must use these parameterised templates when executing diagnostic queries.
Always replace `?` with the actual module API name or field name from the user request.
Never expose credentials in reports; reference them from the environment config only.

### Q-01 — Resolve MODULEID from SYSTEMNAME

```sql
SELECT MODULEID, NAME, SYSTEMNAME, PRESENCE
FROM ZD_Modules
WHERE SYSTEMNAME = ?;
```

### Q-02 — Check all filter properties for a specific field

```sql
SELECT f.FIELDID, f.APINAME, f.UITYPE,
       f.PRESENCE, f.ISPRESENCE, f.SHOWTYPE,
       f.IS_INTERNAL_STATE, f.IS_COMPUTED
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND f.APINAME = ?;
```

### Q-03 — List all present/active fields for a module

```sql
SELECT f.APINAME, f.UITYPE,
       f.PRESENCE, f.ISPRESENCE, f.SHOWTYPE,
       f.IS_INTERNAL_STATE, f.IS_COMPUTED
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND f.PRESENCE = 1
  AND f.ISPRESENCE = 1
ORDER BY f.APINAME;
```

### Q-04 — List inactive/hidden fields for a module

```sql
SELECT f.APINAME, f.UITYPE,
       f.PRESENCE, f.ISPRESENCE, f.SHOWTYPE
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND (f.PRESENCE = 0 OR f.ISPRESENCE = 0)
ORDER BY f.APINAME;
```

### Q-05 — List internal state and computed fields for a module

```sql
SELECT f.APINAME, f.UITYPE,
       f.IS_INTERNAL_STATE, f.IS_COMPUTED, f.PRESENCE
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND (f.IS_INTERNAL_STATE = 1 OR f.IS_COMPUTED = 1)
ORDER BY f.APINAME;
```

---

## MySQL Credential Configuration

Credentials must never be hardcoded. The agent must resolve them from environment
configuration using the following keys:

| Config Key              | Description |
|-------------------------|-------------|
| `DB_HOST`               | MySQL server hostname or IP |
| `DB_PORT`               | MySQL port (default `3306`) |
| `DB_NAME`               | Target database name |
| `DB_USER`               | Read-only service account username |
| `DB_PASSWORD`           | Service account password (never logged or written to chat output) |

The agent must request these credentials from the user or environment if they are
not already available in the session context. The password must be used only for
the diagnostic query execution tool call and must not appear in any chat output.

---

## MCP Server Integration — Fields Team Support Chat

The MCP (Message Channel Protocol) server integration is used **only for escalation**:
when the Filter API agent cannot resolve the user query, the user contacts the module
owner and that process posts the unresolved query to the Fields team support chat via
the OAuth-authenticated MCP server.

### Authentication

Authentication is handled via **OAuth**. The agent must obtain and use an OAuth token
to authenticate with the MCP server. The token must never be logged or written to any
chat output or escalation message body.

| Config Key          | Description |
|---------------------|-------------|
| `MCP_SERVER_URL`    | Base URL of the MCP server |
| `MCP_OAUTH_TOKEN`   | OAuth access token for authenticating with the MCP server |
| `MCP_CHAT_ID`       | Target group chat identifier for the Fields team support chat |

Authentication header:

```
Authorization: Bearer <MCP_OAUTH_TOKEN>
```

The agent must validate that `MCP_OAUTH_TOKEN` and `MCP_CHAT_ID` are available before
attempting any message post. If either is missing, inform the user and stop the
escalation step.

### Escalation Message Contract

```
POST <MCP_SERVER_URL>/chats/<MCP_CHAT_ID>/messages
Authorization: Bearer <MCP_OAUTH_TOKEN>
Content-Type: application/json

{
  "type": "filter_api_unresolved_query",
  "module": "<module_api_name>",
  "field": "<field_name — set to null when not field-specific>",
  "unresolved_query": "<the user query or question that the agent could not resolve>",
  "context": "<relevant context collected during the agent session>",
  "timestamp": "<ISO-8601 UTC timestamp>"
}
```

The `unresolved_query` and `context` fields must not include database passwords or
OAuth tokens. Include only the information needed for the module owner to understand
and respond to the query.

### MCP Escalation Rules

- Use the MCP channel only when the agent cannot resolve the user query.
- Do not post intermediate diagnostic results or successful findings to MCP.
- If the MCP post fails (non-2xx response), inform the user of the failure; do not
  retry more than once.
- Post once per escalation; do not send multiple messages for the same unresolved query.
