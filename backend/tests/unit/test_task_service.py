"""
TaskMaster Pro - Unit Tests for TaskService
Generated with GitHub Copilot assistance
Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
User Stories 1-4: View, Filter, Create, Update, Delete Tasks
Tests for all TaskService methods.
"""

import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException
from src.services.task_service import TaskService
from src.models.task import Task
from src.models.schemas import TaskCreate, TaskUpdate
from datetime import date


@pytest.fixture
def mock_db_session():
    """Mock database session for unit testing"""
    return Mock()


@pytest.fixture
def task_service(mock_db_session):
    """Create TaskService instance with mocked database"""
    return TaskService(mock_db_session)


@pytest.fixture
def sample_tasks():
    """Sample Task objects for testing"""
    return [
        Task(
            id=1,
            title="Task 1",
            description="Description 1",
            due_date=date(2026, 3, 15),
            priority="High",
            status="Pending",
            reminder_sent=False
        ),
        Task(
            id=2,
            title="Task 2",
            description="Description 2",
            due_date=date(2026, 3, 16),
            priority="Medium",
            status="In Progress",
            reminder_sent=False
        ),
        Task(
            id=3,
            title="Task 3",
            description="Description 3",
            due_date=date(2026, 3, 14),
            priority="Low",
            status="Completed",
            reminder_sent=True
        ),
    ]


class TestGetAllTasks:
    """Tests for TaskService.get_all_tasks() method"""
    
    def test_get_all_tasks_returns_all_tasks(self, task_service, mock_db_session, sample_tasks):
        """
        Test get_all_tasks() returns all tasks from database
        Expected: List of all Task objects ordered by due_date
        """
        mock_query = MagicMock()
        mock_query.order_by.return_value.all.return_value = sample_tasks
        mock_db_session.query.return_value = mock_query
        
        result = task_service.get_all_tasks()
        
        assert len(result) == 3
        assert result == sample_tasks
        mock_db_session.query.assert_called_once()
    
    def test_get_all_tasks_returns_empty_list_when_no_tasks(self, task_service, mock_db_session):
        """
        Test get_all_tasks() returns empty list when database is empty
        Expected: Empty list []
        """
        mock_query = MagicMock()
        mock_query.order_by.return_value.all.return_value = []
        mock_db_session.query.return_value = mock_query
        
        result = task_service.get_all_tasks()
        
        assert result == []
        assert len(result) == 0
    
    def test_get_all_tasks_orders_by_due_date(self, task_service, mock_db_session):
        """
        Test get_all_tasks() orders results by due_date ascending
        Expected: Tasks ordered from earliest to latest due date
        """
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        
        task_service.get_all_tasks()
        
        # Verify order_by was called with Task.due_date
        mock_query.order_by.assert_called_once()


class TestGetTasksByStatus:
    """Tests for TaskService.get_tasks_by_status() method"""
    
    def test_get_tasks_by_status_filters_pending(self, task_service, mock_db_session, sample_tasks):
        """
        Test get_tasks_by_status('Pending') returns only pending tasks
        Expected: Only tasks with status='Pending'
        """
        pending_tasks = [t for t in sample_tasks if t.status == "Pending"]
        
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = pending_tasks
        mock_db_session.query.return_value = mock_query
        
        result = task_service.get_tasks_by_status("Pending")
        
        assert len(result) == 1
        assert all(task.status == "Pending" for task in result)
    
    def test_get_tasks_by_status_filters_in_progress(self, task_service, mock_db_session, sample_tasks):
        """
        Test get_tasks_by_status('In Progress') returns only in-progress tasks
        Expected: Only tasks with status='In Progress'
        """
        in_progress_tasks = [t for t in sample_tasks if t.status == "In Progress"]
        
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = in_progress_tasks
        mock_db_session.query.return_value = mock_query
        
        result = task_service.get_tasks_by_status("In Progress")
        
        assert len(result) == 1
        assert all(task.status == "In Progress" for task in result)
    
    def test_get_tasks_by_status_filters_completed(self, task_service, mock_db_session, sample_tasks):
        """
        Test get_tasks_by_status('Completed') returns only completed tasks
        Expected: Only tasks with status='Completed'
        """
        completed_tasks = [t for t in sample_tasks if t.status == "Completed"]
        
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = completed_tasks
        mock_db_session.query.return_value = mock_query
        
        result = task_service.get_tasks_by_status("Completed")
        
        assert len(result) == 1
        assert all(task.status == "Completed" for task in result)
    
    def test_get_tasks_by_status_returns_empty_when_no_matches(self, task_service, mock_db_session):
        """
        Test get_tasks_by_status() returns empty list when no tasks match status
        Expected: Empty list []
        """
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = []
        mock_db_session.query.return_value = mock_query
        
        result = task_service.get_tasks_by_status("Pending")
        
        assert result == []
    
    def test_get_tasks_by_status_validates_status_enum(self, task_service):
        """
        Test get_tasks_by_status() raises error for invalid status
        Expected: ValueError for invalid status values
        """
        with pytest.raises((ValueError, Exception)):
            task_service.get_tasks_by_status("InvalidStatus")


