# QuickStart Guide: TaskMaster Pro

**Feature**: TaskMaster Pro - Complete Task Management Application  
**Branch**: 001-taskmaster-core  
**Date**: 2026-03-12  
**Target Audience**: Developers new to the TaskMaster Pro codebase

## Overview

This guide walks you through setting up the TaskMaster Pro development environment, running the application locally, and verifying the installation with basic tests. Expected setup time: **30-45 minutes**.

---

## Prerequisites

Before starting, ensure you have the following installed on your development machine:

### Required Software

- **Node.js**: Version 20.x or later ([Download](https://nodejs.org/))
  ```bash
  node --version  # Should output v20.x.x or higher
  ```

- **Python**: Version 3.11 or later ([Download](https://www.python.org/downloads/))
  ```bash
  python --version  # Should output Python 3.11.x or higher
  ```

- **Docker Desktop**: For local MySQL database ([Download](https://www.docker.com/products/docker-desktop))
  ```bash
  docker --version  # Should output Docker version 20.x or higher
  ```

- **Git**: For version control ([Download](https://git-scm.com/downloads))
  ```bash
  git --version
  ```

- **Azure CLI** (Optional, for deployment): ([Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
  ```bash
  az --version
  ```

### Development Tools (Recommended)

- **VS Code** with extensions:
  - Angular Language Service
  - Python
  - Pylance
  - ESLint
  - Prettier
  - GitHub Copilot (required per Constitution Principle III)

---

## Project Structure Overview

```
taskmaster-pro/
├── backend/          # Python FastAPI backend
├── frontend/         # Angular 18 frontend
├── infrastructure/   # Bicep IaC templates
└── specs/            # Feature specifications and documentation
```

---

## Step 1: Clone Repository

```bash
git clone https://github.com/your-org/taskmaster-pro.git
cd taskmaster-pro
git checkout 001-taskmaster-core
```

---

## Step 2: Database Setup (MySQL via Docker)

### Start MySQL Container

```bash
# Start MySQL 8.0 container with persistent volume
docker run --name taskmaster-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=taskmaster \
  -e MYSQL_USER=taskuser \
  -e MYSQL_PASSWORD=taskpass \
  -p 3306:3306 \
  -v taskmaster-data:/var/lib/mysql \
  -d mysql:8.0
```

### Verify Database Connection

```bash
# Connect to MySQL (password: rootpass)
docker exec -it taskmaster-mysql mysql -u root -p

# Inside MySQL shell:
SHOW DATABASES;  # Should list 'taskmaster' database
USE taskmaster;
SHOW TABLES;     # Should be empty (no tables yet)
EXIT;
```

**Alternative**: Use Azure Database for MySQL Flexible Server for cloud-based development (requires Azure subscription).

---

## Step 3: Backend Setup (FastAPI)

### Navigate to Backend Directory

```bash
cd backend
```

### Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install backend dependencies
pip install -r requirements.txt
```

**Expected `requirements.txt` contents** (to be created during implementation):
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.12.1
mysql-connector-python==8.2.0
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
```

### Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# backend/.env
DATABASE_URL=mysql+mysqlconnector://taskuser:taskpass@localhost:3306/taskmaster
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:4200
```

**Important**: Add `.env` to `.gitignore` to prevent committing secrets.

### Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic init src/db/migrations

# Run migrations to create tables
alembic upgrade head
```

**Verify Migration**:
```bash
docker exec -it taskmaster-mysql mysql -u taskuser -p taskmaster -e "SHOW TABLES;"
# Should output: tasks
```

### Start Backend Server

```bash
# Start FastAPI development server with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verify Backend API

Open browser to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check** (if implemented): http://localhost:8000/health

**Test GET /api/tasks** (should return empty array):
```bash
curl http://localhost:8000/api/tasks
# Expected: []
```

**Test POST /api/tasks**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "description": "Quick test from curl",
    "dueDate": "2026-03-20",
    "priority": "Medium",
    "status": "Pending"
  }'
# Expected: Returns created task with id=1
```

---

## Step 4: Frontend Setup (Angular 18)

### Navigate to Frontend Directory

Open a **new terminal** (keep backend running in previous terminal):

```bash
cd frontend
```

### Install Dependencies

```bash
# Install npm packages
npm install
```

**Expected `package.json` key dependencies** (to be created during implementation):
```json
{
  "dependencies": {
    "@angular/core": "^18.0.0",
    "@angular/common": "^18.0.0",
    "@angular/platform-browser": "^18.0.0",
    "rxjs": "^7.8.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "@angular/cli": "^18.0.0",
    "jest": "^29.7.0",
    "typescript": "~5.3.0"
  }
}
```

### Configure Environment

Update `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

### Start Frontend Development Server

```bash
# Start Angular dev server
ng serve
```

**Expected Output**:
```
✔ Browser application bundle generation complete.
✔ Compiled successfully.

** Angular development server running on http://localhost:4200 **
```

### Verify Frontend Application

Open browser to: **http://localhost:4200**

**Expected behavior**:
1. Dashboard loads (may be empty if no tasks)
2. "Create Task" button is visible
3. Status filters (All, Pending, In Progress, Completed) are visible
4. Layout is responsive (test by resizing browser window to 375px width)

---

## Step 5: Run Tests

### Backend Tests (pytest)

In backend terminal:

```bash
cd backend

# Run all tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Expected output:
# ======================== test session starts =========================
# collected X items
# tests/contract/test_get_tasks.py ....                          [ 20%]
# tests/contract/test_create_task.py ....                        [ 40%]
# tests/integration/test_task_lifecycle.py ....                  [ 60%]
# tests/unit/test_task_service.py ........                       [ 100%]
# 
# ---------- coverage: platform win32, python 3.11.x -----------
# Name                          Stmts   Miss  Cover
# -------------------------------------------------
# src/models/task.py               45      0   100%
# src/api/tasks.py                 80      5    94%
# src/services/task_service.py     60      3    95%
# -------------------------------------------------
# TOTAL                           185      8    96%
# ========================= X passed in 5.23s ==========================
```

**View HTML Coverage Report**:
```bash
# Open in browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
```

### Frontend Tests (Jest)

In frontend terminal:

```bash
cd frontend

# Run all tests with coverage
npm test -- --coverage

# Expected output:
# PASS  src/app/features/dashboard/dashboard.component.spec.ts
# PASS  src/app/core/services/task.service.spec.ts
# PASS  src/app/features/task-form/task-form.component.spec.ts
# 
# Test Suites: 8 passed, 8 total
# Tests:       45 passed, 45 total
# Coverage:    Statements: 85% | Branches: 82% | Functions: 88% | Lines: 84%
```

---

## Step 6: Common Development Tasks

### Create a New Task (via UI)

1. Navigate to http://localhost:4200
2. Click "Create Task" button
3. Fill form:
   - Title: "My First Task"
   - Description: "Testing TaskMaster Pro"
   - Due Date: Select tomorrow's date
   - Priority: High
   - Status: Pending
4. Click "Submit"
5. Verify task appears in dashboard

### Filter Tasks by Status

1. Click "Pending" filter button
2. Verify only pending tasks display
3. Click "All" to show all tasks

### Mark Task as Completed (via Checkbox)

1. Find a pending task in the dashboard
2. Click the checkbox next to the task
3. Verify task status updates to "Completed" immediately

### Edit a Task

1. Click "Edit" button on any task
2. Modify any field (e.g., change priority to "Low")
3. Click "Save"
4. Verify changes persist

### Delete a Task

1. Click "Delete" button on any task
2. Confirmation modal appears: "Are you sure you want to delete this task?"
3. Click "Confirm"
4. Verify task is removed from dashboard

---

## Step 7: Debug and Troubleshooting

### Backend Issues

**Issue**: Database connection error
```
sqlalchemy.exc.OperationalError: (mysql.connector.errors.DatabaseError) 2003
```
**Solution**: Verify MySQL container is running:
```bash
docker ps | grep taskmaster-mysql
# If not running:
docker start taskmaster-mysql
```

**Issue**: Import errors for SQLAlchemy models
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend Issues

**Issue**: `ng` command not found
**Solution**: Install Angular CLI globally:
```bash
npm install -g @angular/cli@18
```

**Issue**: CORS errors when calling backend API
**Solution**: Verify `CORS_ORIGINS` in backend `.env` includes `http://localhost:4200`

**Issue**: TailwindCSS styles not applying
**Solution**: Ensure `tailwind.config.js` is present and `styles.css` imports Tailwind:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Common Development Commands

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload                    # Start dev server
pytest --cov=src                                 # Run tests with coverage
alembic revision --autogenerate -m "description" # Create migration
alembic upgrade head                             # Apply migrations
black src/                                       # Format code
flake8 src/                                      # Lint code

# Frontend
cd frontend
ng serve                                # Start dev server
ng test --coverage                      # Run tests with coverage
ng build                                # Build for production
ng lint                                 # Lint code
npm run format                          # Format code (if configured)
```

---

## Step 8: Using GitHub Copilot (Required per Constitution)

### Enable Copilot in VS Code

1. Install GitHub Copilot extension
2. Sign in with GitHub account (requires Copilot subscription)
3. Verify Copilot is active (icon in bottom right of VS Code)

### Example Copilot Prompts

**Generate Angular Component**:
```typescript
// Prompt: Create a TaskItemComponent that displays a single task with checkbox and edit/delete buttons
// Copilot will generate component structure
```

**Generate Pytest Test**:
```python
# Prompt: Generate pytest contract test for POST /api/tasks endpoint that validates request/response schema
# Copilot will generate test function
```

**Generate Documentation**:
```python
# Prompt: Add comprehensive docstring for this function explaining parameters and return value
def create_task(task_data: TaskCreate) -> Task:
    # Copilot will generate docstring
```

---

## Next Steps

✅ **Quickstart Complete** - You now have a fully functional local development environment!

### Recommended Next Actions

1. **Read Specifications**:
   - [Feature Specification](../spec.md) - User stories and requirements
   - [Implementation Plan](../plan.md) - Technical architecture
   - [Data Model](../data-model.md) - Database schema and entity details
   - [API Contracts](../contracts/) - OpenAPI spec and JSON schemas

2. **Explore Codebase**:
   - Backend: `backend/src/api/tasks.py` - API endpoints
   - Frontend: `frontend/src/app/features/dashboard/` - Main dashboard component
   - Tests: `backend/tests/` and `frontend/tests/` - Test examples

3. **Implement User Stories**:
   - Follow TDD workflow (write tests first!)
   - Use GitHub Copilot for code generation
   - Maintain 80% test coverage minimum
   - Reference Constitution for compliance

4. **Deploy to Azure** (when ready):
   - Follow deployment guide in `infrastructure/README.md` (to be created)
   - Use Bicep templates to provision Azure resources
   - Configure GitHub Actions for CI/CD

---

## Support and Resources

### Documentation
- **Constitution**: `.specify/memory/constitution.md` - Governing principles
- **Research**: `specs/001-taskmaster-core/research.md` - Technology decisions
- **OpenAPI Docs**: http://localhost:8000/docs (when backend running)

### External Resources
- [Angular 18 Documentation](https://angular.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Azure Container Apps Documentation](https://learn.microsoft.com/en-us/azure/container-apps/)

### Getting Help
- Check existing issues in GitHub repository
- Review specification documents for requirements
- Use GitHub Copilot for code assistance
- Consult team members or tech lead

---

**Last Updated**: 2026-03-12  
**Branch**: 001-taskmaster-core  
**Status**: Ready for development
