# USE_CASE_ALIGNMENT_ANALYSIS — Report

---

## 1. Report Identity

| Field | Value |
|---|---|
| Analysis Type | USE_CASE_ALIGNMENT_ANALYSIS |
| Classification Confidence | _(0.0–1.0)_ |
| Report Template | `.github/templates/usecase-alignment-report-template.md` |
| Workflow Source | _(agent-local deep steps or external reference)_ |
| Repository / Branch | |
| Generated At | |

---

## 2. Inputs — What Came From the User vs What the Agent Derived

> **Purpose:** Make it transparent which inputs were provided by the user
> and which were inferred by the agent so reviewers can judge assumptions.

| # | Input | Value | Source | How Agent Derived It (if not from user) |
|---|---|---|---|---|
| 1 | Request Context | | User / Agent | Extracted from user prompt and constraints |
| 2 | Scope Targets | | User / Agent | Inferred from use-case boundaries and mapped behaviors |
| 3 | Requirements / Use Case Doc | | User / Agent | Marked `Not Provided` if absent |
| 4 | Non-Functional Constraints | | User / Agent | Inferred from configs and runtime setup |
| 5 | Expected Output Format | | User / Agent | Defaults to this template |

---

## 3. Executive Summary

> **Purpose:** One-paragraph overview so a reader can decide whether to read further.

- **Use Case Subject:**
- **Goal (what alignment is being checked):**
- **Alignment Verdict:**
- **Coverage Score:** _( % of expected behaviors confirmed)_
- **Top Risks (≤ 3):**
- **Verdict (one line):**

---

## 4. Scope

> **Purpose:** Define boundaries so every finding can be traced to agreed scope.

| Category | Details |
|---|---|
| In Scope | |
| Out of Scope | |
| Assumptions | |
| Limitations | |

---

## 5. Architecture Context

> **Purpose:** Orient the reader on the system areas relevant to this use case.

- **Architecture Style:**
- **Key Modules / Layers:**
- **Dependency / Boundary Notes:**
- **Integration Points:**
- **Use-Case Entry Points:**

---

## 6. Findings

> **Purpose:** Central table of everything discovered. Each row is the single source of truth
> for that finding. Evidence, gaps, and actions link back here — never rewrite the same fact twice.