class TestGetTaskById:
    """Tests for TaskService.get_task_by_id() method"""

    def test_get_task_by_id_returns_task(self, task_service, mock_db_session, sample_tasks):
        """get_task_by_id() returns the matching Task."""
        target = sample_tasks[0]
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = target
        mock_db_session.query.return_value = mock_query

        result = task_service.get_task_by_id(1)

        assert result is target

    def test_get_task_by_id_returns_none_when_not_found(self, task_service, mock_db_session):
        """get_task_by_id() returns None when task does not exist."""
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_db_session.query.return_value = mock_query

        result = task_service.get_task_by_id(999)

        assert result is None


class TestCreateTask:
    """Tests for TaskService.create_task() method"""

    def test_create_task_returns_new_task(self, task_service, mock_db_session):
        """create_task() adds a task to the database and returns it."""
        future_date = date(2026, 12, 31)
        task_data = TaskCreate(
            title="New Task",
            description="A fresh task",
            due_date=future_date,
            priority="High",
            status="Pending",
        )

        created = task_service.create_task(task_data)

        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
        assert created.title == "New Task"
        assert created.status == "Pending"

    def test_create_task_sets_reminder_sent_false(self, task_service, mock_db_session):
        """create_task() always sets reminder_sent to False."""
        future_date = date(2026, 12, 31)
        task_data = TaskCreate(
            title="Reminder Test",
            description="Checking reminder_sent default",
            due_date=future_date,
            priority="Low",
            status="Pending",
        )

        created = task_service.create_task(task_data)

        assert created.reminder_sent is False


class TestUpdateTask:
    """Tests for TaskService.update_task() method"""

    def test_update_task_modifies_fields(self, task_service, mock_db_session, sample_tasks):
        """update_task() updates the given fields on an existing task."""
        task = sample_tasks[0]
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = task
        mock_db_session.query.return_value = mock_query

        update_data = TaskUpdate(status="Completed")
        result = task_service.update_task(task.id, update_data)

        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
        assert result.status == "Completed"

    def test_update_task_raises_404_when_not_found(self, task_service, mock_db_session):
        """update_task() raises HTTPException 404 when task does not exist."""
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_db_session.query.return_value = mock_query

        update_data = TaskUpdate(title="Ghost")

        with pytest.raises(HTTPException) as exc_info:
            task_service.update_task(999, update_data)

        assert exc_info.value.status_code == 404


class TestDeleteTask:
    """Tests for TaskService.delete_task() method"""

    def test_delete_task_removes_from_database(self, task_service, mock_db_session, sample_tasks):
        """delete_task() deletes the task and commits the transaction."""
        task = sample_tasks[0]
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = task
        mock_db_session.query.return_value = mock_query

        task_service.delete_task(task.id)

        mock_db_session.delete.assert_called_once_with(task)
        mock_db_session.commit.assert_called_once()

    def test_delete_task_raises_404_when_not_found(self, task_service, mock_db_session):
        """delete_task() raises HTTPException 404 when task does not exist."""
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = None
        mock_db_session.query.return_value = mock_query

        with pytest.raises(HTTPException) as exc_info:
            task_service.delete_task(999)

        assert exc_info.value.status_code == 404
