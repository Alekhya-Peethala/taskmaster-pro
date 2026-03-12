# Tasks: TaskMaster Pro - Complete Task Management Application

**Feature Branch**: `001-taskmaster-core`  
**Generated**: 2026-03-12  
**Input**: Design documents from `/specs/001-taskmaster-core/`

**Prerequisites**: 
- ✅ plan.md (tech stack, project structure)
- ✅ spec.md (5 user stories with priorities P1-P5)
- ✅ data-model.md (Task entity schema)
- ✅ contracts/ (openapi.yaml, task-schema.json)
- ✅ research.md (technology decisions)
- ✅ quickstart.md (developer onboarding)

**Tests**: ✅ INCLUDED - All tasks follow Test-Driven Development per Constitution Principle II (80% minimum coverage)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **Checkbox**: `- [ ]` (task not started)
- **[ID]**: Task identifier (T001, T002, T003...)
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3...) - only for user story phases
- **Description**: Clear action with exact file path

**Path Conventions** (from plan.md):
- Backend: `backend/src/`, `backend/tests/`
- Frontend: `frontend/src/`, `frontend/src/app/`
- Infrastructure: `infrastructure/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure with src/ and tests/ subdirectories
- [X] T002 Initialize Python project with pyproject.toml and requirements.txt in backend/
- [X] T003 [P] Create frontend directory structure with Angular 18 workspace in frontend/
- [X] T004 [P] Initialize Angular 18 project with standalone components and TailwindCSS configuration
- [X] T005 [P] Create infrastructure directory with Bicep template structure in infrastructure/
- [X] T006 [P] Configure pytest with pytest.ini and coverage settings in backend/pytest.ini
- [X] T007 [P] Configure Jest with jest.config.js and coverage thresholds in frontend/jest.config.js
- [X] T008 [P] Setup ESLint and Prettier for TypeScript in frontend/.eslintrc.json
- [X] T009 [P] Setup Pylint/Black for Python in backend/.pylintrc
- [X] T010 Create .gitignore files for Python (backend/) and Node.js (frontend/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T011 Create database connection module in backend/src/database.py with SQLAlchemy engine and session factory
- [X] T012 [P] Create Alembic configuration in backend/alembic.ini and backend/alembic/env.py
- [X] T013 [P] Create initial Alembic migration for tasks table in backend/alembic/versions/001_create_tasks_table.py
- [X] T014 [P] Create Task SQLAlchemy model in backend/src/models/task.py with all fields and constraints
- [X] T015 [P] Create Pydantic schemas in backend/src/models/schemas.py (TaskBase, TaskCreate, TaskUpdate, TaskResponse)
- [X] T016 [P] Create TypeScript Task interfaces in frontend/src/app/models/task.model.ts
- [X] T017 Create FastAPI application instance in backend/src/main.py with CORS middleware
- [X] T018 [P] Create Angular environment configuration in frontend/src/environments/ (development and production)
- [X] T019 [P] Create backend error handling middleware in backend/src/middleware/error_handler.py
- [X] T020 [P] Create Angular HTTP interceptor for error handling in frontend/src/app/interceptors/error.interceptor.ts
- [X] T021 [P] Create backend logging configuration in backend/src/logging_config.py
- [X] T022 [P] Setup Docker Compose for local MySQL in docker-compose.yml at repository root
- [X] T023 Create backend .env.example with database connection string and environment variables

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Filter Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can see all their tasks in a dashboard view with the ability to filter by status (Pending, In Progress, Completed)

**Independent Test**: Seed the database with sample tasks of different statuses, load the dashboard, and verify all tasks display correctly with working status filters that show/hide tasks appropriately.

### Tests for User Story 1 (TDD: Write FIRST, verify FAIL)

- [X] T024 [P] [US1] Contract test for GET /api/tasks in backend/tests/contract/test_tasks_get.py
- [X] T025 [P] [US1] Contract test for GET /api/tasks?status=Pending in backend/tests/contract/test_tasks_filter.py
- [X] T026 [P] [US1] Unit test for TaskService.get_all_tasks() in backend/tests/unit/test_task_service.py
- [X] T027 [P] [US1] Unit test for TaskService.get_tasks_by_status() in backend/tests/unit/test_task_service.py
- [X] T028 [P] [US1] Integration test for dashboard loading workflow in frontend/src/app/components/task-dashboard/task-dashboard.component.spec.ts
- [X] T029 [P] [US1] Integration test for status filter interaction in frontend/src/app/components/task-filter/task-filter.component.spec.ts

### Implementation for User Story 1

- [X] T030 [US1] Implement GET /api/tasks endpoint in backend/src/api/tasks.py with optional status query parameter
- [X] T031 [US1] Implement TaskService.get_all_tasks() in backend/src/services/task_service.py
- [X] T032 [US1] Implement TaskService.get_tasks_by_status() in backend/src/services/task_service.py  
- [X] T033 [P] [US1] Create TaskService Angular service in frontend/src/app/services/task.service.ts with getTasks() method
- [X] T034 [P] [US1] Create TaskDashboardComponent in frontend/src/app/components/task-dashboard/task-dashboard.component.ts
- [X] T035 [P] [US1] Create TaskDashboardComponent template in frontend/src/app/components/task-dashboard/task-dashboard.component.html with mobile-first TailwindCSS
- [X] T036 [P] [US1] Create TaskFilterComponent in frontend/src/app/components/task-filter/task-filter.component.ts with status filter options
- [X] T037 [P] [US1] Create TaskFilterComponent template in frontend/src/app/components/task-filter/task-filter.component.html with touch-friendly buttons
- [X] T038 [P] [US1] Create TaskCardComponent in frontend/src/app/components/task-card/task-card.component.ts to display individual task
- [X] T039 [P] [US1] Create TaskCardComponent template in frontend/src/app/components/task-card/task-card.component.html with priority styling
- [X] T040 [US1] Add filter state management using Angular signals in frontend/src/app/services/task.service.ts
- [X] T041 [US1] Add validation and error handling for GET /api/tasks in backend/src/api/tasks.py
- [X] T042 [US1] Add logging for task retrieval operations in backend/src/services/task_service.py
- [X] T043 [US1] Verify all US1 tests pass and coverage meets 80% threshold

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Create New Tasks (Priority: P2) 🎯 MVP

**Goal**: Users can create new tasks with title, description, due date, priority, and status

**Independent Test**: Access the task creation form, fill in all required fields (title, description, due date, priority, status), submit the form, and verify the task appears in the database and dashboard view.

### Tests for User Story 2 (TDD: Write FIRST, verify FAIL)

- [ ] T044 [P] [US2] Contract test for POST /api/tasks in backend/tests/contract/test_tasks_create.py
- [ ] T045 [P] [US2] Contract test for POST /api/tasks validation errors in backend/tests/contract/test_tasks_create_validation.py
- [ ] T046 [P] [US2] Unit test for TaskService.create_task() in backend/tests/unit/test_task_service.py
- [ ] T047 [P] [US2] Unit test for Pydantic TaskCreate validation in backend/tests/unit/test_schemas.py
- [ ] T048 [P] [US2] Integration test for task creation form submission in frontend/src/app/components/task-form/task-form.component.spec.ts
- [ ] T049 [P] [US2] Integration test for form validation (required fields) in frontend/src/app/components/task-form/task-form.component.spec.ts

### Implementation for User Story 2

- [ ] T050 [US2] Implement POST /api/tasks endpoint in backend/src/api/tasks.py with request validation
- [ ] T051 [US2] Implement TaskService.create_task() in backend/src/services/task_service.py
- [ ] T052 [P] [US2] Add createTask() method to TaskService in frontend/src/app/services/task.service.ts
- [ ] T053 [P] [US2] Create TaskFormComponent in frontend/src/app/components/task-form/task-form.component.ts with reactive forms
- [ ] T054 [P] [US2] Create TaskFormComponent template in frontend/src/app/components/task-form/task-form.component.html with mobile-optimized inputs
- [ ] T055 [P] [US2] Add form validators for required fields in frontend/src/app/components/task-form/task-form.component.ts (title, description, dueDate)
- [ ] T056 [P] [US2] Create reusable date picker component in frontend/src/app/components/date-picker/date-picker.component.ts
- [ ] T057 [P] [US2] Create reusable dropdown component in frontend/src/app/components/dropdown/dropdown.component.ts for priority/status
- [ ] T058 [US2] Add "Create Task" button to TaskDashboardComponent template
- [ ] T059 [US2] Add modal/dialog service in frontend/src/app/services/dialog.service.ts for task form display
- [ ] T060 [US2] Integrate task creation with dashboard refresh (auto-update task list after create)
- [ ] T061 [US2] Add validation and error handling for POST /api/tasks in backend/src/api/tasks.py
- [ ] T062 [US2] Add logging for task creation operations in backend/src/services/task_service.py
- [ ] T063 [US2] Verify all US2 tests pass and coverage meets 80% threshold

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (MVP complete!)

---

## Phase 5: User Story 3 - Quick Status Update via Checkbox (Priority: P3)

**Goal**: Users can quickly mark pending tasks as completed using a checkbox without opening a detailed edit form

**Independent Test**: Display a pending task with a checkbox, click the checkbox, and verify the task status updates to "Completed" in both the UI and database without requiring a full form submission.

### Tests for User Story 3 (TDD: Write FIRST, verify FAIL)

- [ ] T064 [P] [US3] Contract test for PATCH /api/tasks/{id}/status in backend/tests/contract/test_tasks_status_update.py
- [ ] T065 [P] [US3] Unit test for TaskService.update_task_status() in backend/tests/unit/test_task_service.py
- [ ] T066 [P] [US3] Integration test for checkbox toggle interaction in frontend/src/app/components/task-card/task-card.component.spec.ts

### Implementation for User Story 3

- [ ] T067 [US3] Implement PATCH /api/tasks/{id}/status endpoint in backend/src/api/tasks.py for quick status updates
- [ ] T068 [US3] Implement TaskService.update_task_status() in backend/src/services/task_service.py
- [ ] T069 [P] [US3] Add updateTaskStatus() method to TaskService in frontend/src/app/services/task.service.ts
- [ ] T070 [P] [US3] Add checkbox UI to TaskCardComponent template for pending tasks
- [ ] T071 [US3] Add checkbox toggle handler in TaskCardComponent with optimistic UI update
- [ ] T072 [US3] Add loading spinner during status update in TaskCardComponent
- [ ] T073 [US3] Add visual feedback for completed tasks (styling, checkbox checked state)
- [ ] T074 [US3] Add validation and error handling for PATCH /api/tasks/{id}/status in backend/src/api/tasks.py
- [ ] T075 [US3] Add logging for status update operations in backend/src/services/task_service.py
- [ ] T076 [US3] Verify all US3 tests pass and coverage meets 80% threshold

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Edit and Delete Tasks (Priority: P4)

**Goal**: Users can edit all task fields or delete tasks with confirmation so they can correct mistakes or remove obsolete tasks

**Independent Test**: Select an existing task, click "Edit", modify task fields, save changes, and verify updates persist. Also test deletion by clicking "Delete", confirming in a modal dialog, and verifying the task is removed from the database and UI.

### Tests for User Story 4 (TDD: Write FIRST, verify FAIL)

- [ ] T077 [P] [US4] Contract test for PUT /api/tasks/{id} in backend/tests/contract/test_tasks_update.py
- [ ] T078 [P] [US4] Contract test for DELETE /api/tasks/{id} in backend/tests/contract/test_tasks_delete.py
- [ ] T079 [P] [US4] Unit test for TaskService.update_task() in backend/tests/unit/test_task_service.py
- [ ] T080 [P] [US4] Unit test for TaskService.delete_task() in backend/tests/unit/test_task_service.py
- [ ] T081 [P] [US4] Integration test for task edit workflow in frontend/src/app/components/task-form/task-form.component.spec.ts
- [ ] T082 [P] [US4] Integration test for task delete confirmation in frontend/src/app/components/delete-confirmation/delete-confirmation.component.spec.ts

### Implementation for User Story 4

- [ ] T083 [US4] Implement PUT /api/tasks/{id} endpoint in backend/src/api/tasks.py with full task update
- [ ] T084 [US4] Implement DELETE /api/tasks/{id} endpoint in backend/src/api/tasks.py with 204 No Content response
- [ ] T085 [US4] Implement TaskService.update_task() in backend/src/services/task_service.py
- [ ] T086 [US4] Implement TaskService.delete_task() in backend/src/services/task_service.py
- [ ] T087 [P] [US4] Add updateTask() method to TaskService in frontend/src/app/services/task.service.ts
- [ ] T088 [P] [US4] Add deleteTask() method to TaskService in frontend/src/app/services/task.service.ts
- [ ] T089 [P] [US4] Update TaskFormComponent to support edit mode (pre-populate fields)
- [ ] T090 [P] [US4] Add "Edit" button to TaskCardComponent template
- [ ] T091 [P] [US4] Add "Delete" button to TaskCardComponent template
- [ ] T092 [P] [US4] Create DeleteConfirmationComponent in frontend/src/app/components/delete-confirmation/delete-confirmation.component.ts
- [ ] T093 [P] [US4] Create DeleteConfirmationComponent template with "Confirm" and "Cancel" buttons (44x44px touch targets)
- [ ] T094 [US4] Integrate edit workflow with TaskDashboardComponent (open form in edit mode)
- [ ] T095 [US4] Integrate delete workflow with DeleteConfirmationComponent modal
- [ ] T096 [US4] Add validation and error handling for PUT /api/tasks/{id} in backend/src/api/tasks.py
- [ ] T097 [US4] Add validation and error handling for DELETE /api/tasks/{id} in backend/src/api/tasks.py
- [ ] T098 [US4] Add logging for update and delete operations in backend/src/services/task_service.py
- [ ] T099 [US4] Verify all US4 tests pass and coverage meets 80% threshold

**Checkpoint**: At this point, User Stories 1-4 should all work independently (full CRUD complete)

---

## Phase 7: User Story 5 - Task Due Date Reminders (Priority: P5)

**Goal**: Users receive a reminder one day before a task's due date to ensure timely completion

**Independent Test**: Create a task with a due date set to tomorrow, wait for the scheduled reminder job to run, and verify a notification is sent/displayed to the user 24 hours before the due date.

### Tests for User Story 5 (TDD: Write FIRST, verify FAIL)

- [ ] T100 [P] [US5] Unit test for ReminderService.find_tasks_due_tomorrow() in backend/tests/unit/test_reminder_service.py
- [ ] T101 [P] [US5] Unit test for ReminderService.send_reminder() in backend/tests/unit/test_reminder_service.py
- [ ] T102 [P] [US5] Integration test for scheduled reminder job in backend/tests/integration/test_reminder_scheduler.py
- [ ] T103 [P] [US5] Integration test for reminder notification display in frontend/src/app/components/notification/notification.component.spec.ts

### Implementation for User Story 5

- [ ] T104 [P] [US5] Implement ReminderService.find_tasks_due_tomorrow() in backend/src/services/reminder_service.py
- [ ] T105 [P] [US5] Implement ReminderService.send_reminder() in backend/src/services/reminder_service.py
- [ ] T106 [P] [US5] Implement ReminderService.mark_reminder_sent() in backend/src/services/reminder_service.py
- [ ] T107 [US5] Create scheduled job/function in backend/src/jobs/reminder_scheduler.py using Azure Functions or cron
- [ ] T108 [P] [US5] Create NotificationService in frontend/src/app/services/notification.service.ts for in-app notifications
- [ ] T109 [P] [US5] Create NotificationComponent in frontend/src/app/components/notification/notification.component.ts for toast/banner display
- [ ] T110 [P] [US5] Create NotificationComponent template with mobile-friendly styling
- [ ] T111 [US5] Integrate NotificationService with reminder API polling or WebSocket (if real-time)
- [ ] T112 [US5] Add logging for reminder operations in backend/src/services/reminder_service.py
- [ ] T113 [US5] Add error handling for failed reminder delivery in backend/src/services/reminder_service.py
- [ ] T114 [US5] Verify all US5 tests pass and coverage meets 80% threshold

**Checkpoint**: All user stories (1-5) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T115 [P] Create comprehensive API documentation in backend/docs/api.md
- [ ] T116 [P] Create developer documentation in docs/DEVELOPMENT.md with setup instructions
- [ ] T117 [P] Update README.md with project overview, quick start, and deployment instructions
- [ ] T118 [P] Add GitHub Actions workflow for backend tests in .github/workflows/backend-tests.yml
- [ ] T119 [P] Add GitHub Actions workflow for frontend tests in .github/workflows/frontend-tests.yml
- [ ] T120 [P] Create Bicep template for Azure MySQL Flexible Server in infrastructure/database.bicep
- [ ] T121 [P] Create Bicep template for Azure Container Apps in infrastructure/container-apps.bicep
- [ ] T122 [P] Create Bicep template for Azure Container Registry in infrastructure/container-registry.bicep
- [ ] T123 [P] Create main Bicep orchestration template in infrastructure/main.bicep
- [ ] T124 [P] Create GitHub Actions workflow for Azure deployment in .github/workflows/deploy.yml
- [ ] T125 Code cleanup and refactoring across all components
- [ ] T126 Performance optimization: Add database query optimization (use indexes from data-model.md)
- [ ] T127 Performance optimization: Add frontend lazy loading and code splitting
- [ ] T128 Security hardening: Add input sanitization for all user inputs
- [ ] T129 Security hardening: Add rate limiting to API endpoints
- [ ] T130 Accessibility audit: Ensure WCAG 2.1 AA compliance for all UI components
- [ ] T131 Run quickstart.md validation on fresh development environment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (can run in parallel with US1)
- **User Story 3 (Phase 5)**: Depends on Foundational phase completion (can run in parallel with US1, US2)
- **User Story 4 (Phase 6)**: Depends on Foundational phase completion (can run in parallel with US1, US2, US3)
- **User Story 5 (Phase 7)**: Depends on Foundational phase completion (can run in parallel with US1-US4)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: ✅ Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: ✅ Can start after Foundational (Phase 2) - Integrates with US1 dashboard but independently testable
- **User Story 3 (P3)**: ✅ Can start after Foundational (Phase 2) - Enhances US1 task cards but independently testable
- **User Story 4 (P4)**: ✅ Can start after Foundational (Phase 2) - Extends US2 form and US1 cards but independently testable
- **User Story 5 (P5)**: ✅ Can start after Foundational (Phase 2) - Operates independently with scheduled jobs

### Within Each User Story (TDD Workflow)

1. **Tests FIRST**: Write all test tasks for the story, verify they FAIL (Red)
2. **Models**: Create/update data models and schemas
3. **Services**: Implement business logic in service layer
4. **Endpoints/Components**: Implement API endpoints (backend) or UI components (frontend)
5. **Integration**: Connect frontend to backend, handle errors
6. **Verify**: Run tests, ensure they PASS (Green), verify 80% coverage
7. **Refactor**: Clean up code while keeping tests green

### Parallel Opportunities

#### Within Setup (Phase 1)
- Tasks T003-T010 can run in parallel (different directories/files)

#### Within Foundational (Phase 2)
- Tasks T012-T016 can run in parallel (different model files)
- Tasks T018-T021 can run in parallel (different config files)

#### User Stories (After Foundational Complete)
- All 5 user stories can start in parallel if team capacity allows
- Recommended sequential order: P1 → P2 → P3 → P4 → P5

#### Within Each User Story
- All test tasks marked [P] can run in parallel (different test files)
- All model/component tasks marked [P] can run in parallel (different source files)

---

## Parallel Example: User Story 1

**Launch all test files for User Story 1 together (TDD Red phase)**:
```bash
# Team Member 1: Contract tests
Task T024: Contract test for GET /api/tasks in backend/tests/contract/test_tasks_get.py
Task T025: Contract test for GET /api/tasks?status=Pending in backend/tests/contract/test_tasks_filter.py

