<!--
SYNC IMPACT REPORT
==================
Version Change: Initial → 1.0.0
Modified Principles: N/A (initial constitution)
Added Sections:
  - Core Principles (5 principles defined)
    I. Azure-Native Architecture
    II. Test-Driven Development (NON-NEGOTIABLE)
    III. AI-Assisted Development
    IV. Mobile-First Responsive Design
    V. API Contract Compliance
  - Technology Stack Constraints
  - Development Workflow
  - Governance
Removed Sections: N/A

Templates Requiring Updates:
  ✅ constitution.md (this file) - created v1.0.0
  ✅ spec-template.md - reviewed, no changes needed (generic structure compatible)
  ✅ plan-template.md - reviewed, no changes needed (Constitution Check section is flexible)
  ✅ tasks-template.md - reviewed, no changes needed (already emphasizes TDD workflow)
  ✅ README.md - reviewed, minimal content, no references to update

Follow-up TODOs: None - all placeholders resolved
-->

# TaskMaster Pro Constitution

## Core Principles

### I. Azure-Native Architecture

All infrastructure, services, and deployment pipelines MUST use Azure-native solutions exclusively. This principle ensures consistent operations, unified monitoring, and optimal integration within the Azure ecosystem.

**Requirements**:
- Frontend hosting: Azure Container Apps (Angular 18 container)
- Backend hosting: Azure Container Apps (FastAPI container)
- Database: Azure Database for MySQL Flexible Server only
- Scheduled tasks: Azure Logic Apps or Azure Functions with timer triggers
- Deployment: GitHub Actions with Bicep templates for Infrastructure as Code
- No hybrid cloud or non-Azure services permitted without documented exception

**Rationale**: Azure-native architecture minimizes integration complexity, provides unified security and compliance posture, and enables seamless use of Azure-managed services for observability, scaling, and disaster recovery.

### II. Test-Driven Development (NON-NEGOTIABLE)

TDD is mandatory for all features. Tests MUST be written first, reviewed, confirmed to fail, and only then implemented. This ensures specifications are testable and implementation meets exact requirements.

**Requirements**:
- Write tests before implementation (Red-Green-Refactor cycle)
- 80% minimum code coverage for backend (pytest) and frontend (Jest)
- All tests generated/reviewed by GitHub Copilot
- Contract tests for all API endpoints (GET /api/tasks, POST /api/tasks, PUT /api/tasks/:id, DELETE /api/tasks/:id)
- Integration tests for complete user journeys
- Unit tests for business logic, validators, and services

**Rationale**: TDD catches requirements ambiguities early, ensures code is testable by design, provides living documentation through tests, and maintains high code quality through regression protection.

### III. AI-Assisted Development

All code, tests, and documentation MUST be generated or refactored with GitHub Copilot assistance. This principle ensures consistency, accelerates development, and leverages AI best practices.

**Requirements**:
- All new code generated using GitHub Copilot
- All refactoring performed with Copilot assistance
- Comprehensive inline comments explaining AI-generated logic
- Copilot-generated unit tests for all business logic
- Document AI prompts and constraints in code comments where complex generation occurred

**Rationale**: AI-assisted development increases velocity, maintains consistent coding patterns, reduces human error, and ensures best practices are applied through trained models.

### IV. Mobile-First Responsive Design

All UI components MUST be designed for mobile devices first, then progressively enhanced for tablets and desktops. This ensures accessibility and optimal experience across all screen sizes.

**Requirements**:
- TailwindCSS utility-first responsive breakpoints (sm:, md:, lg:, xl:)
- Touch-friendly interactive elements (minimum 44×44px tap targets)
- Responsive layouts using Flexbox/Grid with mobile breakpoint as default
- Test on mobile viewport (375px width minimum) before desktop
- Optimized for performance on mobile networks (lazy loading, code splitting)

**Rationale**: Mobile traffic dominates modern web usage. Mobile-first ensures core functionality works under the most constrained conditions, improving experience for all users.

### V. API Contract Compliance

All frontend-backend communication MUST strictly adhere to the documented API contract. Endpoints, request/response schemas, and HTTP methods are immutable without versioning.

