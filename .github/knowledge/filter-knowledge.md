# Filter Knowledge

Purpose: Define what the Field Filter API is, how to construct Java predicates for
field filtering, the filtering strategies, scenario guidance for choosing the right API,
recommended filterable properties, best practices, and the rules agents must apply when
diagnosing filter API behaviour or suggesting filtering strategies.
Agents must load this file alongside `field-context.md`, `field-knowledge.md`, and
`module-knowledge.md` whenever a task involves the Filter API.
For CrmField MySQL schema (column definitions, deprecated columns), Java field API
inventory, architecture files, and MySQL diagnostic query templates,
refer to `.github/knowledge/field-context.md`.

---

## What Is the Field Filter API?

The **Field Filter API** is a tool that allows callers to fetch a list of fields by
applying specific, chainable filter conditions using `Predicate<AbstractField>` lambdas.
This enables meta-driven, efficient field retrieval based on business logic rather than
hard-coded field lists.

Key characteristics:

- Every field in a module is addressable and can be filtered by its metadata properties.
- Filters are composed using Java `Predicate<AbstractField>` lambdas (expression or method reference).
- Fields that are inactive or not present are silently excluded by the API.

---

## Java Predicate Reference by AbstractField Property

Use the following metadata properties of `AbstractField` when building predicate lambdas.
Agents must recommend properties from this table when suggesting or validating predicates.

| Property | Method | Use Case |
|----------|--------|----------|
| Internal state flag | `isInternalState()` | Exclude fields used for internal system processes |
| Computed flag | `isComputed()` | Exclude formula / calculated fields from predicates |
| Mandatory flag | `isMandatory()` | Include only fields that require a value |
| Sortable flag | `isSortable()` | Include only fields that support sorting |
| Basic flag | `isBasic()` | Include only fundamental, out-of-the-box fields |
| Identifier flag | `isIdentifier()` | Include only fields acting as unique identifiers |
| Source type | `getSourceType()` | Filter by origin: `SYSTEM`, `CUSTOM`, etc. |
| Field type | `getNewFieldType()` | Filter by data type (use this — not deprecated `getType()`, `getFieldType()`, `getUiType()`) |
| API name | `getApiName()` | Target a specific field by name (last resort) |
| Custom field | `isCustomField()` | Include only user-created custom fields |
| Indexed | `isIndexed()` | Include only fields with a database index |

---

## Why a Field May Not Appear in the Filter API

Use this checklist when diagnosing field visibility issues.
Agents must walk through all conditions before concluding a root cause.

| # | Condition | Diagnostic Query | Resolution |
|---|-----------|-----------------|------------|
| 1 | `CrmField.ISPRESENCE = 0` | `SELECT ISPRESENCE FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | Field is not present in Filter API; enable ISPRESENCE after platform review |
| 2 | `ZD_Modules.PRESENCE = 0` | `SELECT PRESENCE FROM ZD_Modules WHERE SYSTEMNAME = ?` | Module is globally disabled |
| 3 | `CrmField.IS_INTERNAL_STATE = 1` | `SELECT IS_INTERNAL_STATE FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | Internal state field; excluded from Filter API by design |
| 4 | `CrmField.IS_COMPUTED = 1` | `SELECT IS_COMPUTED FROM CrmField WHERE MODULEID = ? AND APINAME = ?` | Computed field; cannot be used in filter predicates |
| 5 | Operator not supported for TYPE | Check `CrmField.TYPE` vs operator used in predicate | Use a supported operator from the table above |

---

## Filtering Strategies

Agents must recommend the appropriate strategy based on the use case.

### Strategy 1 — Whitelisted Filtering (Inclusion)

An **opt-in** strategy that includes only a specific set of fields. All other fields
are ignored. Use when you know the exact fields you need — safer because it prevents
unexpected new fields from being processed.

**Example 1 — Filter by Field ID:**
```java
Set<Long> requiredFieldIds = Set.of(101L, 102L, 105L);
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(requiredFieldIds);
```

**Example 2 — Filter by API Name:**
```java
Predicate<AbstractField> filter = field -> "channel".equals(field.getApiName());
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(MODULE.TICKETS.getName(), departmentId, filter);
```