| ID | Title | Severity | What Was Found | Evidence | Gap | Action |
|---|---|---|---|---|---|---|
| F-001 | _(short title)_ | Critical / High / Medium / Low | _(1–2 sentence observation)_ | [E-001](#e-001) | [G-001](#g-001) | [A-001](#a-001) |
| F-002 | | | | [E-002](#e-002) | [G-002](#g-002) | [A-002](#a-002) |

---

## 7. Evidence Catalog

> **Purpose:** Proof for each finding. Stored once here; referenced by ID everywhere else.

### E-001
| Field | Detail |
|---|---|
| Supports Finding | [F-001](#f-001) |
| Type | File / Method / Config / Schema / Runtime Path |
| File | [`relative/path/to/file.ext`](relative/path/to/file.ext) |
| Lines | [`file.ext#L10-L25`](relative/path/to/file.ext#L10-L25) |
| What It Shows | _(why this proves the finding)_ |
| Confidence | High / Medium / Low |

_(Repeat block for E-002, E-003, …)_

---

## 8. Gaps

> **Purpose:** Each gap is a delta between expected use-case behavior and actual implementation.
> Every gap must trace to at least one finding.

### G-001
| Field | Detail |
|---|---|
| Linked Finding | [F-001](#f-001) |
| Gap | _(what expected behavior is missing, partial, or wrong)_ |
| Root Cause | |
| Impact | |
| Severity | Critical / High / Medium / Low |
| Evidence | [E-001](#e-001) |

_(Repeat block for G-002, G-003, …)_

---

## 9. Actions

> **Purpose:** Concrete steps to close each gap. Every action traces to exactly one gap.

### A-001
| Field | Detail |
|---|---|
| Closes Gap | [G-001](#g-001) |
| What To Do | _(clear, actionable objective)_ |
| Change Type | Add / Modify / Remove / Guardrail / Refactor |
| Priority | P0 / P1 / P2 |
| Owner Suggestion | |
| Done When | _(success criteria)_ |
| Verify By | _(how to confirm it worked)_ |
| Recheck Evidence | [E-001](#e-001) |

_(Repeat block for A-002, A-003, …)_

---

## 10. Roadmap

> **Purpose:** Phase the actions so teams can converge on full alignment.

| Phase | Horizon | Objective | Actions | Exit Criteria |
|---|---|---|---|---|
| P0 | Immediate (0–1 week) | Close critical alignment mismatches | [A-001](#a-001) | Critical use-case paths match expected behavior |
| P1 | Short-term (1–4 weeks) | Resolve partial / missing coverage | | All high-priority behaviors aligned |
| P2 | Medium-term (1–3 months) | Institutionalize alignment monitoring | | Regression checks and alignment score tracking in place |

---

## 11. Behavior Alignment Matrix

> **Purpose:** Map every expected behavior to its implementation status.
> This is the core deliverable of a use-case alignment analysis.

| # | Expected Behavior | Status | Linked Finding | Evidence | Notes |
|---|---|---|---|---|---|
| 1 | _(behavior from use case)_ | Full / Partial / Missing / Unexpected | [F-001](#f-001) | [E-001](#e-001) | |
| 2 | | | | | |

---

## 12. Risk & Safety

> **Purpose:** Consolidated risk view and execution-safety assessment.

### 12a. Risk Matrix

| Risk ID | Category | Severity | Likelihood | Impact | Linked Finding |
|---|---|---|---|---|---|
| R-001 | | | | | [F-001](#f-001) |

### 12b. Execution Safety

| Dimension | Status | Notes |
|---|---|---|
| Transaction Safety | | |
| Failure Modes | | |
| Data Integrity | | |
| Rollback / Recovery | | |

---

## 13. Scalability

| Dimension | Assessment | Notes |
|---|---|---|
| Throughput / Latency | | |
| Concurrency | | |
| Resource Usage | | |
| Growth Constraints | | |

---

## 14. Maturity

| Dimension | Value |
|---|---|
| Current Level | |
| Justification | |
| Target Level | |

---

## 15. Verdict

> **Purpose:** Final judgment. Summarize alignment confidence and recommended next step.

- **Confidence Score:**
- **Alignment Assessment:**
- **Coverage Score:** _( % )_
- **Recommended Immediate Next Step:**
- **Open Unknowns:**

---

## Appendix A — Workflow Step Evidence

> **Purpose:** Log what the agent did and did not do during execution.

| Step | What Was Done | What Was Not Done | Why |
|---|---|---|---|
| Scope Discovery | | | |
| Repository Cartography | | | |
| Call-Path Tracing | | | |
| Data & Transaction Flow | | | |
| Validation / Security / Errors | | | |
| Gap & Feasibility Assessment | | | |
| Recommendation & Impact Modeling | | | |
| Confidence & Conformance Check | | | |

## Appendix B — Case-Specific Evidence (USE_CASE_ALIGNMENT_ANALYSIS)

| Check | Evidence / Notes |
|---|---|
| Atomic behavior extraction from the use case | |
| Behavior-to-code mapping | |
| Runtime flow verification per behavior | |
| Coverage classification (full / partial / missing / unexpected) | |
| Gap severity and impact assessment | |
| Alignment score calculation basis | |

## Appendix C — Knowledge Coverage

| Domain | Applied? | Key Observations |
|---|---|---|
| Architecture | | |
| Design Patterns (incl. anti-patterns) | | |
| Data Structure Fitness | | |
| Algorithm Complexity / Hotspots | | |
