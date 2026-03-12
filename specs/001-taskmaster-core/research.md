# Research: TaskMaster Pro Technology Decisions and Best Practices

**Feature**: TaskMaster Pro - Complete Task Management Application  
**Branch**: 001-taskmaster-core  
**Phase**: 0 - Technology Research  
**Date**: 2026-03-12

## Executive Summary

All technology decisions for TaskMaster Pro are predefined by the **TaskMaster Pro Constitution v1.0.0**. This research document consolidates the rationale, best practices, and integration patterns for the mandated Azure-native stack: Angular 18, Python FastAPI, Azure Database for MySQL Flexible Server, and Azure Container Apps deployment.

**Key Finding**: Zero unknowns or clarifications needed - all technical context is fully specified by constitution compliance.

---

## Technology Decisions

### Frontend: Angular 18 + TypeScript + TailwindCSS

**Decision**: Angular 18 with TypeScript (strict mode) and TailwindCSS for styling

**Rationale** (from Constitution Principle IV: Mobile-First Responsive Design):
- Angular 18 provides modern standalone components, signals, and improved performance
- TypeScript strict mode ensures type safety and catches errors at compile time
- TailwindCSS enables mobile-first responsive design with utility classes
- Built-in dependency injection and RxJS for reactive state management

**Best Practices**:
1. **Standalone Components**: Use Angular 18 standalone components to reduce boilerplate and NgModule complexity
2. **Signals for State**: Leverage Angular Signals for reactive state management (filters, task list updates)
3. **OnPush Change Detection**: Use `ChangeDetectionStrategy.OnPush` for performance optimization
4. **Lazy Loading**: Implement route-based lazy loading for features (if expanded beyond single dashboard)
5. **RxJS Best Practices**:
   - Use `takeUntilDestroyed()` for automatic subscription cleanup
   - Prefer `async` pipe in templates over manual subscriptions
   - Use subjects sparingly, prefer signals where possible
6. **TailwindCSS Mobile-First**:
   - Default styles for mobile (375px minimum width)
   - Use `sm:`, `md:`, `lg:`, `xl:` breakpoints for progressive enhancement
   - Minimum touch targets: `w-11 h-11` (44×44px) for buttons/checkboxes
7. **Accessibility**:
   - Use semantic HTML elements
   - Include ARIA labels for interactive elements
   - Ensure keyboard navigation works for all actions

**Alternatives Considered**: None - Angular 18 mandated by Constitution

---

### Backend: Python 3.11+ FastAPI + Pydantic

**Decision**: FastAPI with Pydantic for data validation and type safety

**Rationale** (from Constitution Principle V: API Contract Compliance):
- FastAPI auto-generates OpenAPI/Swagger documentation
- Pydantic provides TypeScript-style typing and validation for Python
- Async support enables high-performance I/O operations
- Built-in dependency injection for database sessions and services

**Best Practices**:
1. **Pydantic Models**:
   - Define separate models for request/response schemas
   - Use `TaskCreate`, `TaskUpdate`, `TaskResponse` schemas
   - Leverage Pydantic validators for business rules (e.g., due date validation)
2. **Dependency Injection**:
   - Use FastAPI's `Depends()` for database session management
   - Create reusable dependencies for common operations
3. **Error Handling**:
   - Use `HTTPException` for API errors with appropriate status codes
   - Implement global exception handlers for unexpected errors
   - Return consistent error response format: `{"detail": "error message"}`
4. **Async/Await**:
   - Use async database operations with `asyncpg` or async MySQL driver
   - Prefer `async def` for all route handlers
5. **CORS Configuration**:
   - Enable CORS for frontend origin (localhost during dev, Azure Container Apps domain in prod)
   - Restrict allowed origins in production
6. **Database Best Practices**:
   - Use SQLAlchemy 2.0+ with async support
   - Implement database connection pooling
   - Use Alembic for schema migrations
   - Always use parameterized queries (SQLAlchemy ORM handles this)

**Alternatives Considered**: None - FastAPI mandated by Constitution

---

### Database: Azure Database for MySQL Flexible Server

