# Field Knowledge

Purpose: Document domain terminology, business rules, data field definitions,
and validation constraints that agents must understand to produce accurate findings.
Populate this file with project-specific domain context to avoid repeated discovery.

## Field Type to Database Column Mapping

Every field in the system has a logical type that maps directly to a database column type.
Agents must apply this mapping when reasoning about schema design, migrations, or validations.

| Field Type | DB Column Type | Notes                                                       |
|------------|----------------|-------------------------------------------------------------|
| long       | BIGINT         | Used for surrogate keys (id) and foreign keys               |
| number     | INT            | General-purpose integer values (age, amounts, counts)       |
| boolean    | TINYINT(1)     | 0 = false, 1 = true                                         |
| singleline | VARCHAR(255)   | Short free-text strings; max 255 characters unless noted    |
| textarea   | TEXT           | Long free-text content; no practical length limit           |
| picklist   | VARCHAR(100)   | Stores the selected value key; valid values in picklist_value table |

## Domain Glossary

| Term          | Definition                                                        | Common Code Identifiers              |
|---------------|-------------------------------------------------------------------|--------------------------------------|
| Module        | A self-contained feature area with its own base table and fields  | doctor, patient, payment             |
| Base Table    | The primary database table owned by a module                      | doctor, patient, payment             |
| Picklist      | A field whose value must come from a predefined set of options    | specialist, gender, status           |
| Picklist Value| A row in `picklist_value` representing one allowed option         | picklist_value.value_key             |
| Foreign Key   | A `long` field that references the `id` of another module's table | doctor_id, patient_id                |
| Singleline    | A VARCHAR field for short text input                              | name, contact, payment_date          |
| Textarea      | A TEXT field for long-form free text                              | description                          |

## Core Business Rules

- BR-001 – Every module record must have an `id` field of type `long` (BIGINT) as its primary key.
- BR-002 – Every foreign-key field must use type `long` (BIGINT) to match the referenced table's `id` column.
- BR-003 – Picklist fields must store a value key that exists in the `picklist_value` table; orphaned keys are invalid.
- BR-004 – `amount` in the Payment module must be greater than zero.
- BR-005 – `payment_date` must be a valid ISO 8601 date string (YYYY-MM-DD).
- BR-006 – A payment record must always reference a valid patient; orphaned payments are not permitted.
- BR-007 – A patient's `doctor_id` must reference a valid doctor record when set.

## Key Data Fields

### Doctor Module (`doctor` table)

| Field Name  | Entity / Table | Type       | DB Column Type | Valid Values / Constraints                        | Business Significance                         |
|-------------|---------------|------------|----------------|--------------------------------------------------|-----------------------------------------------|
| id          | doctor        | long       | BIGINT         | PK, NOT NULL, auto-increment                     | Unique identifier for a doctor record         |
| name        | doctor        | singleline | VARCHAR(255)   | NOT NULL, non-empty                              | Doctor's full name                            |
| description | doctor        | textarea   | TEXT           | NULLABLE                                         | Biography, qualifications, or general notes   |
| specialist  | doctor        | picklist   | VARCHAR(100)   | NOT NULL; value must exist in picklist_value     | Doctor's area of medical specialization       |

### Patient Module (`patient` table)

| Field Name  | Entity / Table | Type       | DB Column Type | Valid Values / Constraints                        | Business Significance                         |
|-------------|---------------|------------|----------------|--------------------------------------------------|-----------------------------------------------|
| id          | patient       | long       | BIGINT         | PK, NOT NULL, auto-increment                     | Unique identifier for a patient record        |
| name        | patient       | singleline | VARCHAR(255)   | NOT NULL, non-empty                              | Patient's full name                           |
| age         | patient       | number     | INT            | NOT NULL, >= 0                                   | Patient's age in years                        |
| gender      | patient       | picklist   | VARCHAR(20)    | NOT NULL; value must exist in picklist_value     | Patient's gender identity                     |
| contact     | patient       | singleline | VARCHAR(20)    | NOT NULL, non-empty                              | Primary phone or contact number               |
| description | patient       | textarea   | TEXT           | NULLABLE                                         | Medical history summary or additional notes   |
| doctor_id   | patient       | long       | BIGINT         | FK → doctor.id; NULLABLE                         | Assigned primary doctor for the patient       |

### Payment Module (`payment` table)

| Field Name   | Entity / Table | Type       | DB Column Type | Valid Values / Constraints                        | Business Significance                         |
|--------------|---------------|------------|----------------|--------------------------------------------------|-----------------------------------------------|
| id           | payment       | long       | BIGINT         | PK, NOT NULL, auto-increment                     | Unique identifier for a payment record        |
| patient_id   | payment       | long       | BIGINT         | FK → patient.id; NOT NULL                        | Patient associated with this payment          |
| amount       | payment       | number     | INT            | NOT NULL, > 0                                    | Payment amount in the smallest currency unit  |
| status       | payment       | picklist   | VARCHAR(50)    | NOT NULL; value must exist in picklist_value     | Current payment state                         |
| payment_date | payment       | singleline | VARCHAR(20)    | NOT NULL; must be valid ISO 8601 date (YYYY-MM-DD)| Date on which the payment was made           |
| description  | payment       | textarea   | TEXT           | NULLABLE                                         | Remarks, invoice reference, or billing notes  |

## Validation Rules

- id (all modules): must be a positive BIGINT; generated by the database; must not be supplied by the client on create
- name (doctor, patient): must be non-empty after trimming whitespace; max 255 characters
- specialist (doctor): must match an active value in `picklist_value` for the `specialist` picklist group
- age (patient): must be an integer >= 0
- gender (patient): must match an active value in `picklist_value` for the `gender` picklist group
- contact (patient): must be non-empty; should match a phone-number pattern
- doctor_id (patient): when provided, must reference an existing `doctor.id`
- patient_id (payment): must reference an existing `patient.id`; required on every payment record
- amount (payment): must be a positive integer > 0
- status (payment): must match an active value in `picklist_value` for the `status` picklist group
- payment_date (payment): must be a valid ISO 8601 date string (YYYY-MM-DD)

## State Machines

### Payment

- States: Pending, Completed, Refunded
- Allowed transitions:
  - Pending -> Completed: payment is successfully processed
  - Pending -> Refunded: payment is cancelled before processing
  - Completed -> Refunded: payment is reversed after processing
- Terminal states: Refunded (no further transitions permitted once refunded)

## Compliance and Regulatory Notes

- Patient personal data (name, age, gender, contact): classified as sensitive personally identifiable information (PII); must not appear in logs or error messages (see common-knowledge.md BR on sensitive data).
- Payment amount data: must be stored and transmitted accurately; any rounding must be explicitly documented.

