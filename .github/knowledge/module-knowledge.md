# Module Knowledge

Purpose: Document the names, responsibilities, ownership boundaries, and
inter-module contracts for every major module in the system.
Agents use this file to avoid re-discovering module structure on every run.

## Module Inventory

List each module in the table below. Add or update rows as the codebase evolves.

| Module Name | Path | Responsibility | Owner Team | Status |
|-------------|------|----------------|------------|--------|
| (example)   | src/ | (brief description) | (team) | Active |

## Module Dependency Map

Describe the permitted dependency direction between modules.
List only intentional, approved dependencies.

- (module-a) -> (module-b): reason
- (module-b) -> (module-c): reason

## Module Contracts

For each module that exposes an interface to other modules, document the contract.

### (Module Name)

- Exposes: (public interface, event, or API surface)
- Consumes: (interfaces or events it depends on)
- Invariants: (rules that must never be violated by callers)
- Known breaking-change risks: (anything fragile in the current contract)

## Cross-Cutting Modules

List modules that are used by almost all other modules (utilities, logging, config, etc.)
and their permitted usage rules.

- (module-name): (permitted usage, any restrictions)

## Deprecated Modules

List modules that are no longer active and should not be used in new code.

| Module Name | Replacement | Removal Target Date |
|-------------|-------------|---------------------|