**Decision**: Azure Database for MySQL Flexible Server

**Rationale** (from Constitution Principle I: Azure-Native Architecture):
- Fully managed MySQL service with automatic backups and high availability
- Seamless integration with Azure Monitor and Application Insights
- Private network connectivity with Azure Container Apps via VNet integration
- Support for burstable compute tiers for cost optimization

**Best Practices**:
1. **Schema Design**:
   - Use InnoDB storage engine (default for MySQL 8.0+)
   - Define indexes on frequently queried columns (`status`, `dueDate`)
   - Implement foreign key constraints even with single entity (future-proof)
2. **Connection Management**:
   - Use connection pooling via SQLAlchemy (max 10-20 connections for small apps)
   - Set appropriate timeouts and retries for resilience
   - Use SSL/TLS for database connections
3. **Security**:
   - Enable Azure AD authentication for MySQL
   - Use managed identities for connection from Container Apps
   - Restrict network access to Azure VNet only (no public internet)
4. **Performance**:
   - Enable query performance insights in Azure portal
   - Use read replicas for read-heavy workloads (future optimization)
   - Configure appropriate innodb_buffer_pool_size
5. **Migrations**:
   - Use Alembic for schema versioning
   - Test migrations in dev environment first
   - Always create backward-compatible migrations

**Schema for Task Entity**:
```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    priority VARCHAR(50) NOT NULL CHECK (priority IN ('Low', 'Medium', 'High')),
    status VARCHAR(50) NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_due_date (due_date),
    INDEX idx_status_due_date (status, due_date)
);
```

**Alternatives Considered**: None - Azure MySQL Flexible Server mandated by Constitution

---

### Reminders: Azure Logic Apps or Azure Functions

**Decision**: Azure Functions with Timer Trigger (recommended over Logic Apps for this use case)

**Rationale**:
- **Azure Functions** offers more flexibility for custom logic in Python
- Timer trigger can run hourly to check for tasks due in next 24 hours
- Direct access to Azure MySQL via connection string
- Lower cost for simple scheduled tasks
- Easier local testing and debugging

**Best Practices**:
1. **Timer Configuration**:
   - Cron expression: `0 0 * * * *` (run at the top of every hour)
   - Use `schedule` decorator: `@app.schedule(schedule="0 0 * * * *", arg_name="timer")`
2. **Reminder Logic**:
   - Query tasks where `due_date = CURDATE() + INTERVAL 1 DAY` and status != 'Completed'
   - Track sent reminders in database (add `reminder_sent` boolean field)
   - Implement idempotency to prevent duplicate reminders
3. **Notification Delivery**:
   - Phase 1: Log reminder to Application Insights (placeholder)
   - Future: Integrate with Azure Communication Services for email/SMS
   - Future: Implement in-app notifications via SignalR
4. **Error Handling**:
   - Retry on transient database connection failures
   - Log failures to Application Insights
   - Set up Azure Monitor alerts for function failures

**Alternative Considered**:
- **Azure Logic Apps**: More visual, but overkill for simple hourly query + notification logic
- **Decision**: Use Azure Functions for better code reusability and testability

---

### Deployment: Azure Container Apps + GitHub Actions + Bicep

**Decision**: Dual-container deployment on Azure Container Apps orchestrated via GitHub Actions with Bicep IaC

**Rationale** (from Constitution Principle I: Azure-Native Architecture):
- Azure Container Apps provides serverless container hosting with automatic scaling
- GitHub Actions enables CI/CD with native Azure integration
- Bicep provides declarative infrastructure as code with strong typing
- Single environment for both frontend and backend containers

**Best Practices**:

#### Azure Container Apps
1. **Container Configuration**:
   - Frontend container: Nginx serving Angular static build
   - Backend container: Uvicorn running FastAPI application
   - Use multi-stage Docker builds to minimize image size
2. **Environment Variables**:
   - Store database connection strings in Azure Key Vault
   - Reference secrets via Container Apps secret management
   - Use separate configurations for dev/staging/prod
