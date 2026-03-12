"""
TaskMaster Pro - Task API Endpoints
Generated with GitHub Copilot assistance
RESTful API endpoints for task CRUD operations
Constitution: API Contract Compliance (Principle V), TDD (Principle II)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database import get_db
from src.models.schemas import TaskResponse, TaskCreate, TaskUpdate, TaskStatusUpdate, StatusType
from src.services.task_service import TaskService
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Create API router with /tasks prefix
router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(
    status_filter: Optional[StatusType] = Query(None, alias="status", description="Filter tasks by status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks, optionally filtered by status.
    
    **User Story 1 (P1): View and Filter Tasks**
    
    Query Parameters:
        status: Optional status filter ('Pending', 'In Progress', 'Completed')
    
    Returns:
        List[TaskResponse]: Array of tasks ordered by due date
        
    Examples:
        GET /api/tasks - Returns all tasks
        GET /api/tasks?status=Pending - Returns only pending tasks
    """
    try:
        service = TaskService(db)
        
        if status_filter:
            # Filter by status
            logger.info(f"Fetching tasks with status: {status_filter}")
            tasks = service.get_tasks_by_status(status_filter)
        else:
            # Get all tasks
            logger.info("Fetching all tasks")
            tasks = service.get_all_tasks()
        
        logger.info(f"Retrieved {len(tasks)} tasks")
        return tasks
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error fetching tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )


@router.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a single task by ID.
    
    Path Parameters:
        task_id: Unique identifier of the task
        
    Returns:
        TaskResponse: Task details
        
    Raises:
        404: Task not found
    """
    try:
        service = TaskService(db)
        task = service.get_task_by_id(task_id)
        
        if not task:
            logger.warning(f"Task {task_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        
        logger.info(f"Retrieved task {task_id}")
        return task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    **User Story 2 (P2): Create New Tasks**
    
    Request Body:
        TaskCreate: Task data (title, description, due_date, priority, status)
        
    Returns:
        TaskResponse: Created task with generated ID and timestamps
    """
    try:
        service = TaskService(db)
        new_task = service.create_task(task_data)
        
        logger.info(f"Created task {new_task.id}: {new_task.title}")
        return new_task
        
    except Exception as e:
        logger.exception(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )


@router.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    **User Story 4 (P4): Edit Tasks**
    
    Path Parameters:
        task_id: ID of task to update
        
    Request Body:
        TaskUpdate: Updated task fields (all fields optional)
        
    Returns:
        TaskResponse: Updated task
        
    Raises:
        404: Task not found
    """
    try:
        service = TaskService(db)
        updated_task = service.update_task(task_id, task_data)
        
        logger.info(f"Updated task {task_id}")
        return updated_task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error updating task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


@router.patch("/tasks/{task_id}/status", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Quick status update for a task (checkbox toggle).
    
    **User Story 3 (P3): Quick Status Update via Checkbox**
    
    Path Parameters:
        task_id: ID of task to update
        
    Request Body:
        TaskStatusUpdate: New status
        
    Returns:
        TaskResponse: Updated task
        
    Raises:
        404: Task not found
    """
    try:
        service = TaskService(db)
        task_update = TaskUpdate(status=status_data.status)
        updated_task = service.update_task(task_id, task_update)
        
        logger.info(f"Updated task {task_id} status to {status_data.status}")
        return updated_task
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error updating task {task_id} status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task status"
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    
    **User Story 4 (P4): Delete Tasks**
    
    Path Parameters:
        task_id: ID of task to delete
        
    Returns:
        204 No Content on success
        
    Raises:
        404: Task not found
    """
    try:
        service = TaskService(db)
        service.delete_task(task_id)
        
        logger.info(f"Deleted task {task_id}")
        return None  # 204 No Content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error deleting task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )
