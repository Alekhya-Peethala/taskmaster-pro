"""
TaskMaster Pro - Pytest Configuration
Generated with GitHub Copilot assistance
Test fixtures and configuration for backend tests
Constitution: Test-Driven Development (Principle II)
"""

import os
import sys
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

# Mock environment variables before any imports
os.environ.setdefault("DATABASE_URL", "mysql+mysqlconnector://test:test@localhost:3306/test_db")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:4200")
os.environ.setdefault("ENV", "test")

@pytest.fixture
def mock_db():
    """
    Mock database session for unit tests.
    Returns a MagicMock session object.
    """
    session = MagicMock()
    return session


@pytest.fixture
def client():
    """
    FastAPI test client fixture.
    Provides a test client for contract/integration tests.
    """
    # Import here to ensure env vars are set first
    from src.main import app
    
    # Create test client
    test_client = TestClient(app)
    return test_client


@pytest.fixture
def sample_task_data():
    """
    Sample task data for testing.
    Provides a dictionary with valid task fields.
    """
    from datetime import datetime, timedelta
    
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "priority": "Medium",
        "status": "Pending"
    }


@pytest.fixture
def sample_tasks():
    """
    Sample list of tasks for testing.
    Provides a list of task dictionaries with various statuses and priorities.
    """
    from datetime import datetime, timedelta
    
    base_date = datetime.now()
    
    return [
        {
            "id": 1,
            "title": "Task 1 - Pending",
            "description": "First test task",
            "due_date": (base_date + timedelta(days=5)).isoformat(),
            "priority": "High",
            "status": "Pending",
            "reminder_sent": False,
            "created_at": base_date.isoformat(),
            "updated_at": base_date.isoformat()
        },
        {
            "id": 2,
            "title": "Task 2 - In Progress",
            "description": "Second test task",
            "due_date": (base_date + timedelta(days=3)).isoformat(),
            "priority": "Medium",
            "status": "In Progress",
            "reminder_sent": False,
            "created_at": base_date.isoformat(),
            "updated_at": base_date.isoformat()
        },
        {
            "id": 3,
            "title": "Task 3 - Completed",
            "description": "Third test task",
            "due_date": (base_date + timedelta(days=1)).isoformat(),
            "priority": "Low",
            "status": "Completed",
            "reminder_sent": True,
            "created_at": base_date.isoformat(),
            "updated_at": base_date.isoformat()
        }
    ]
