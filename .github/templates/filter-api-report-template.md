# FILTER API AGENT — Report

---

## 1. Report Identity

| Field | Value |
|---|---|
| Request Type | FILTER_SUGGESTION / FIELD_VISIBILITY_DEBUG / FILTER_FIELD_LISTING |
| Classification Confidence | _(0.0–1.0)_ |
| Report Template | `.github/templates/filter-api-report-template.md` |
| Agent | `.github/agents/filter-api.agent.md` |
| Module | _(module api_name)_ |
| Field (if applicable) | _(field_name or N/A)_ |
| Repository / Branch | |
| Generated At | _(ISO-8601 UTC)_ |

---

## 2. Inputs — User-Provided vs Agent-Derived

| # | Input | Value | Source | How Agent Derived It (if not from user) |
|---|---|---|---|---|
| 1 | Module API Name | | User / Agent | |
| 2 | Request Type | | User / Agent | Classified from prompt keywords |
| 3 | Field Name | | User / N/A | N/A for FILTER_SUGGESTION |
| 4 | Predicate Attempted | | User / N/A | |
| 5 | Use Case Description | | User / N/A | |
| 6 | MySQL Credentials | Resolved from env | Agent | Never logged; used only for query execution |
| 7 | MCP Config | Resolved from env | Agent | MCP_AUTH_TOKEN not logged |

---

## 3. Executive Summary

> One-paragraph overview of the session.

- **Request Subject:**
- **Module:**
- **Field (if applicable):**
- **Key Finding:**
- **Recommended Action:**
- **MCP Notification Status:** Sent / Skipped / Failed

---

## 4. Scope

| Category | Details |
|---|---|
| In Scope | |
| Out of Scope | |
| Assumptions | |
| Limitations | |

---

## 5. Findings

> Central findings table. Each row is the single source of truth for that finding.