**Requirements**:
- **GET /api/tasks**: Retrieve all tasks (supports status filtering via query params)
- **POST /api/tasks**: Create new task (requires title, description, dueDate, priority, status)
- **PUT /api/tasks/:id**: Update existing task (full resource update)
- **DELETE /api/tasks/:id**: Delete task (requires confirmation)
- Pydantic models enforce TypeScript-style typing on backend
- OpenAPI/Swagger documentation auto-generated from FastAPI routes
- Contract tests validate request/response schemas match specification

**Rationale**: Strict API contracts prevent integration bugs, enable parallel frontend/backend development, provide clear boundaries for testing, and support future API versioning strategies.

## Technology Stack Constraints

**MANDATORY**: The following technology choices are immutable and MUST be used for all implementations:

**Frontend**:
- Angular 18 (latest stable)
- TypeScript (strict mode enabled)
- TailwindCSS for styling (no custom CSS frameworks)
- Jest for unit testing
- Azure Container Apps for deployment

**Backend**:
- Python 3.11+ with FastAPI framework
- Pydantic for data validation and TypeScript-style typing
- pytest for testing (with pytest-cov for coverage reports)
- Azure Container Apps for deployment

**Database**:
- Azure Database for MySQL Flexible Server
- Migrations managed via Alembic (SQLAlchemy) or similar

**DevOps**:
- GitHub Actions for CI/CD pipeline
- Bicep for Infrastructure as Code (no Terraform/ARM templates)
- Azure Container Registry for image storage
- Automated deployment on merge to main branch

**Observability**:
- Azure Monitor for infrastructure monitoring
- Application Insights for application telemetry
- Structured logging (JSON format) in all services

**Exceptions**: Any deviation from this stack MUST be documented in the feature specification with explicit rationale and architectural review approval.

## Development Workflow

**Feature Specifications**: Every feature begins with a specification document following the `.specify/templates/spec-template.md` format. Specifications MUST include:
- User scenarios with acceptance criteria (Given-When-Then format)
- Functional requirements matching PDF requirements document
- Success criteria with measurable outcomes
- Edge cases and error handling scenarios

**Implementation Planning**: All features require an implementation plan (`.specify/templates/plan-template.md`) that includes:
- Constitution compliance check before Phase 0 research
- Technical context capturing stack decisions
- Project structure aligned with dual-container deployment model
- Complexity justification for any deviations

**Task Execution**: Tasks are generated from plans using `.specify/templates/tasks-template.md` and MUST:
- Be organized by user story priority (P1, P2, P3)
- Include TDD test tasks before implementation tasks
- Specify exact file paths for all work items
- Mark parallelizable tasks with [P] prefix
- Reference dependency relationships explicitly

**Quality Gates**:
- Tests written and failing before implementation begins
- 80% minimum coverage before PR approval
- No console.log or print statements in production code (use structured logging)
- All API endpoints documented in OpenAPI spec
- Responsive design verified on mobile (375px), tablet (768px), desktop (1024px+)

**Code Review**:
- All PRs require constitution compliance verification
- GitHub Copilot-generated code MUST include explanatory comments
- Test coverage reports automatically attached to PRs
- Breaking changes require API versioning and migration plan

## Governance

**Authority**: This constitution supersedes all other development practices, coding standards, and architectural decisions. All features, code reviews, and deployment pipelines MUST verify compliance with these principles.

**Amendment Process**:
- Proposed amendments require documented rationale and impact analysis
- Version bumps follow semantic versioning:
  - **MAJOR**: Backward-incompatible principle changes (e.g., removing Azure-native requirement)
  - **MINOR**: New principles or material expansions (e.g., adding security principle)
  - **PATCH**: Clarifications, wording fixes, non-semantic updates
- All amendments MUST update dependent templates (spec, plan, tasks) and sync impact report
- Migration plans required for any principle changes affecting existing code

**Compliance Verification**:
- Constitution check is Phase 0 gate in all implementation plans
- CI/CD pipeline enforces test coverage, linting, and API contract validation
- Feature specifications reference specific principles they satisfy
- Quarterly constitution review to validate ongoing relevance

**Deferred Decisions**: Any placeholder or TODO items MUST be tracked in project issues and resolved before features depending on them proceed to implementation.

**Version**: 1.0.0 | **Ratified**: 2026-03-12 | **Last Amended**: 2026-03-12
