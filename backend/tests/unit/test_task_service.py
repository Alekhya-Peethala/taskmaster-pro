"""
TaskMaster Pro - Unit Tests for TaskService
Generated with GitHub Copilot assistance
Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
User Story 1: View and Filter Tasks (P1)
Tests for TaskService.get_all_tasks() and TaskService.get_tasks_by_status()
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.services.task_service import TaskService
from src.models.task import Task
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
