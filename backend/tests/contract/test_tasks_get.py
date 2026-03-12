"""
TaskMaster Pro - Contract Test for GET /api/tasks
Generated with GitHub Copilot assistance
Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
User Story 1: View and Filter Tasks (P1)
"""

import pytest
from src.models.task import Task
from datetime import date


@pytest.fixture
def sample_tasks(db_session):
    """Create sample tasks in the SQLite test database."""
    tasks = [
        Task(
            title="Task 1 - Pending",
            description="Description for task 1",
            due_date=date(2026, 4, 15),
            priority="High",
            status="Pending",
            reminder_sent=False
        ),
        Task(
            title="Task 2 - In Progress",
            description="Description for task 2",
            due_date=date(2026, 4, 16),
            priority="Medium",
            status="In Progress",
            reminder_sent=False
        ),
        Task(
            title="Task 3 - Completed",
            description="Description for task 3",
            due_date=date(2026, 4, 17),
            priority="Low",
            status="Completed",
            reminder_sent=True
        ),
    ]
    for task in tasks:
        db_session.add(task)
    db_session.commit()
    return tasks


def test_get_all_tasks_empty_database(client, db_session):
    """
    Test GET /api/tasks returns empty array when no tasks exist.
    Expected: 200 OK with empty array []
    """
    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks_with_data(client, db_session, sample_tasks):
    """
    Test GET /api/tasks returns all tasks.
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
        assert "due_date" in task
        assert "priority" in task
        assert "status" in task
        assert "reminder_sent" in task
        assert "created_at" in task
        assert "updated_at" in task


def test_get_all_tasks_ordered_by_due_date(client, db_session, sample_tasks):
    """
    Test GET /api/tasks returns tasks ordered by due date ascending.
    Expected: Earliest due date first
    """
    response = client.get("/api/tasks")

    assert response.status_code == 200
    data = response.json()

    due_dates = [task["due_date"] for task in data]
    assert due_dates == sorted(due_dates)


def test_get_all_tasks_response_schema(client, db_session, sample_tasks):
    """
    Test GET /api/tasks response matches OpenAPI schema.
    Expected: All required fields present with correct types
    """
    response = client.get("/api/tasks")

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    task = data[0]

    assert isinstance(task["id"], int)
    assert isinstance(task["title"], str)
    assert isinstance(task["description"], str)
    assert isinstance(task["priority"], str)
    assert task["priority"] in ["Low", "Medium", "High"]
    assert isinstance(task["status"], str)
    assert task["status"] in ["Pending", "In Progress", "Completed"]
