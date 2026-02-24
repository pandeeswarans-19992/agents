# NEW_FEATURE_ANALYSIS — Report

---

## 1. Report Identity

| Field | Value |
|---|---|
| Analysis Type | NEW_FEATURE_ANALYSIS |
| Classification Confidence | _(0.0–1.0)_ |
| Report Template | `.github/templates/new-feature-analysis-report-template.md` |
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
| 2 | Scope Targets | | User / Agent | Inferred from feature boundaries and affected modules |
| 3 | Requirements / Use Case Doc | | User / Agent | Marked `Not Provided` if absent |
| 4 | Non-Functional Constraints | | User / Agent | Inferred from configs and runtime setup |
| 5 | Expected Output Format | | User / Agent | Defaults to this template |

---

## 3. Executive Summary

> **Purpose:** One-paragraph overview so a reader can decide whether to read further.

- **Feature Subject:**
- **Goal:**
- **Feasibility Verdict:**
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

## 5. Findings

> **Purpose:** Central table of everything discovered. Each row is the single source of truth
> for that finding. Evidence, gaps, and actions link back here — never rewrite the same fact twice.

| ID | Title | Severity | What Was Found | Evidence | Gap | Action |
|---|---|---|---|---|---|---|
| F-001 | _(short title)_ | Critical / High / Medium / Low | _(1–2 sentence observation)_ | [E-001](#e-001) | [G-001](#g-001) | [A-001](#a-001) |
| F-002 | | | | [E-002](#e-002) | [G-002](#g-002) | [A-002](#a-002) |

---

## 6. Evidence Catalog

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

## 7. Gaps

> **Purpose:** Each gap is a delta between what the new feature needs and what exists today.
> Every gap must trace to at least one finding.

### G-001
| Field | Detail |
|---|---|
| Linked Finding | [F-001](#f-001) |
| Gap | _(what is missing or incompatible)_ |
| Root Cause | |
| Impact | |
| Severity | Critical / High / Medium / Low |
| Evidence | [E-001](#e-001) |

_(Repeat block for G-002, G-003, …)_

---

## 8. Actions

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

## 9. Roadmap

> **Purpose:** Phase the actions so teams can plan delivery safely.

| Phase | Horizon | Objective | Actions | Exit Criteria |
|---|---|---|---|---|
| P0 | Immediate (0–1 week) | De-risk feature introduction | [A-001](#a-001) | Core safety checks pass |
| P1 | Short-term (1–4 weeks) | Complete functional coverage | | Feature requirements met |
| P2 | Medium-term (1–3 months) | Harden maintainability | | Scale and operability validated |

---

## 10. Suggestions — Architecture, Patterns, Data Structures, Algorithms

> **Purpose:** Actionable improvement suggestions based on findings. Include only when applicable.
> Each suggestion must link to a finding or gap that motivates it. Skip domains with no relevant observations.

| # | Domain | Suggestion | Why (linked finding/gap) | Impact if Applied |
|---|---|---|---|---|
| 1 | Architecture | _(e.g., isolate new feature behind a bounded context)_ | [F-001](#f-001) | _(expected benefit)_ |
| 2 | Design Pattern | _(e.g., use factory for pluggable provider creation)_ | [G-002](#g-002) | |
| 3 | Data Structure | _(e.g., use immutable DTO to prevent mutation bugs)_ | [F-003](#f-003) | |
| 4 | Algorithm | _(e.g., batch processing instead of sequential calls)_ | [F-004](#f-004) | |

_(Delete rows for domains that have no suggestions. Do not include empty placeholders.)_

---

## 11. Risk & Safety

> **Purpose:** Consolidated risk view and execution-safety assessment.

### 11a. Risk Matrix

| Risk ID | Category | Severity | Likelihood | Impact | Linked Finding |
|---|---|---|---|---|---|
| R-001 | | | | | [F-001](#f-001) |

### 11b. Execution Safety

| Dimension | Status | Notes |
|---|---|---|
| Transaction Safety | | |
| Failure Modes | | |
| Data Integrity | | |
| Rollback / Recovery | | |

---

## 12. Scalability

| Dimension | Assessment | Notes |
|---|---|---|
| Throughput / Latency | | |
| Concurrency | | |
| Resource Usage | | |
| Growth Constraints | | |

---

## 13. Maturity

| Dimension | Value |
|---|---|
| Current Level | |
| Justification | |
| Target Level | |

---

## 14. Verdict

> **Purpose:** Final judgment. Summarize confidence, feasibility, and the recommended next step.

- **Confidence Score:**
- **Feasibility Assessment:**
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

## Appendix B — Case-Specific Evidence (NEW_FEATURE_ANALYSIS)

| Check | Evidence / Notes |
|---|---|
| Use-case decomposition (actors, triggers, edge cases) | |
| Architecture insertion-point identification | |
| Contract / API / schema delta definition | |
| Reuse vs new-component decisions | |
| Migration and backward-compatibility strategy | |
| Phased implementation planning | |

## Appendix C — Knowledge Coverage

| Domain | Applied? | Key Observations |
|---|---|---|
| Architecture | | |
| Design Patterns (incl. anti-patterns) | | |
| Data Structure Fitness | | |
| Algorithm Complexity / Hotspots | | |