# Team Member 2: Unit tests
Task T026: Unit test for TaskService.get_all_tasks() in backend/tests/unit/test_task_service.py
Task T027: Unit test for TaskService.get_tasks_by_status() in backend/tests/unit/test_task_service.py

# Team Member 3: Frontend tests
Task T028: Integration test for dashboard loading in task-dashboard.component.spec.ts
Task T029: Integration test for status filter in task-filter.component.spec.ts
```

**Launch all frontend components for User Story 1 together (after backend services ready)**:
```bash
# Team Member 1: Service layer
Task T033: Create TaskService in frontend/src/app/services/task.service.ts

# Team Member 2: Dashboard component
Task T034: Create TaskDashboardComponent (TypeScript)
Task T035: Create TaskDashboardComponent template (HTML)

# Team Member 3: Filter component
Task T036: Create TaskFilterComponent (TypeScript)
Task T037: Create TaskFilterComponent template (HTML)

# Team Member 4: Card component
Task T038: Create TaskCardComponent (TypeScript)
Task T039: Create TaskCardComponent template (HTML)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. ✅ Complete **Phase 1**: Setup → Project structure ready
2. ✅ Complete **Phase 2**: Foundational → Database, models, base infrastructure ready
3. ✅ Complete **Phase 3**: User Story 1 → Dashboard with filtering functional
4. ✅ Complete **Phase 4**: User Story 2 → Task creation functional
5. **STOP and VALIDATE**: Test US1 + US2 independently
6. Deploy MVP to Azure for demo/feedback

