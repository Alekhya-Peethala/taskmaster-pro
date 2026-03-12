"""
TaskMaster Pro - Pydantic Schemas
Generated with GitHub Copilot assistance
Data validation and serialization schemas for API request/response
Constitution: API Contract Compliance (Principle V), TypeScript-style typing
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date, datetime
from typing import Literal


# Type aliases for strict enum validation
PriorityType = Literal["Low", "Medium", "High"]
StatusType = Literal["Pending", "In Progress", "Completed"]


class TaskBase(BaseModel):
    """
    Base Pydantic model with shared Task fields.
    Used as parent for TaskCreate, TaskUpdate schemas.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Short, descriptive name for the task"
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=65535,
        description="Detailed explanation of the task"
    )
    due_date: date = Field(
        ...,
        description="Date by which task should be completed (YYYY-MM-DD)"
    )
    priority: PriorityType = Field(
        ...,
        description="Task importance level"
    )
    status: StatusType = Field(
        ...,
        description="Current state of the task"
    )


class TaskCreate(TaskBase):
    """
    Schema for creating a new task (POST /api/tasks).
    Inherits all fields from TaskBase, adds past-date guard.
    
    Example:
        {
            "title": "Deploy to production",
            "description": "Deploy v2.1.0 to production environment",
            "due_date": "2026-03-20",
            "priority": "High",
            "status": "Pending"
        }
    """
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: date) -> date:
        """
        Validate that due_date is not in the past.
        Allow today and future dates only.
        """
        if v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task (PUT /api/tasks/{id}).
    All fields are optional to allow partial updates.
    
    Example:
        {
            "status": "Completed"
        }
    """
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, min_length=1, max_length=65535)
    due_date: date | None = None
    priority: PriorityType | None = None
    status: StatusType | None = None
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: date | None) -> date | None:
        """Validate that due_date is not in the past if provided."""
        if v is not None and v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v


class TaskResponse(TaskBase):
    """
    Schema for task responses (GET /api/tasks, POST /api/tasks, PUT /api/tasks/{id}).
    Includes all fields plus system-generated fields (id, timestamps).
    
    Example:
        {
            "id": 1,
            "title": "Deploy to production",
            "description": "Deploy v2.1.0 to production environment",
            "due_date": "2026-03-20",
            "priority": "High",
            "status": "Pending",
            "reminder_sent": false,
            "created_at": "2026-03-12T15:45:00Z",
            "updated_at": "2026-03-12T15:45:00Z"
        }
    """
    id: int
    reminder_sent: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TaskStatusUpdate(BaseModel):
    """
    Schema for quick status updates via checkbox (PATCH /api/tasks/{id}/status).
    User Story 3: Quick Status Update via Checkbox.
    
    Example:
        {
            "status": "Completed"
        }
    """
    status: StatusType = Field(
        ...,
        description="New status for the task"
    )