3. **Scaling**:
   - Configure horizontal autoscaling: min 1, max 5 replicas
   - Scale based on HTTP requests or CPU utilization
   - Backend: Scale on concurrent requests
   - Frontend: Typically static, scale conservatively
4. **Networking**:
   - Use VNet integration for private MySQL access
   - Enable ingress with external traffic for frontend/backend
   - Configure custom domain with SSL/TLS certificate

#### GitHub Actions CI/CD
1. **CI Pipeline** (on pull requests):
   - Backend: Run pytest with coverage report, linting (flake8/black)
   - Frontend: Run Jest with coverage report, build check, linting (ESLint)
   - Fail PR if coverage < 80%
2. **CD Pipeline** (on merge to main):
   - Build Docker images for frontend and backend
   - Push images to Azure Container Registry
   - Update Container Apps with new image tags
   - Run smoke tests against deployed endpoints
3. **Secrets Management**:
   - Store Azure credentials as GitHub secrets
   - Use workload identity federation for secure auth
   - Never commit connection strings or API keys

#### Bicep Infrastructure
1. **Module Structure**:
   - `main.bicep`: Orchestrates all modules
   - `modules/container-apps.bicep`: Defines frontend/backend containers
   - `modules/mysql.bicep`: Provisions MySQL Flexible Server
   - `modules/container-registry.bicep`: Sets up ACR
   - `modules/monitoring.bicep`: Configures Application Insights
2. **Parameters**:
   - Use parameter files for environment-specific configs
   - Define outputs for connection strings and endpoints
3. **Best Practices**:
   - Use symbolic names for resources
   - Implement resource tags for cost tracking
   - Define dependencies explicitly with `dependsOn`
   - Use user-assigned managed identities for container apps

**Alternatives Considered**: None - GitHub Actions + Bicep mandated by Constitution

---

## Testing Strategy

### Test-Driven Development Workflow (from Constitution Principle II)

**Mandatory Process**:
1. **Write Test First**: Create failing test for new feature
2. **Get Approval**: Review test with team/stakeholder
3. **Confirm Failure**: Run test suite, verify new test fails
4. **Implement**: Write minimum code to make test pass
5. **Verify Pass**: Run test suite, verify new test passes
6. **Refactor**: Clean up code while keeping tests green
7. **Coverage Check**: Ensure 80% coverage maintained

### Backend Testing (pytest)
1. **Contract Tests** (`tests/contract/`):
   - Test each API endpoint against OpenAPI specification
   - Validate request/response schemas match Pydantic models
   - Test HTTP status codes and error messages
   - Use `pytest-httpx` for mocking API responses
2. **Integration Tests** (`tests/integration/`):
   - Test complete user journeys (create → edit → delete task)
   - Use real database (Docker MySQL container for tests)
   - Test reminder scheduling flow end-to-end
3. **Unit Tests** (`tests/unit/`):
   - Test Pydantic validators in isolation
   - Test business logic in services (status transitions, date validation)
   - Mock database dependencies with `pytest-mock`
4. **Coverage**:
   - Use `pytest-cov` to generate coverage reports
   - Enforce 80% minimum via `--cov-fail-under=80`
   - Generate HTML reports for visualization

### Frontend Testing (Jest)
1. **Component Tests**:
   - Test Angular components in isolation
   - Mock HttpClient and services
   - Test user interactions (button clicks, form submissions)
   - Use Angular Testing Library for accessibility testing
2. **Service Tests**:
   - Test TaskService HTTP methods
   - Mock HttpClient responses
   - Test error handling and retry logic
3. **Integration Tests**:
   - Test component + service integration
   - Simulate real API responses
   - Test state management (filters, task list updates)
4. **Coverage**:
   - Configure Jest with `coverageThreshold: { global: { branches: 80, functions: 80, lines: 80 } }`
   - Generate LCOV reports for CI/CD integration

---

## GitHub Copilot Integration (from Constitution Principle III)

**Mandatory Usage**:
1. **Code Generation**:
   - Use Copilot to generate boilerplate Angular components
   - Use Copilot to generate FastAPI endpoint stubs
   - Use Copilot for Pydantic model creation
