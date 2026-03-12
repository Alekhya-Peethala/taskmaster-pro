"""
TaskMaster Pro - Task SQLAlchemy Model
Generated with GitHub Copilot assistance
Represents a work item in the task management system
Constitution: Azure MySQL Flexible Server (Principle I), TDD (Principle II)
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, CheckConstraint, Index
from sqlalchemy.sql import func
from src.database import Base


class Task(Base):
    """
    SQLAlchemy ORM model for Task entity.
    
    Represents a work item with title, description, due date, priority, and status.
    Supports CRUD operations and filtering by status.
    
    Attributes:
        id (int): Unique identifier (auto-incrementing primary key)
        title (str): Short, descriptive name (max 255 chars)
        description (str): Detailed explanation (max 65,535 chars - TEXT type)
        due_date (date): Date by which task should be completed
        priority (str): Task importance ('Low', 'Medium', 'High')
        status (str): Current state ('Pending', 'In Progress', 'Completed')
        reminder_sent (bool): Flag indicating if 24-hour reminder has been sent
        created_at (datetime): Timestamp when task was created
        updated_at (datetime): Timestamp of last modification
    """
    __tablename__ = "tasks"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core Fields (Required by FR-005 to FR-010 in spec.md)
    title = Column(String(255), nullable=False)
    description = Column(String(65535), nullable=False)  # TEXT type
    due_date = Column(Date, nullable=False)
    priority = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    
    # Reminder Field (for User Story 5)
    reminder_sent = Column(Boolean, nullable=False, default=False)
    
    # Audit Fields
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Check Constraints for data integrity
    __table_args__ = (
        CheckConstraint(
            "priority IN ('Low', 'Medium', 'High')",
            name="check_priority_values"
        ),
        CheckConstraint(
            "status IN ('Pending', 'In Progress', 'Completed')",
            name="check_status_values"
        ),
        # Performance indexes (from data-model.md)
        Index('idx_status', 'status'),
        Index('idx_due_date', 'due_date'),
        Index('idx_status_due_date', 'status', 'due_date'),
        Index('idx_reminder_due', 'reminder_sent', 'due_date'),
    )
    
    def __repr__(self) -> str:
        """String representation of Task for debugging."""
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