**MVP Deliverables**: Users can view, filter, and create tasks. This is a useful, deployable product.

### Incremental Delivery (Recommended)

1. **Foundation**: Setup → Foundational → Foundation ready
2. **MVP (P1 + P2)**: Add User Story 1 → Add User Story 2 → Test independently → Deploy/Demo
3. **Enhanced (P3)**: Add User Story 3 → Test independently → Deploy/Demo (Quick status updates)
4. **Complete CRUD (P4)**: Add User Story 4 → Test independently → Deploy/Demo (Edit/Delete)
5. **Advanced (P5)**: Add User Story 5 → Test independently → Deploy/Demo (Reminders)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy (3-5 Developers)

**With multiple developers after Foundational phase complete**:

1. **Team completes Setup + Foundational together** (critical path)
2. **Once Foundational is done**:
   - Developer A: User Story 1 (View/Filter)
   - Developer B: User Story 2 (Create)
   - Developer C: User Story 3 (Quick Update)
   - Developer D: User Story 4 (Edit/Delete)
   - Developer E: User Story 5 (Reminders)
3. **Stories complete and integrate independently**
4. **Final integration**: Verify all stories work together, run full test suite

---

## Task Count Summary

- **Phase 1 (Setup)**: 10 tasks
- **Phase 2 (Foundational)**: 13 tasks
- **Phase 3 (User Story 1)**: 20 tasks (6 tests + 14 implementation)
- **Phase 4 (User Story 2)**: 20 tasks (6 tests + 14 implementation)
- **Phase 5 (User Story 3)**: 13 tasks (3 tests + 10 implementation)
- **Phase 6 (User Story 4)**: 23 tasks (6 tests + 17 implementation)
- **Phase 7 (User Story 5)**: 15 tasks (4 tests + 11 implementation)
- **Phase 8 (Polish)**: 17 tasks

