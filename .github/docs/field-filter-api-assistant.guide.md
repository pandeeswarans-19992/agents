# Field Filter API Assistant Guide

Example queries and configuration instructions for `.github/agents/field-filter-api-assistant.agent.md`.
This guide shows how to phrase requests to get the best output from the Field Filter API Assistant.

---

## What the Filter API Agent Can Do

| Capability | Description |
|---|---|
| Filter Suggestion | Understand a use case and recommend which Filter API to use |
| Field Visibility Debug | Diagnose why a specific field appears or does not appear in the Filter API |
| Field Listing / Query | Execute a MySQL query for a module's fields and display results as a table |
| MCP Escalation | When the agent cannot resolve a query, escalate to the module owner via OAuth-authenticated MCP support chat |

---

## FILTER_SUGGESTION — Example Queries

> "I need to display fields in a form area for the doctor module. Which API should I use?"

> "We want to show patient records in a list view. What Filter API is recommended?"

> "Which API should I use to build a search screen for payments?"

**Agent output format:**
```
Output:
Suggest API: LayoutFieldAPI
Reason: You will display the fields in the form area so that you must use the LayoutFieldAPI
```

---

## FIELD_VISIBILITY_DEBUG — Example Queries

> "The field `specialist` on the `doctor` module isn't showing up when I use the predicate
> `specialist+eq+Cardiology`. Can you find out why?"

> "I tried the predicate `date_of_birth+gte+19900101` on the `patient` module but the field
> is not in the Filter API response. What's the reason?"

> "Why is the `notes` field on the `payment` module not filterable?
> My predicate was `notes+contains+urgent`."

**Agent output format:**
```
That field data:
< field record from MySQL >

MySQL query from the predicate:
< constructed SQL query >

Reason:
< which condition > — this condition is the reason the field is shown or hidden
```

---

## FILTER_FIELD_LISTING — Example Queries

> "Show me all fields for the `doctor` module where `ISPRESENCE = 1`."

> "I want to apply the predicate `PRESENCE+eq+1` on the `patient` module — show me the results."

> "Run this MySQL query for me: SELECT FIELDID, APINAME, PRESENCE, ISPRESENCE FROM CrmField WHERE MODULEID = 5 AND ISPRESENCE = 1"

**Agent output:** Results are printed as a markdown table in the chat window.

---

## Providing Inputs

Use the input template at `.github/templates/field-filter-api-assistant-input-template.md` for structured requests.

Minimum required inputs per request type:

| Request Type | Required |
|---|---|
| FILTER_SUGGESTION | module API name, use case description |
| FIELD_VISIBILITY_DEBUG | module API name, field name, predicate, MySQL credentials (from env) |
| FILTER_FIELD_LISTING | module API name, MySQL credentials (from env) |

### Tips for Better Queries

- **Name the module**: always include the module's API-level name (e.g. `doctor`, not `Doctor`).
- **Describe the use case goal**: for Filter Suggestion, state what you want to achieve
  (e.g. "display fields in a form", "build a search screen") — not which fields to filter.
- **Include the predicate**: for Field Visibility Debug, always include the exact predicate you tried.
- **Confirm environment credentials**: ensure `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`,
  and `DB_PASSWORD` are set in the environment before requesting a debug or listing run.

---

## Setting Up MySQL Credentials

The agent resolves credentials from environment variables. Set the following before running
any diagnostic or listing request:

```
DB_HOST=<mysql-server-host>
DB_PORT=3306
DB_NAME=<database-name>
DB_USER=<read-only-service-account>
DB_PASSWORD=<service-account-password>
```

**Important:**
- Use a **read-only** service account. The agent only executes `SELECT` queries.
- Never paste the password into the agent chat or template; supply it only through
  the environment or a secrets manager.

---

## Setting Up MCP Escalation

The agent uses MCP only to escalate queries it cannot resolve to the module owner.
Set the following environment variables to enable escalation:

```
MCP_SERVER_URL=<mcp-server-base-url>
MCP_OAUTH_TOKEN=<oauth-token-for-mcp-server>
MCP_CHAT_ID=<fields-team-support-chat-id>
```

**Important:**
- Authentication uses **OAuth**. The `MCP_OAUTH_TOKEN` is never written to any output.
- If any MCP variable is missing, the agent informs the user and skips the escalation.
- MCP is not used for successful findings — only for unresolved queries.

---

## Understanding Field Visibility Diagnostics

When a field is missing from the Filter API, the agent checks these conditions
(using the MySQL query templates Q-01 through Q-05 in `filter-knowledge.md`):

1. Is the **module** active? (`ZD_Modules.PRESENCE = 1`)
2. Is the field present in the Filter API response? (`CrmField.ISPRESENCE = 1`)
3. Is the field an internal state field? (`CrmField.IS_INTERNAL_STATE = 0` required)
4. Is the field a computed field? (`CrmField.IS_COMPUTED = 0` required)
5. Is the **operator** in the supported set for the field's `TYPE`?

---

## Supported Predicates Quick Reference

| Field Type | Supported Operators |
|---|---|
| `long` | `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `in`, `not_in` |
| `number` | `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `in`, `not_in` |
| `boolean` | `eq`, `ne` |
| `singleline` | `eq`, `ne`, `contains`, `starts_with`, `ends_with`, `in`, `not_in` |
| `textarea` | `contains` _(high scan cost — use with caution)_ |
| `picklist` | `eq`, `ne`, `in`, `not_in` |
