# Platform Knowledge

Purpose: Capture runtime, language, framework, and infrastructure knowledge
that agents must apply when analyzing or designing for this platform.
Update this file whenever the platform stack changes.

## Runtime and Language

- Language: Java (server-side), JavaScript (frontend/WebContent)
- Runtime version: JDK 11+ (see `build/build.xml` and `zohodesk.iml` for compile targets)
- Package manager: Gradle (see `build/gradle/`) and Apache Ant (`build/build.xml`)
- Build tool: Ant (`build/antfile.xml`, `build/build.xml`) + Gradle wrapper (`build/gradle/`)

## Frameworks and Libraries

- Web / API framework: Java Servlet-based (custom Zoho framework); REST resources in
  `com.zoho.support.restapi.*`
- ORM / query builder: Custom JDBC-based data access layer (`FieldDBStore`, `FieldDBAPIImpl`)
- Validation library: Custom validators (`BasicFieldValidator`, `AbstractFieldValueValidator`)
- Authentication library: Internal Zoho auth (OAuth for MCP/external integrations)
- Testing framework: JUnit (see `JUnitTests/`), Mockito (see `mockito-extensions/`),
  Cucumber for acceptance tests (`acceptanceTests/cucumber/`, `apiTests/cucumber/`)
- Task / job queue: Internal scheduler beans (e.g. `CustomFieldDeletionBean`, `UniqueFieldScheduler`)

## Infrastructure

- Hosting environment: Zoho on-premise / private cloud data centers
- Container runtime: Docker (see `build/Dockerfile`)
- Orchestration: Internal Zoho deployment tooling
- Service discovery / API gateway: Internal Zoho service mesh

## Persistence

- Primary database engine and version: MySQL (versions vary by deployment region;
  use `SELECT VERSION()` in diagnostic queries to confirm)
- Secondary / caching stores: Internal Zoho cache layer (not directly exposed to agents)
- Migration tooling: Custom migration scripts under `migration/` directory
- Connection-pool configuration: Managed by Zoho platform runtime; not agent-configurable

## Platform-Level Constraints

- Known runtime limits: Java heap configured per deployment; avoid loading unbounded field sets
  without pagination or predicate filtering
- Deployment pipeline: Zoho internal CI/CD; zero-downtime deployments expected
- Regulated data residency: Data residency rules apply per customer region (EU, US, AU, IN, etc.)

## Integration Points

- External APIs consumed: Zoho CRM, Zoho Accounts, Zoho Analytics (via internal Zoho SDKs)
- External APIs exposed: Zoho Desk REST API (public + internal)
- Event bus or message broker: Internal Zoho event/micros framework
- Third-party SaaS dependencies: None directly in this repository

## Platform Conventions

- Logging format: Internal Zoho logging framework (structured log entries with correlation IDs)
- Standard error response shape: JSON `{ "errorCode": "...", "message": "...", "status": ... }`
- API versioning strategy: URL-path versioned (`/api/v1/`, internal APIs may be unversioned)
- Feature flag mechanism: Internal Zoho feature toggle system (not exposed in this repository)

## Key Package Roots

- Core field framework: `com.zoho.support.core.fields`
- REST API resources: `com.zoho.support.restapi`
- Common utilities: `com.adventnet.support.common.util`
- Module/department: `com.zoho.support.core.modules`, `com.zoho.support.core.department`
- Source root: `source/` (Java source files)
- Web content root: `WebContent/` (JSPs, JS, CSS)
- Build output: `bin/` (compiled classes)
