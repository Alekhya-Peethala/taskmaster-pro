"""
TaskMaster Pro - Contract Test for GET /api/tasks with Status Filter
Generated with GitHub Copilot assistance
Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
User Story 1: View and Filter Tasks (P1) - Filter by status requirement
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import Base, engine, SessionLocal
from src.models.task import Task
from datetime import date

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
def mixed_status_tasks(db_session):
    """Create tasks with different statuses for filter testing"""
    tasks = [
        Task(title=f"Pending Task {i}", description=f"Desc {i}", 
             due_date=date(2026, 3, 15 + i), priority="Medium", status="Pending")
        for i in range(3)
    ] + [
        Task(title=f"In Progress Task {i}", description=f"Desc {i}",
             due_date=date(2026, 3, 20 + i), priority="High", status="In Progress")
        for i in range(2)
    ] + [
        Task(title=f"Completed Task {i}", description=f"Desc {i}",
             due_date=date(2026, 3, 10 + i), priority="Low", status="Completed")
        for i in range(4)
    ]
    
    for task in tasks:
        db_session.add(task)
    db_session.commit()
    return tasks


def test_filter_by_pending_status(db_session, mixed_status_tasks):
    """
    Test GET /api/tasks?status=Pending returns only pending tasks
    Expected: 3 pending tasks
    """
    response = client.get("/api/tasks?status=Pending")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Verify all returned tasks have Pending status
    for task in data:
        assert task["status"] == "Pending"


def test_filter_by_in_progress_status(db_session, mixed_status_tasks):
    """
    Test GET /api/tasks?status=In Progress returns only in-progress tasks
    Expected: 2 in-progress tasks
    """
    response = client.get("/api/tasks?status=In Progress")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    for task in data:
        assert task["status"] == "In Progress"


def test_filter_by_completed_status(db_session, mixed_status_tasks):
    """
    Test GET /api/tasks?status=Completed returns only completed tasks
    Expected: 4 completed tasks
    """
    response = client.get("/api/tasks?status=Completed")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    
    for task in data:
        assert task["status"] == "Completed"


def test_filter_invalid_status(db_session, mixed_status_tasks):
    """
    Test GET /api/tasks?status=InvalidStatus returns 400 Bad Request
    Expected: Validation error
    """
    response = client.get("/api/tasks?status=InvalidStatus")
    
    # Should either return 400 or 422 for validation error
    assert response.status_code in [400, 422]


def test_filter_returns_empty_when_no_matches(db_session):
    """
    Test GET /api/tasks?status=Pending returns empty array when no pending tasks
    Expected: 200 OK with empty array
    """
    # Create only completed tasks
    task = Task(title="Completed", description="Desc", 
                due_date=date(2026, 3, 15), priority="Low", status="Completed")
    db_session.add(task)
    db_session.commit()
    
    response = client.get("/api/tasks?status=Pending")
    
    assert response.status_code == 200
    assert response.json() == []
