# Module Knowledge

Purpose: Define what a module is, how it is structured, and the architectural
rules that govern every module in the system. Agents must apply this understanding
when analysing, generating, or reviewing any module.

## What Is a Module?

A **module** is a self-contained feature unit that encapsulates a single
business concept. It owns its own data, exposes a defined interface to other
modules, and must not reach into another module's internals.

Each module consists of:

- **Base table** – the primary database table that owns the module's core data.
- **Dependency tables** – lookup or reference tables the module relies on
  (e.g. a `picklist_value` table that supplies allowed values for a picklist field).
- **Join information** – the declared relationships to other module base tables
  expressed as foreign-key joins.
- **Fields** – the named, typed attributes stored in the base table
  (see `field-knowledge.md` for the complete field-type reference).

## Module Architecture

```
┌─────────────────────────────┐
│           Module            │
│                             │
│  ┌─────────────────────┐    │
│  │     Base Table      │    │  ← owns core data rows
│  └────────┬────────────┘    │
│           │ joins           │
│  ┌────────▼────────────┐    │
│  │  Dependency Tables  │    │  ← picklist_value, lookup tables, etc.
│  └─────────────────────┘    │
│                             │
│  Fields: id, name, ...      │  ← each field has a type mapped to a DB column
└────────────┬────────────────┘
             │ foreign-key reference
             ▼
       Another Module's Base Table
```

### Structural rules

1. Every module **must** have a surrogate primary key field named `id` of type `long` (→ `BIGINT`).
2. References to another module are expressed as a `long` foreign-key field pointing to the other module's `id`.
3. Dependency tables (e.g. picklist values) are joined, not embedded; they must not be owned by more than one module.
4. Join direction is always from the depending module to the depended-on module; circular joins are not permitted.

## Module Dependency Map

Modules may declare dependencies on other modules through foreign-key fields.
The permitted direction is: **dependent module → depended-on module**.

Dependency rules:
- A module may depend on one or more other modules via foreign-key fields.
- Dependency direction must be unidirectional; no circular dependencies are allowed.
- Cross-module reads are done through declared joins; a module must never write to another module's base table.

## Module Contracts

Every module exposes a contract that describes its public interface:

- **Exposes** – the record(s) and identifier(s) other modules may read.
- **Consumes** – the modules or dependency tables it reads from.
- **Invariants** – rules that callers must never violate (e.g. a referenced `id` must exist).
- **Breaking-change risks** – changes that would silently break dependent modules.

## Golden Example — Doctor Module

The **Doctor** module illustrates all of the above concepts applied to a single
real-world entity.

**Base table:** `doctor`

| Field Name  | Field Type | DB Column Type | Constraints           | Notes                                              |
|-------------|------------|----------------|-----------------------|----------------------------------------------------|
| id          | long       | BIGINT         | PRIMARY KEY, NOT NULL | Auto-incremented surrogate key                     |
| name        | singleline | VARCHAR(255)   | NOT NULL              | Full name of the doctor                            |
| description | textarea   | TEXT           | NULLABLE              | Free-text biography or notes                       |
| specialist  | picklist   | VARCHAR(100)   | NOT NULL              | Value must exist in the `picklist_value` table     |

**Dependency table:**
- `picklist_value` — supplies the allowed values for the `specialist` picklist field.
- Join: `doctor.specialist = picklist_value.value_key`

**Contract:**
- Exposes: the doctor record identified by `id`.
- Consumes: `picklist_value` for specialist validation.
- Invariants: `id` is unique and immutable; `specialist` must resolve to an entry in `picklist_value`.
- Breaking-change risk: removing a picklist value while doctor records still reference it will leave orphaned keys.

This same structural pattern — base table, dependency tables, join info, and contract — applies to every module in the system.

## Module Inventory

List each module in the table below. Add or update rows as the codebase evolves.

| Module Name | Base Table | Responsibility | Status |
|-------------|------------|----------------|--------|

## Deprecated Modules

| Module Name | Replacement | Removal Target Date |
|-------------|-------------|---------------------|