**Example 3 — Filter by Metadata (e.g. indexed datetime fields):**
```java
Predicate<AbstractField> filter = field -> field.isIndexed() && field.getNewFieldType() == DATETIME;
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(MODULE.TICKETS.getName(), departmentId, filter);
```

### Strategy 2 — Blacklisted Filtering (Exclusion)

An **opt-out** strategy that excludes certain fields and returns everything else.
Use for future-proofing: new fields are automatically included. Your code must be
prepared to handle any new fields that are not explicitly blocked.

**Example — Exclude computed fields:**
```java
Predicate<AbstractField> filter = field -> !field.isComputed();
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(MODULE.TICKETS.getName(), departmentId, filter);
```

**Example — Custom fields, optionally excluding unused ones:**
```java
Predicate<AbstractField> filter = AbstractField::isCustomField;

if (!isUnUsedFieldsNeeded) {
    Long layoutId = layoutApi.getLayoutsByDepartmentIds(CrmConstants.MODULE_AGENT, null)
                             .get(0)
                             .getLayoutId();
    Set<Long> unUsedFieldIds = layoutApi.getUnUsedAbstractFieldsInLayout(layoutId)
                                        .stream()
                                        .map(AbstractField::getId)
                                        .collect(Collectors.toSet());
    filter = field -> field.isCustomField() && !unUsedFieldIds.contains(field.getFieldId());
}
return orgFieldApi.getAbstractFields(module, null, filter);
```

---

## How to Choose the Right API

| Scenario | Recommended API | Reason |
|----------|----------------|--------|
| Criteria and Query Store — query construction | `OrgFieldAPI` | Configuration context; cannot use permission API |
| Criteria and Query Store — UI field listing | `LayoutFieldAPI` | Show fields from the layout in the UI |
| Table Views and Reports | `FieldPermissionAPI` | Field access must be restricted by user profile |
| Blueprint Transaction Forms | `LayoutFieldAPI` | Show fields associated with the ticket's layout |

---

## Best Practices for Predicate Construction

### 1. Avoid Internal Metadata in Filters

Never use methods that expose internal structural details in predicates. They lead
to fragile logic that breaks when the underlying system changes.

| Method to Avoid        | Alternate |
|------------------------|-----------|
| `getTableName()`       | N/A — do not use |
| `getColumnName()`      | N/A — do not use |
| `getType()`            | `getNewFieldType()` |
| `getFieldType()`       | `getNewFieldType()` |
| `getUiType()`          | `getNewFieldType()` |
| `getUITypeForCreate()` | `getNewFieldType()` |
| `getFieldLabel()`      | `getApiName()` |

**Recommended:**
```java
new OrgFieldApiImpl().getAbstractFields(MODULE.TICKETS.getName(), null,
    field -> !field.isInternalState() && !field.isComputed());
```

**Problematic — Do NOT use:**
```java
var caseColumnNames = Set.of(CRMCASE.SUBJECT, ...);
var filter = field -> field.getTableName().equals(CRMCASE.TABLE)
                   && caseColumnNames.contains(field.getColumnName());
new OrgFieldApiImpl().getAbstractFields(MODULE.TICKETS.getName(), null, filter);
```

### 2. Exclude Internal State Fields by Default

Almost every predicate should start by excluding internal state fields.
These fields (`responseSlaType`, `slaViolationType`, `isPresence`, etc.) are generally
not needed in UI or business logic.

```java
Predicate<AbstractField> filter = field -> !field.isInternalState() && /* additional conditions */;
```

### 3. Limit the Use of Sets and Maps

Avoid building large `Set` or `Map` structures inside predicates unless absolutely
necessary. Prefer metadata-driven boolean flags on `AbstractField`.

### 4. Use Expression Lambdas for Filtering

Prefer concise lambda expressions over anonymous inner classes to keep predicates
readable and composable.

```java
// Composable predicates
Predicate<AbstractField> notInternal = field -> !field.isInternalState();
Predicate<AbstractField> notComputed = field -> !field.isComputed();
Predicate<AbstractField> combined    = notInternal.and(notComputed);

List<AbstractField> fields = new OrgFieldAPIImpl()
    .getAbstractFields(MODULE.TICKETS.getName(), departmentId, combined);
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
