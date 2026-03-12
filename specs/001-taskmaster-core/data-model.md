# Data Model: TaskMaster Pro

**Feature**: TaskMaster Pro - Complete Task Management Application  
**Branch**: 001-taskmaster-core
**Date**: 2026-03-12  
**Phase**: 1 - Data Model Design

## Overview

TaskMaster Pro uses a single-entity data model centered around the **Task** entity. This minimalist approach aligns with the feature scope: task CRUD operations, filtering, and reminders. No complex relationships or multi-entity interactions are required for v1.

---

## Entity: Task

**Purpose**: Represents a work item that can be created, viewed, edited, deleted, and filtered by users.

### Attributes

| Field | Type | MySQL Type | Constraints | Description |
|-------|------|------------|-------------|-------------|
| `id` | Integer | `INT` | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for each task |
| `title` | String | `VARCHAR(255)` | NOT NULL | Short, descriptive name for the task (max 255 chars) |
| `description` | String | `TEXT` | NOT NULL | Detailed explanation of the task (max 65,535 chars) |
| `due_date` | Date | `DATE` | NOT NULL | Date by which task should be completed (YYYY-MM-DD) |
| `priority` | Enum | `VARCHAR(50)` | NOT NULL, CHECK constraint | Task importance: 'Low', 'Medium', or 'High' |
| `status` | Enum | `VARCHAR(50)` | NOT NULL, CHECK constraint | Current state: 'Pending', 'In Progress', or 'Completed' |
| `created_at` | DateTime | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP | Timestamp when task was created |
| `updated_at` | DateTime | `TIMESTAMP` | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Timestamp of last modification |

### Additional Fields (for Reminders - Phase 5)

| Field | Type | MySQL Type | Constraints | Description |
|-------|------|------------|-------------|-------------|
| `reminder_sent` | Boolean | `TINYINT(1)` | DEFAULT 0 | Flag indicating if 24-hour reminder has been sent |

---

## Database Schema (MySQL DDL)

```sql
CREATE TABLE tasks (
    -- Primary Key
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Core Fields (Required by FR-005 to FR-010)
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    priority VARCHAR(50) NOT NULL CHECK (priority IN ('Low', 'Medium', 'High')),
    status VARCHAR(50) NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    
    -- Reminder Field (for User Story 5)
    reminder_sent TINYINT(1) DEFAULT 0 NOT NULL,
    
    -- Audit Fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for Performance
    INDEX idx_status (status),
    INDEX idx_due_date (due_date),
    INDEX idx_status_due_date (status, due_date),
    INDEX idx_reminder_due (reminder_sent, due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Index Justification**:
- `idx_status`: Supports filtering by status (P1 requirement)
- `idx_due_date`: Supports date-based queries and reminders (P5 requirement)
- `idx_status_due_date`: Composite index for combined filters (common use case)
- `idx_reminder_due`: Optimizes reminder queries (find unsent reminders for tomorrow)

---

## SQLAlchemy ORM Model (backend/src/models/task.py)

```python
# Generated with GitHub Copilot
from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, CheckConstraint
from sqlalchemy.sql import func
from .database import Base

class Task(Base):
    """
    SQLAlchemy ORM model for Task entity.
    
    Represents a work item with title, description, due date, priority, and status.
    Supports CRUD operations and filtering by status.
    """
    __tablename__ = "tasks"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core Fields
    title = Column(String(255), nullable=False)
    description = Column(String(65535), nullable=False)  # TEXT type
    due_date = Column(Date, nullable=False, index=True)
    priority = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, index=True)
    
    # Reminder Field
    reminder_sent = Column(Boolean, default=False, nullable=False, index=True)
    
    # Audit Fields
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Check Constraints
    __table_args__ = (
        CheckConstraint("priority IN ('Low', 'Medium', 'High')", name="check_priority"),
        CheckConstraint("status IN ('Pending', 'In Progress', 'Completed')", name="check_status"),
    )
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
```

---

## Pydantic Schemas (backend/src/models/schemas.py)

### Base Schema

```python
# Generated with GitHub Copilot
from pydantic import BaseModel, Field, validator
from datetime import date
from enum import Enum

