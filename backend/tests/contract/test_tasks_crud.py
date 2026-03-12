"""
TaskMaster Pro - Contract Tests for CRUD Operations
Test-Driven Development: User Stories P2–P4
Covers POST /api/tasks, GET /api/tasks/{id},
PUT /api/tasks/{id}, PATCH /api/tasks/{id}/status, DELETE /api/tasks/{id}
"""

import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from src.main import app
from src.database import Base, engine, SessionLocal
from src.models.task import Task

client = TestClient(app)

FUTURE_DATE = (date.today() + timedelta(days=7)).isoformat()
FAR_FUTURE = (date.today() + timedelta(days=30)).isoformat()


@pytest.fixture(scope="function")
def db_session():
    """Fresh in-memory SQLite session for each test."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def existing_task(db_session):
    """Insert a single task and return it."""
    task = Task(
        title="Existing Task",
        description="Already in the database",
        due_date=date.today() + timedelta(days=10),
        priority="Medium",
        status="Pending",
        reminder_sent=False,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


# ---------------------------------------------------------------------------
# POST /api/tasks
# ---------------------------------------------------------------------------

class TestCreateTask:
    def test_create_task_returns_201(self, db_session):
        payload = {
            "title": "New Task",
            "description": "A brand-new task",
            "due_date": FUTURE_DATE,
            "priority": "High",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201

    def test_create_task_response_contains_id(self, db_session):
        payload = {
            "title": "Task with ID",
            "description": "Should get an auto-increment id",
            "due_date": FUTURE_DATE,
            "priority": "Low",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_task_persists_to_database(self, db_session):
        payload = {
            "title": "Persistent Task",
            "description": "Should appear in GET /api/tasks",
            "due_date": FUTURE_DATE,
            "priority": "Medium",
            "status": "In Progress",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 201
        task_id = response.json()["id"]

        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["id"] == task_id

    def test_create_task_with_past_due_date_returns_422(self, db_session):
        past_date = (date.today() - timedelta(days=1)).isoformat()
        payload = {
            "title": "Late Task",
            "description": "Due date is in the past",
            "due_date": past_date,
            "priority": "Low",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 422

    def test_create_task_missing_required_field_returns_422(self, db_session):
        payload = {
            "description": "No title provided",
            "due_date": FUTURE_DATE,
            "priority": "Low",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/tasks/{task_id}
# ---------------------------------------------------------------------------

class TestGetTaskById:
    def test_get_existing_task_returns_200(self, db_session, existing_task):
        response = client.get(f"/api/tasks/{existing_task.id}")
        assert response.status_code == 200

    def test_get_existing_task_returns_correct_data(self, db_session, existing_task):
        response = client.get(f"/api/tasks/{existing_task.id}")
        data = response.json()
        assert data["id"] == existing_task.id
        assert data["title"] == existing_task.title

    def test_get_nonexistent_task_returns_404(self, db_session):
        response = client.get("/api/tasks/99999")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# PUT /api/tasks/{task_id}
# ---------------------------------------------------------------------------

class TestUpdateTask:
    def test_update_task_returns_200(self, db_session, existing_task):
        payload = {
            "title": "Updated Title",
            "description": "Updated description",
            "due_date": FAR_FUTURE,
            "priority": "High",
            "status": "In Progress",
        }
        response = client.put(f"/api/tasks/{existing_task.id}", json=payload)
        assert response.status_code == 200

    def test_update_task_changes_fields(self, db_session, existing_task):
        payload = {"title": "Changed Title", "status": "Completed"}
        response = client.put(f"/api/tasks/{existing_task.id}", json=payload)
        assert response.json()["title"] == "Changed Title"
        assert response.json()["status"] == "Completed"

    def test_update_nonexistent_task_returns_404(self, db_session):
        payload = {"title": "Ghost Update", "status": "Completed"}
        response = client.put("/api/tasks/99999", json=payload)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /api/tasks/{task_id}/status
# ---------------------------------------------------------------------------

class TestUpdateTaskStatus:
    def test_patch_status_returns_200(self, db_session, existing_task):
        payload = {"status": "Completed"}
        response = client.patch(f"/api/tasks/{existing_task.id}/status", json=payload)
        assert response.status_code == 200

    def test_patch_status_updates_status_field(self, db_session, existing_task):
        payload = {"status": "In Progress"}
        response = client.patch(f"/api/tasks/{existing_task.id}/status", json=payload)
        assert response.json()["status"] == "In Progress"

    def test_patch_status_nonexistent_task_returns_404(self, db_session):
        payload = {"status": "Completed"}
        response = client.patch("/api/tasks/99999/status", json=payload)
        assert response.status_code == 404

    def test_patch_invalid_status_returns_422(self, db_session, existing_task):
        payload = {"status": "Bogus"}
        response = client.patch(f"/api/tasks/{existing_task.id}/status", json=payload)
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# DELETE /api/tasks/{task_id}
# ---------------------------------------------------------------------------

class TestDeleteTask:
    def test_delete_task_returns_204(self, db_session, existing_task):
        response = client.delete(f"/api/tasks/{existing_task.id}")
        assert response.status_code == 204

    def test_delete_task_removes_from_database(self, db_session, existing_task):
        task_id = existing_task.id
        client.delete(f"/api/tasks/{task_id}")
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_task_returns_404(self, db_session):
        response = client.delete("/api/tasks/99999")
        assert response.status_code == 404
