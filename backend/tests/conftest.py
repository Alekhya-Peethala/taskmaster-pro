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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

# Set environment variables before any application imports
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["ALLOWED_ORIGINS"] = "http://localhost:4200"
os.environ["ENV"] = "test"

# ---------------------------------------------------------------------------
# SQLite in-memory database fixtures for contract/integration tests
# StaticPool ensures all sessions share the same in-memory connection so
# data written in one session is visible to the application under test.
# ---------------------------------------------------------------------------

SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

_test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    SQLite in-memory database session for contract tests.
    Creates all tables before the test and drops them afterwards.
    """
    from src.database import Base
    from src.models import task  # ensure model is registered with Base  # noqa: F401

    Base.metadata.create_all(bind=_test_engine)
    db = _TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    FastAPI test client with the database dependency overridden to use the
    SQLite in-memory session provided by `db_session`.
    """
    from src.main import app
    from src.database import get_db

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_db():
    """
    Mock database session for unit tests (no real DB needed).
    Returns a MagicMock session object.
    """
    return MagicMock()


@pytest.fixture
def sample_task_data():
    """
    Sample task data dictionary with valid fields for API request payloads.
    """
    from datetime import date, timedelta

    return {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": (date.today() + timedelta(days=7)).isoformat(),
        "priority": "Medium",
        "status": "Pending",
    }


@pytest.fixture
def sample_tasks_data():
    """
    Sample list of task dictionaries (various statuses/priorities) for unit tests.
    """
    from datetime import date, timedelta

    base = date.today()

    return [
        {
            "id": 1,
            "title": "Task 1 - Pending",
            "description": "First test task",
            "due_date": (base + timedelta(days=5)).isoformat(),
            "priority": "High",
            "status": "Pending",
            "reminder_sent": False,
        },
        {
            "id": 2,
            "title": "Task 2 - In Progress",
            "description": "Second test task",
            "due_date": (base + timedelta(days=3)).isoformat(),
            "priority": "Medium",
            "status": "In Progress",
            "reminder_sent": False,
        },
        {
            "id": 3,
            "title": "Task 3 - Completed",
            "description": "Third test task",
            "due_date": (base + timedelta(days=1)).isoformat(),
            "priority": "Low",
            "status": "Completed",
            "reminder_sent": True,
        },
    ]
