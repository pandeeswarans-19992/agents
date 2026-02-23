## USE_CASE_ALIGNMENT_ANALYSIS -- Request Input Template

Purpose: Standard input format for submitting a USE_CASE_ALIGNMENT_ANALYSIS request to the research agent.
Complete as many fields as possible to improve analysis accuracy and report quality.
Reference: .github/agents/research.agent.md

---

## Request Fields

- Goal:
  (Describe what you want to verify, e.g. "Verify the password-reset flow against the use case document.")

- Feature / Use Case Name:
  (Short kebab-case name used as the output folder name, e.g. `password-reset`.)

- Use Case Document:
  (Paste the use case description inline, or provide a file path, e.g. `docs/use-cases/password-reset.md`.
   The agent will extract atomic expected behaviors from this document.)

- Specific Behaviors to Verify:
  (List the individual behaviors you want validated, one per line.
   Leave blank to let the agent extract all behaviors from the use case document.
   Example:
     - Token must expire after 15 minutes.
     - Reset link must be invalidated after first use.
     - Audit log entry must be created on every reset attempt.)

- Known Implementation Files:
  (List files or modules you already know implement this use case, e.g. `src/auth`, `src/notification`.)

- Scope Out:
  (List file paths, modules, or layers that must be excluded from the analysis.)

- Compliance / Audit Requirements:
  (Describe any regulatory or internal compliance requirements that apply,
   e.g. "GDPR - user must be notified of reset via verified channel", "PCI-DSS logging required".)

- Coverage Threshold:
  (State the minimum acceptable alignment score, e.g. "At least 90% of behaviors must be fully covered."
   Leave blank to use the agent default.)

- Constraints:
  (Security, performance, time-box, or other non-functional requirements.)

- Expected Output:
  (Describe what deliverables you need, e.g. behavior-to-code mapping, coverage gaps, alignment score.)

---

## Input Examples

### Compliance-driven verification

Goal: Verify password-reset flow against use case document.
Feature / Use Case Name: password-reset
Use Case Document: docs/use-cases/password-reset.md
Specific Behaviors to Verify:
  - Token must expire after 15 minutes.
  - Reset link must be single-use.
  - Failed attempts must be logged with timestamp and IP.
Known Implementation Files: `src/auth`, `src/notification`
Compliance / Audit Requirements: Compliance and audit logging required; OWASP ASVS Level 2.
Expected Output: behavior-to-code mapping, coverage gaps, alignment score, compliance gap list

### Full use-case coverage check

Goal: Verify all checkout behaviors are correctly implemented.
Feature / Use Case Name: checkout-flow
Use Case Document: |
  Actor: authenticated customer.
  1. Customer adds items to cart.
  2. Customer selects shipping address.
  3. Customer selects payment method.
  4. System validates stock in real time.
  5. System reserves stock and creates pending order.
  6. Customer confirms; system charges payment.
  7. On success, system sends confirmation email and releases reservation as fulfilled.
  8. On payment failure, system releases reservation and notifies customer.
Known Implementation Files: `src/checkout`, `src/orders`, `src/payments`, `src/notifications`
Coverage Threshold: 95% of behaviors must be fully covered.
Expected Output: behavior-to-code mapping, gap list with severity, alignment score, recommended fixes
