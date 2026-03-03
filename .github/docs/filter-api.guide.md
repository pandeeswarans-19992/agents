# Filter API Agent Guide

Example queries and configuration instructions for `.github/agents/filter-api.agent.md`.
This guide shows how to phrase requests to get the best output from the Filter API agent.

---

## What the Filter API Agent Can Do

| Capability | Description |
|---|---|
| Filter Suggestion | Given a use case, suggest the correct Filter API predicates, operators, and strategy |
| Field Visibility Debug | Diagnose why a specific field appears or does not appear in the Filter API |
| Field Inventory | List all filterable (and optionally non-filterable) fields for a module |
| MySQL Diagnostics | Execute read-only diagnostic queries against the live database |
| MCP Chat Notification | Post consolidated findings to the Fields team group chat |

---

## FILTER_SUGGESTION — Example Queries

> "I need to build a search screen that lets users find active doctors by specialty and partial name.
> The doctor table has about 2 million rows. What Filter API predicates and strategies should I use?"

> "We want to filter patients by age range and admission status. Which fields and operators
> should we use? Are there any performance risks?"

> "Give me an example Filter API request URL for finding all payments with status 'pending'
> or 'failed' made after a specific date."

---

## FIELD_VISIBILITY_DEBUG — Example Queries

> "The field `date_of_birth` on the `patient` module isn't showing up in the Filter API
> field listing. Can you find out why?"

> "I tried the predicate `specialist+eq+Cardiology` but the Filter API returns a 400 error.
> The specialist field exists on the doctor module. What's going wrong?"

> "Why can't I filter the `payment` module by the `notes` field? It exists in the database
> but doesn't appear when I list filterable fields."

---

## FILTER_FIELD_LISTING — Example Queries

> "Give me a complete list of all filterable fields for the `doctor` module, including
> which operators are supported for each."

> "List all fields on the `patient` module — both filterable and non-filterable — so I
> can decide which ones need to be enabled for the new search feature."

---

## Providing Inputs

Use the input template at `.github/templates/filter-api-input-template.md` for structured requests.

Minimum required inputs per request type:

| Request Type | Required |
|---|---|
| FILTER_SUGGESTION | module API name, use case description |
| FIELD_VISIBILITY_DEBUG | module API name, field name, MySQL credentials (from env) |
| FILTER_FIELD_LISTING | module API name, MySQL credentials (from env) |

### Tips for Better Queries

- **Name the module**: always include the module's API-level name (e.g. `doctor`, not `Doctor` or `doctors`).
- **Describe the use case precisely**: "find active Cardiology doctors by name" is more useful than "filter doctors".
- **Include the predicate you tried**: for debugging, paste the exact predicate string that failed.
- **State the observed vs expected behaviour**: the more specific, the faster the diagnosis.
- **Confirm environment credentials**: ensure `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`
  are set in the environment before requesting a debug or listing run.

---

## Setting Up MySQL Credentials

The agent resolves credentials from environment variables. Set the following before running
any diagnostic request:

```
DB_HOST=<mysql-server-host>
DB_PORT=3306
DB_NAME=<database-name>
DB_USER=<read-only-service-account>
DB_PASSWORD=<service-account-password>
```

**Important:**
- Use a **read-only** service account. The agent only executes `SELECT` queries
  and will refuse to run write operations.
- Never paste the password into the agent chat or template; supply it only through
  the environment or a secrets manager.

---

## Setting Up MCP Chat Notification

To enable automatic posting of findings to the Fields team group chat, set:

```
MCP_SERVER_URL=<mcp-server-base-url>
MCP_AUTH_TOKEN=<bearer-token-for-mcp-server>
MCP_CHAT_ID=<fields-team-chat-id>
```

**Important:**
- The `MCP_AUTH_TOKEN` is never written to reports or logged; supply it only through
  the environment.
- If any MCP variable is missing, the agent skips the notification step and notes
  it in the report. The diagnostic analysis still completes.

---

## Where to Find the Report

Generated reports are saved at:

```
ai-research-report/filter-api/<report-name>_v<version-number>.md
```

Examples:

- `ai-research-report/filter-api/field-visibility-debug_v1.md`
- `ai-research-report/filter-api/filter-suggestion-doctor_v1.md`
- `ai-research-report/filter-api/filter-field-listing-patient_v2.md`

---

## Understanding Filter API Diagnostics

When a field is missing from the Filter API, the agent checks these conditions in order:

1. Is the **module** active and filter-enabled?
2. Is the **field** active (`is_active = 1`)?
3. Is the field marked filterable (`is_filterable = 1`)?
4. Is the field visible in the listing (`filter_visible = 1`)?
5. Is the **operator** in the supported set for the field type?
6. For `picklist` fields: is the predicate **value key** an active picklist value?

Each condition maps to a specific MySQL query template (Q-01 through Q-05) documented in
`.github/knowledge/filter-knowledge.md`.

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