class PriorityEnum(str, Enum):
    """Task priority levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusEnum(str, Enum):
    """Task status states."""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class TaskBase(BaseModel):
    """Base schema with common Task fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(..., min_length=1, max_length=65535, description="Task description")
    due_date: date = Field(..., description="Task due date (YYYY-MM-DD)")
    priority: PriorityEnum = Field(..., description="Task priority: Low, Medium, or High")
    status: StatusEnum = Field(..., description="Task status: Pending, In Progress, or Completed")
    
    @validator('due_date')
    def validate_due_date(cls, v):
        """
        Validate that due date is not in the past (optional constraint).
        Uncomment to enforce future dates only.
        """
        # from datetime import date as date_today
        # if v < date_today.today():
        #     raise ValueError('Due date cannot be in the past')
        return v
```

### Create Schema (POST /api/tasks)

```python
class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass  # Inherits all fields from TaskBase as required
```

### Update Schema (PUT /api/tasks/:id)

```python
class TaskUpdate(TaskBase):
    """Schema for updating an existing task."""
    pass  # Inherits all fields from TaskBase; full resource update
```

### Response Schema (All API Responses)

```python
from datetime import datetime

class TaskResponse(TaskBase):
    """Schema for task responses (includes id and audit fields)."""
    id: int = Field(..., description="Unique task identifier")
    reminder_sent: bool = Field(default=False, description="Whether reminder has been sent")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models
```

---

## TypeScript Interface (frontend/src/app/core/models/task.model.ts)

```typescript
// Generated with GitHub Copilot
/**
 * Task entity representing a work item.
 * Matches backend Pydantic schema (TaskResponse).
 */
export interface Task {
  id: number;
  title: string;
  description: string;
  dueDate: string; // ISO 8601 date string (YYYY-MM-DD)
  priority: 'Low' | 'Medium' | 'High';
  status: 'Pending' | 'In Progress' | 'Completed';
  reminderSent: boolean;
  createdAt: string; // ISO 8601 datetime string
  updatedAt: string; // ISO 8601 datetime string
}

/**
 * Enum for task priority levels.
 */
export enum TaskPriority {
  Low = 'Low',
  Medium = 'Medium',
  High = 'High'
}

/**
 * Enum for task status states.
 */
export enum TaskStatus {
  Pending = 'Pending',
  InProgress = 'In Progress',
  Completed = 'Completed'
}

/**
 * DTO for creating a new task (excludes auto-generated fields).
 */
export interface TaskCreateDto {
  title: string;
  description: string;
  dueDate: string; // YYYY-MM-DD
  priority: TaskPriority;
  status: TaskStatus;
}

/**
 * DTO for updating an existing task (full resource update).
 */
