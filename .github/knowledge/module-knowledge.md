# Module Knowledge

Purpose: Document the names, responsibilities, ownership boundaries, and
inter-module contracts for every major module in the system.
Agents use this file to avoid re-discovering module structure on every run.

## Application Context

Domain: Hospital Management System
The system manages doctors, patients, and payments. Each concept is represented
as a module with a dedicated base table, optional dependency tables, and
join relationships to related modules.

## Module Inventory

| Module Name | Base Table         | Responsibility                                          | Status |
|-------------|--------------------|---------------------------------------------------------|--------|
| Doctor      | doctor             | Stores doctor profiles including specialty information  | Active |
| Patient     | patient            | Stores patient demographic and contact details          | Active |
| Payment     | payment            | Tracks payment transactions linked to patients          | Active |

## Module Field Definitions

### Doctor Module

Base table: `doctor`

| Field Name  | Field Type | DB Column Type | Constraints              | Notes                              |
|-------------|------------|----------------|--------------------------|------------------------------------|
| id          | long       | BIGINT         | PRIMARY KEY, NOT NULL    | Auto-incremented surrogate key     |
| name        | singleline | VARCHAR(255)   | NOT NULL                 | Full name of the doctor            |
| description | textarea   | TEXT           | NULLABLE                 | Free-text biography or notes       |
| specialist  | picklist   | VARCHAR(100)   | NOT NULL                 | Allowed values defined in picklist table (e.g. Cardiology, Neurology, Orthopedics, General) |

Dependency tables:
- `picklist_value` – stores the allowed values for `specialist`; joined on `doctor.specialist = picklist_value.value_key`

### Patient Module

Base table: `patient`

| Field Name  | Field Type | DB Column Type | Constraints              | Notes                                    |
|-------------|------------|----------------|--------------------------|------------------------------------------|
| id          | long       | BIGINT         | PRIMARY KEY, NOT NULL    | Auto-incremented surrogate key           |
| name        | singleline | VARCHAR(255)   | NOT NULL                 | Full name of the patient                 |
| age         | number     | INT            | NOT NULL, >= 0           | Age in years                             |
| gender      | picklist   | VARCHAR(20)    | NOT NULL                 | Allowed values: Male, Female, Other      |
| contact     | singleline | VARCHAR(20)    | NOT NULL                 | Primary phone or contact number          |
| description | textarea   | TEXT           | NULLABLE                 | Medical history summary or notes         |
| doctor_id   | long       | BIGINT         | FOREIGN KEY (doctor.id)  | Assigned/primary doctor                  |

Dependency tables:
- `picklist_value` – stores the allowed values for `gender`; joined on `patient.gender = picklist_value.value_key`

Join information:
- `patient` JOIN `doctor` ON `patient.doctor_id = doctor.id` – resolves the assigned doctor record

### Payment Module

Base table: `payment`

| Field Name    | Field Type | DB Column Type | Constraints              | Notes                                        |
|---------------|------------|----------------|--------------------------|----------------------------------------------|
| id            | long       | BIGINT         | PRIMARY KEY, NOT NULL    | Auto-incremented surrogate key               |
| patient_id    | long       | BIGINT         | FOREIGN KEY (patient.id) | Patient associated with this payment         |
| amount        | number     | INT            | NOT NULL, > 0            | Payment amount (in smallest currency unit)   |
| status        | picklist   | VARCHAR(50)    | NOT NULL                 | Allowed values: Pending, Completed, Refunded |
| payment_date  | singleline | VARCHAR(20)    | NOT NULL                 | ISO 8601 date string (YYYY-MM-DD)            |
| description   | textarea   | TEXT           | NULLABLE                 | Remarks or invoice reference                 |

Dependency tables:
- `picklist_value` – stores the allowed values for `status`; joined on `payment.status = picklist_value.value_key`

Join information:
- `payment` JOIN `patient` ON `payment.patient_id = patient.id` – resolves the patient associated with the payment
- `payment` JOIN `patient` JOIN `doctor` ON `payment.patient_id = patient.id AND patient.doctor_id = doctor.id` – full chain to resolve treating doctor

## Module Dependency Map

Permitted dependency directions between modules:

- Payment -> Patient: a payment must always be linked to a patient (`payment.patient_id`)
- Patient -> Doctor: a patient may be assigned to a doctor (`patient.doctor_id`)
- Doctor: no outgoing foreign-key dependencies to other domain modules

## Module Contracts

### Doctor

- Exposes: doctor record identified by `id`; readable by Patient and (transitively) Payment
- Consumes: `picklist_value` for specialist field validation
- Invariants: `id` must be unique and immutable; `specialist` must match a value in `picklist_value`
- Known breaking-change risks: renaming or removing a specialist picklist value will orphan existing doctor records

### Patient

- Exposes: patient record identified by `id`; readable by Payment
- Consumes: Doctor module (via `doctor_id`), `picklist_value` for gender
- Invariants: `id` must be unique and immutable; `doctor_id` must reference a valid `doctor.id`
- Known breaking-change risks: deleting a doctor record without nullifying or reassigning `patient.doctor_id` will break referential integrity

### Payment

- Exposes: payment transaction record identified by `id`
- Consumes: Patient module (via `patient_id`), `picklist_value` for status
- Invariants: `id` must be unique and immutable; `patient_id` must reference a valid `patient.id`; `amount` must be > 0
- Known breaking-change risks: deleting a patient without cascading or archiving payments will break referential integrity

## Cross-Cutting Modules

- `picklist_value`: shared lookup table used by Doctor (`specialist`), Patient (`gender`), and Payment (`status`); must not be deleted without verifying all referencing modules

## Deprecated Modules

| Module Name | Replacement | Removal Target Date |
|-------------|-------------|---------------------|
