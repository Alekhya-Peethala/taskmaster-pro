"""
TaskMaster Pro - Contract Test for GET /api/tasks
Generated with GitHub Copilot assistance
Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
User Story 1: View and Filter Tasks (P1)
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import Base, engine, SessionLocal
from src.models.task import Task
from datetime import date, datetime

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_tasks(db_session):
    """Create sample tasks for testing"""
    tasks = [
        Task(
            title="Task 1 - Pending",
            description="Description for task 1",
            due_date=date(2026, 3, 15),
            priority="High",
            status="Pending",
            reminder_sent=False
        ),
        Task(
            title="Task 2 - In Progress",
            description="Description for task 2",
            due_date=date(2026, 3, 16),
            priority="Medium",
            status="In Progress",
            reminder_sent=False
        ),
        Task(
            title="Task 3 - Completed",
            description="Description for task 3",
            due_date=date(2026, 3, 14),
            priority="Low",
            status="Completed",
            reminder_sent=True
        ),
    ]
    for task in tasks:
        db_session.add(task)
    db_session.commit()
    return tasks


def test_get_all_tasks_empty_database(db_session):
    """
    Test GET /api/tasks returns empty array when no tasks exist
    Expected: 200 OK with empty array []
    """
    response = client.get("/api/tasks")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks_with_data(db_session, sample_tasks):
    """
    Test GET /api/tasks returns all tasks
    Expected: 200 OK with array of 3 tasks
    """
    response = client.get("/api/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Verify response structure matches TaskResponse schema
    for task in data:
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "dueDate" in task or "due_date" in task
        assert "priority" in task
        assert "status" in task
        assert "reminderSent" in task or "reminder_sent" in task
        assert "createdAt" in task or "created_at" in task
        assert "updatedAt" in task or "updated_at" in task


def test_get_all_tasks_ordered_by_due_date(db_session, sample_tasks):
    """
    Test GET /api/tasks returns tasks ordered by due date ascending
    Expected: Oldest due date first
    """
    response = client.get("/api/tasks")
    
    assert response.status_code == 200
    data = response.json()
    
    # Extract due dates and verify ascending order
    due_dates = [task.get("dueDate") or task.get("due_date") for task in data]
    assert due_dates == sorted(due_dates)


def test_get_all_tasks_response_schema(db_session, sample_tasks):
    """
    Test GET /api/tasks response matches OpenAPI schema
    Expected: All required fields present with correct types
    """
    response = client.get("/api/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    
    task = data[0]
    
    # Verify data types
    assert isinstance(task["id"], int)
    assert isinstance(task["title"], str)
    assert isinstance(task["description"], str)
    assert isinstance(task["priority"], str)
    assert task["priority"] in ["Low", "Medium", "High"]
    assert isinstance(task["status"], str)
    assert task["status"] in ["Pending", "In Progress", "Completed"]