export interface TaskUpdateDto {
  title: string;
  description: string;
  dueDate: string; // YYYY-MM-DD
  priority: TaskPriority;
  status: TaskStatus;
}
```

**Note**: TypeScript uses camelCase (`dueDate`, `createdAt`) while Python/MySQL use snake_case (`due_date`, `created_at`). The backend API will handle serialization/deserialization using Pydantic's alias configuration.

---

## Validation Rules

### Business Logic Validations

1. **Title** (FR-006):
   - Required, cannot be empty
   - Maximum 255 characters
   - No special validation (allows all characters)

2. **Description** (FR-007):
   - Required, cannot be empty
   - Maximum 65,535 characters (TEXT field limit)
   - No special validation (allows all characters)

3. **Due Date** (FR-008):
   - Required, must be valid date in YYYY-MM-DD format
   - Optional: Can enforce no past dates (currently disabled in validator)
   - Used for reminder scheduling (24 hours before)

4. **Priority** (FR-009):
   - Required, must be one of: 'Low', 'Medium', 'High'
   - Enforced by enum in Pydantic and CHECK constraint in MySQL

5. **Status** (FR-010):
   - Required, must be one of: 'Pending', 'In Progress', 'Completed'
   - Enforced by enum in Pydantic and CHECK constraint in MySQL

6. **Reminder Sent**:
   - Boolean flag, defaults to false
   - Set to true after reminder notification is sent
   - Prevents duplicate reminders for same task

### State Transitions

**Valid Status Transitions** (enforced in business logic, not database):
- `Pending` → `In Progress` (user starts working on task)
- `Pending` → `Completed` (quick completion via checkbox - P3 requirement)
- `In Progress` → `Completed` (task finished)
- `Completed` → `Pending` (user unchecks completed task - P3 requirement)
- `In Progress` → `Pending` (user pauses work)

**Invalid Transitions**: None enforced - all transitions allowed for maximum flexibility

---

## Relationships

**Current**: None - TaskMaster Pro v1 uses a single-entity model.

**Future Enhancements** (out of scope for this feature):
- `User` entity → Tasks assigned to users (many-to-one)
- `Project` entity → Tasks grouped by projects (many-to-one)
- `Tag` entity → Tasks tagged for categorization (many-to-many)
- `Comment` entity → Comments on tasks (one-to-many)

---

## Data Access Patterns

### Common Queries (Optimized by Indexes)

1. **Get All Tasks** (P1 - Dashboard):
   ```sql
   SELECT * FROM tasks ORDER BY due_date ASC;
   ```

2. **Filter by Status** (P1 - Dashboard filters):
   ```sql
   SELECT * FROM tasks WHERE status = 'Pending' ORDER BY due_date ASC;
   -- Uses idx_status index
   ```

3. **Get Task by ID** (P4 - Edit/Delete):
   ```sql
   SELECT * FROM tasks WHERE id = ?;
   -- Uses primary key index
   ```

4. **Find Tasks Due Tomorrow for Reminders** (P5 - Reminder scheduling):
   ```sql
   SELECT * FROM tasks 
   WHERE due_date = CURDATE() + INTERVAL 1 DAY 
     AND reminder_sent = 0 
     AND status != 'Completed';
   -- Uses idx_reminder_due index
   ```

5. **Update Task Status** (P3 - Quick checkbox update):
   ```sql
   UPDATE tasks SET status = 'Completed', updated_at = CURRENT_TIMESTAMP WHERE id = ?;
   ```

---

## Migration Strategy

### Initial Migration (Alembic)

**File**: `backend/src/db/migrations/versions/001_create_tasks_table.py`

```python
# Generated with GitHub Copilot
"""Create tasks table

Revision ID: 001
Revises: 
Create Date: 2026-03-12
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('reminder_sent', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.CheckConstraint("priority IN ('Low', 'Medium', 'High')", name='check_priority'),
        sa.CheckConstraint("status IN ('Pending', 'In Progress', 'Completed')", name='check_status'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_status', 'tasks', ['status'])
    op.create_index('idx_due_date', 'tasks', ['due_date'])
    op.create_index('idx_status_due_date', 'tasks', ['status', 'due_date'])
    op.create_index('idx_reminder_due', 'tasks', ['reminder_sent', 'due_date'])

def downgrade():
    op.drop_index('idx_reminder_due', table_name='tasks')
    op.drop_index('idx_status_due_date', table_name='tasks')
    op.drop_index('idx_due_date', table_name='tasks')
    op.drop_index('idx_status', table_name='tasks')
    op.drop_table('tasks')
```

---

## Summary

**Entity Count**: 1 (Task)  
**Total Fields**: 9 (including audit fields)  
**Indexes**: 4 (optimized for common queries)  
**Relationships**: None (single-entity model)  
**Validation Rules**: 6 (title, description, due_date, priority, status, reminder_sent)

**Next Steps**:
✅ Data model complete  
➡️ Generate API contracts (OpenAPI spec + JSON schema)  
➡️ Generate quickstart.md for developers