2. **Test Generation**:
   - Prompt: "Generate pytest contract test for POST /api/tasks endpoint"
   - Prompt: "Generate Jest test for TaskFormComponent form validation"
3. **Documentation**:
   - Use Copilot to generate inline comments
   - Prompt: "Add docstring explaining this Pydantic validator"
   - Prompt: "Generate JSDoc for this Angular service method"
4. **Refactoring**:
   - Use Copilot suggestions for code improvements
   - Review and accept/reject suggestions based on alignment with best practices

**Comment Standards**:
- All complex functions MUST have explanatory comments
- Mark Copilot-generated code with: `// Generated with GitHub Copilot` or `# Generated with GitHub Copilot`
- Document any complex Copilot prompts used: `// Copilot prompt: "Generate async validator for unique task titles"`

---

## Integration Patterns

### Frontend-Backend Communication
1. **API Client Service** (`task.service.ts`):
   - Use Angular HttpClient with RxJS observables
   - Implement retry logic with exponential backoff (`retry`, `retryWhen`)
   - Handle errors globally with `HttpInterceptor`
2. **State Management**:
   - Use Angular Signals for task list state
   - Implement filter state with BehaviorSubject or Signals
   - Optimistic updates: Update UI before API confirms
3. **Error Handling**:
   - Show user-friendly error messages (toast notifications)
   - Distinguish between network errors (503) and validation errors (400)
   - Implement retry UI for failed operations

### Backend-Database Communication
1. **Repository Pattern** (optional, but recommended):
   - Create `TaskRepository` class for database operations
   - Keeps business logic in services, data access in repositories
   - Easier to mock for unit testing
2. **Async Operations**:
   - Use `async with` for database sessions
   - Implement connection pooling via SQLAlchemy
3. **Transaction Management**:
   - Use database transactions for multi-step updates
   - Implement rollback on errors

---

## Security Considerations

1. **API Security**:
   - Implement rate limiting (future enhancement)
   - Validate all inputs with Pydantic
   - Use HTTPS only in production (enforce via Container Apps)
2. **Database Security**:
   - Use parameterized queries (SQLAlchemy ORM)
   - Encrypt connections with SSL/TLS
   - Use managed identities for authentication
3. **Frontend Security**:
   - Sanitize user inputs (Angular sanitizes by default)
   - Implement Content Security Policy headers
   - Use Angular's built-in XSS protection

---

## Performance Optimization

1. **Frontend**:
   - Lazy load routes (if application grows)
   - Implement virtual scrolling for large task lists (>100 tasks)
   - Use OnPush change detection
   - Optimize bundle size with tree shaking
2. **Backend**:
   - Implement database query optimization (indexes on status, due_date)
   - Use async operations to handle concurrent requests
   - Cache frequently accessed data (optional, for future)
3. **Database**:
   - Create composite indexes for common query patterns
   - Monitor query performance with Azure insights
   - Optimize connection pool size

---

## Development Environment Setup

1. **Local Development**:
   - Frontend: `ng serve` on port 4200
   - Backend: `uvicorn main:app --reload` on port 8000
   - Database: Docker MySQL container or Azure MySQL dev instance
2. **Environment Variables**:
   - Use `.env` files for local development (gitignored)
   - Use Azure Container Apps environment variables in production
3. **Prerequisites**:
   - Node.js 20+ (for Angular 18)
   - Python 3.11+
   - Docker Desktop (for local MySQL)
   - Azure CLI (for deployment)

---

## Unknowns Resolved

**Total NEEDS CLARIFICATION markers**: 0

All technical decisions are defined by the TaskMaster Pro Constitution v1.0.0. No research required for technology selection - all choices are mandated and justified by constitutional principles.

---

## Next Steps

✅ **Phase 0 Complete** - All technology decisions documented  
➡️ **Phase 1**: Generate data-model.md, contracts/, quickstart.md  
➡️ **Phase 1**: Update agent context with technology decisions  
➡️ **Phase 2**: Generate tasks.md from implementation plan