**Total**: 131 tasks

**Test Tasks**: 25 test tasks (TDD compliance)  
**Implementation Tasks**: 106 implementation/infrastructure tasks

---

## Suggested MVP Scope

**MVP = User Story 1 + User Story 2** (40 tasks total after Setup + Foundational)

**Why this is MVP**:
- Users can **view** their tasks (US1)
- Users can **filter** by status (US1)
- Users can **create** new tasks (US2)
- This provides immediate utility and value
- Independently testable and deployable
- Foundation for all other stories

**Post-MVP**: Add US3 → US4 → US5 incrementally based on feedback

---

## Format Validation

✅ **All tasks follow checklist format**:
- ✅ Every task starts with `- [ ]` checkbox
- ✅ Every task has sequential Task ID (T001-T131)
- ✅ Parallelizable tasks marked with `[P]`
- ✅ User story tasks marked with `[US1]`, `[US2]`, `[US3]`, `[US4]`, or `[US5]`
- ✅ Every task includes clear file path or location
- ✅ Setup/Foundational tasks have NO story label
- ✅ User Story phases (3-7) have story labels
- ✅ Polish phase tasks have NO story label

---

## Notes

- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story for traceability (US1-US5)
- **TDD workflow**: Tests MUST be written first and FAIL before implementation (Red-Green-Refactor)
- **80% coverage**: Minimum threshold enforced per Constitution Principle II
- **GitHub Copilot**: All code MUST be generated/refactored using Copilot per Constitution Principle III
- **Independent stories**: Each user story should be independently completable and testable
- **Commit frequency**: Commit after each task or logical group
- **Checkpoints**: Stop at any checkpoint to validate story independently before proceeding