| ID | Title | Severity | Root Cause Class | What Was Found | Evidence | Action |
|---|---|---|---|---|---|---|
| F-001 | _(short title)_ | Critical / High / Medium / Low | _(root_cause_class)_ | _(1–2 sentence observation)_ | [E-001](#e-001) | [A-001](#a-001) |
| F-002 | | | | | [E-002](#e-002) | [A-002](#a-002) |

**Root Cause Classes (FIELD_VISIBILITY_DEBUG):**
`field_inactive` | `not_filterable` | `filter_hidden` | `module_filter_disabled` |
`module_inactive` | `operator_unsupported` | `picklist_value_inactive` | `field_not_found` | `unknown`

---

## 6. Evidence Catalog

> Proof for each finding. Reference these IDs from Findings and Actions.

### E-001
| Field | Detail |
|---|---|
| Supports Finding | [F-001](#f-001) |
| Query Executed | _(Q-01 / Q-02 / Q-03 / Q-04 / Q-05)_ |
| SQL Template | _(query template name from filter-knowledge.md)_ |
| Row Count Returned | _(number)_ |
| Key Column Values | _(relevant non-credential column values from result)_ |
| What It Shows | _(why this proves the finding)_ |
| Confidence | High / Medium / Low |

_(Repeat block for E-002, E-003, …)_

---

## 7. Filter API Suggestion (FILTER_SUGGESTION only)

> Skip this section for FIELD_VISIBILITY_DEBUG and FILTER_FIELD_LISTING.

### 7.1 Recommended Strategy

| # | Strategy Name | Justification | Fields Used |
|---|---|---|---|
| 1 | _(e.g. Compound Filter)_ | _(why this fits the use case)_ | _(field list)_ |

### 7.2 Example Predicates

| Field | Operator | Example Value | Field Type | Risk |
|---|---|---|---|---|
| _(field_name)_ | _(operator)_ | _(example)_ | _(type)_ | Low / Medium / High |

### 7.3 Example Filter API Request

```
GET /filter/<module>?predicate=<field>+<op>+<value>&predicate=...&logic=AND&page=1&per_page=20
```

### 7.4 Strategy Risks and Caveats

| Risk | Severity | Notes |
|---|---|---|
| _(e.g. textarea full-table scan)_ | High | _(mitigation)_ |

---

## 8. Filterable Field Inventory (FILTER_FIELD_LISTING and FIELD_VISIBILITY_DEBUG)

> For FILTER_SUGGESTION, this section may be omitted unless discovery was needed.

### 8.1 Filterable Fields

| Field Name | Field Type | filter_visible | Supported Operators | is_active |
|---|---|---|---|---|
| | | | | |

### 8.2 Non-Filterable Active Fields (if requested)

| Field Name | Field Type | is_filterable | Reason Not Filterable | Notes |
|---|---|---|---|---|
| | | 0 | _(e.g. not configured)_ | |

---

## 9. Picklist Value Status (if applicable)

> Include only when a picklist field is involved.

| Value Key | Label | is_active | Impact on Predicate |
|---|---|---|---|
| | | | |

---

## 10. Actions

> Concrete steps to resolve each finding. Every action traces to exactly one finding.

### A-001
| Field | Detail |
|---|---|
| Closes Finding | [F-001](#f-001) |
| What To Do | _(clear, actionable objective)_ |
| Change Type | Config / Schema / Code / MCP / Escalation |
| Priority | P0 / P1 / P2 |
| Resolution SQL | _(SQL statement for DBA review only — never executed by agent; may be `UPDATE`, `ALTER`, or other DML/DDL)_ |
| Done When | _(success criteria, e.g. "field appears in Filter API field listing")_ |
| Verify By | _(how to confirm, e.g. "GET /filter/patient — field_name present in response")_ |

_(Repeat block for A-002, A-003, …)_

---

## 11. MySQL Query Log

> Record every query the agent executed. Credentials must not appear here.

| # | Template | Module | Field | Rows Returned | Notes |
|---|---|---|---|---|---|
| 1 | Q-01 | _(module)_ | N/A | _(count)_ | |
| 2 | Q-02 | _(module)_ | _(field)_ | _(count)_ | |
| 3 | Q-05 | _(module)_ | _(field)_ | _(count)_ | Picklist check |

---

## 12. MCP Notification Log

| Field | Detail |
|---|---|
| Status | Sent / Skipped / Failed |
| Chat ID | _(MCP_CHAT_ID — not the token)_ |
| Message Type | `filter_api_analysis` |
| HTTP Status | _(e.g. 200 OK / 401 Unauthorized)_ |
| Message ID (if sent) | |
| Skip Reason (if skipped) | _(e.g. MCP_AUTH_TOKEN not available)_ |
| Failure Detail (if failed) | _(HTTP status + response body summary)_ |

---

## 13. Risk & Safety

### 13a. Risk Matrix

| Risk ID | Category | Severity | Likelihood | Impact | Linked Finding |
|---|---|---|---|---|---|
| R-001 | Data | | | | [F-001](#f-001) |

### 13b. Credential Safety

| Check | Status | Notes |
|---|---|---|
| DB_PASSWORD not in report | | |
| MCP_AUTH_TOKEN not in report | | |
| Parameterised queries only | | |
| No write queries executed | | |

---

## 14. Verdict

- **Confidence Score:**
- **Root Cause (FIELD_VISIBILITY_DEBUG):**
- **Recommended Immediate Next Step:**
- **Open Unknowns:**

---

## Appendix A — Workflow Step Log

| Step | What Was Done | What Was Not Done | Why |
|---|---|---|---|
| Gather Inputs | | | |
| Module Check (Q-01) | | | |
| Field Check (Q-02) | | | |
| Filterable Field Listing (Q-03/Q-04) | | | |
| Picklist Check (Q-05) | | | |
| Root Cause Classification | | | |
| Strategy / Recommendation | | | |
| MCP Notification | | | |

## Appendix B — Knowledge Coverage

| Knowledge File | Applied? | Key Observations |
|---|---|---|
| `filter-knowledge.md` | | |
| `field-knowledge.md` | | |
| `module-knowledge.md` | | |
| `common-knowledge.md` | | |
