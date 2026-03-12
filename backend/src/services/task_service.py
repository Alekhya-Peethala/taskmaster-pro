"""
TaskMaster Pro - Task Service
Generated with GitHub Copilot assistance
Business logic for task operations (CRUD and filtering)
User Story 1: View and Filter Tasks (P1)
Constitution: TDD (Principle II), API Contract Compliance (Principle V)
"""

from sqlalchemy.orm import Session
from src.models.task import Task
from src.models.schemas import TaskCreate, TaskUpdate, StatusType
from typing import List, Optional
from fastapi import HTTPException, status


class TaskService:
    """
    Service class for task-related business logic.
    Handles database operations for tasks.
    """
    
    def __init__(self, db: Session):
        """
        Initialize TaskService with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from database ordered by due date ascending.
        
        Returns:
            List[Task]: All tasks ordered by due_date
            
        User Story 1 (P1): View all tasks in dashboard
        """
        return self.db.query(Task).order_by(Task.due_date).all()
    
    def get_tasks_by_status(self, status: StatusType) -> List[Task]:
        """
        Retrieve tasks filtered by status, ordered by due date.
        
        Args:
            status: Task status to filter by ('Pending', 'In Progress', 'Completed')
            
        Returns:
            List[Task]: Tasks matching the specified status
            
        Raises:
            ValueError: If status is not a valid enum value
            
        User Story 1 (P1): Filter tasks by status
        """
        # Validate status is one of the allowed values
        valid_statuses = ["Pending", "In Progress", "Completed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")
        
        return (
            self.db.query(Task)
            .filter(Task.status == status)
            .order_by(Task.due_date)
            .all()
        )
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a single task by ID.
        
        Args:
            task_id: Unique identifier of the task
            
        Returns:
            Task if found, None otherwise
        """
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """
        Create a new task.
        
        Args:
            task_data: Task creation data (TaskCreate schema)
            
        Returns:
            Task: Newly created task with generated ID and timestamps
            
        User Story 2 (P2): Create new tasks
        """
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            status=task_data.status,
            reminder_sent=False  # Default value
        )
        
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        
        return new_task
    
    def update_task(self, task_id: int, task_data: TaskUpdate) -> Task:
        """
        Update an existing task.
        
        Args:
            task_id: ID of task to update
            task_data: Updated task data (TaskUpdate schema)
            
        Returns:
            Task: Updated task
            
        Raises:
            HTTPException: 404 if task not found
            
        User Story 4 (P4): Edit tasks
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        
        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by ID.
        
        Args:
            task_id: ID of task to delete
            
        Raises:
            HTTPException: 404 if task not found
            
        User Story 4 (P4): Delete tasks
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        
        self.db.delete(task)
        self.db.commit()
