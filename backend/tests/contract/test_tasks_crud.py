"""
TaskMaster Pro - Contract Tests for Task CRUD Operations
Generated with GitHub Copilot assistance
Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
User Stories 2, 3, 4 (P2-P4): Create, Update, Delete Tasks
"""

import pytest
from datetime import date, timedelta
from src.models.task import Task


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _future_date(days: int = 7) -> str:
    """Return an ISO-format date string that is `days` days from today."""
    return (date.today() + timedelta(days=days)).isoformat()


# ---------------------------------------------------------------------------
# POST /api/tasks
# ---------------------------------------------------------------------------

class TestCreateTask:
    """Contract tests for POST /api/tasks (User Story 2)."""

    def test_create_task_returns_201(self, client, db_session):
        """POST /api/tasks with valid data returns 201 Created."""
        payload = {
            "title": "New Task",
            "description": "Task description",
            "due_date": _future_date(7),
            "priority": "High",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)

        assert response.status_code == 201

    def test_create_task_returns_task_with_id(self, client, db_session):
        """POST /api/tasks returns the created task including generated id."""
        payload = {
            "title": "Task with ID",
            "description": "Should get an ID",
            "due_date": _future_date(5),
            "priority": "Medium",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)
        data = response.json()

        assert response.status_code == 201
        assert "id" in data
        assert isinstance(data["id"], int)
        assert data["title"] == payload["title"]
        assert data["description"] == payload["description"]
        assert data["priority"] == payload["priority"]
        assert data["status"] == payload["status"]

    def test_create_task_persists_in_database(self, client, db_session):
        """POST /api/tasks persists the task so GET /api/tasks returns it."""
        payload = {
            "title": "Persisted Task",
            "description": "Should appear in list",
            "due_date": _future_date(10),
            "priority": "Low",
            "status": "Pending",
        }
        client.post("/api/tasks", json=payload)

        response = client.get("/api/tasks")
        assert response.status_code == 200
        titles = [t["title"] for t in response.json()]
        assert payload["title"] in titles

    def test_create_task_missing_required_field_returns_422(self, client, db_session):
        """POST /api/tasks without 'title' returns 400 or 422 validation error."""
        payload = {
            "description": "No title here",
            "due_date": _future_date(7),
            "priority": "Low",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)

        assert response.status_code in [400, 422]

    def test_create_task_past_due_date_returns_422(self, client, db_session):
        """POST /api/tasks with a past due_date returns 400 or 422 validation error."""
        payload = {
            "title": "Past Due",
            "description": "Should be rejected",
            "due_date": "2020-01-01",
            "priority": "Low",
            "status": "Pending",
        }
        response = client.post("/api/tasks", json=payload)

        assert response.status_code in [400, 422]


# ---------------------------------------------------------------------------
# GET /api/tasks/{id}
# ---------------------------------------------------------------------------

class TestGetTaskById:
    """Contract tests for GET /api/tasks/{id}."""

    def test_get_task_by_id_returns_200(self, client, db_session):
        """GET /api/tasks/{id} for existing task returns 200 and correct task."""
        task = Task(
            title="Specific Task",
            description="For retrieval",
            due_date=date(2026, 4, 1),
            priority="High",
            status="Pending",
            reminder_sent=False,
        )
        db_session.add(task)
        db_session.commit()

        response = client.get(f"/api/tasks/{task.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == task.title

    def test_get_task_by_id_not_found_returns_404(self, client, db_session):
        """GET /api/tasks/{id} for non-existent task returns 404."""
        response = client.get("/api/tasks/99999")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# PUT /api/tasks/{id}
# ---------------------------------------------------------------------------

class TestUpdateTask:
    """Contract tests for PUT /api/tasks/{id} (User Story 4)."""

    def _create_task(self, db_session):
        task = Task(
            title="Original Title",
            description="Original description",
            due_date=date(2026, 4, 1),
            priority="Low",
            status="Pending",
            reminder_sent=False,
        )
        db_session.add(task)
        db_session.commit()
        return task

    def test_update_task_returns_200(self, client, db_session):
        """PUT /api/tasks/{id} with valid data returns 200 OK."""
        task = self._create_task(db_session)

        payload = {"title": "Updated Title"}
        response = client.put(f"/api/tasks/{task.id}", json=payload)

        assert response.status_code == 200

    def test_update_task_modifies_fields(self, client, db_session):
        """PUT /api/tasks/{id} updates the specified fields."""
        task = self._create_task(db_session)

        payload = {"title": "Updated Title", "status": "In Progress"}
        response = client.put(f"/api/tasks/{task.id}", json=payload)
        data = response.json()

        assert data["title"] == "Updated Title"
        assert data["status"] == "In Progress"

    def test_update_task_not_found_returns_404(self, client, db_session):
        """PUT /api/tasks/{id} for non-existent task returns 404."""
        payload = {"title": "Ghost"}
        response = client.put("/api/tasks/99999", json=payload)

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /api/tasks/{id}/status
# ---------------------------------------------------------------------------

class TestUpdateTaskStatus:
    """Contract tests for PATCH /api/tasks/{id}/status (User Story 3)."""

    def test_patch_status_returns_200(self, client, db_session):
        """PATCH /api/tasks/{id}/status updates only the status field."""
        task = Task(
            title="Status Task",
            description="Will change status",
            due_date=date(2026, 4, 5),
            priority="Medium",
            status="Pending",
            reminder_sent=False,
        )
        db_session.add(task)
        db_session.commit()

        response = client.patch(
            f"/api/tasks/{task.id}/status",
            json={"status": "Completed"},
        )

        assert response.status_code == 200
        assert response.json()["status"] == "Completed"

    def test_patch_status_not_found_returns_404(self, client, db_session):
        """PATCH /api/tasks/{id}/status for non-existent task returns 404."""
        response = client.patch("/api/tasks/99999/status", json={"status": "Completed"})

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /api/tasks/{id}
# ---------------------------------------------------------------------------

class TestDeleteTask:
    """Contract tests for DELETE /api/tasks/{id} (User Story 4)."""

    def test_delete_task_returns_204(self, client, db_session):
        """DELETE /api/tasks/{id} for existing task returns 204 No Content."""
        task = Task(
            title="To Delete",
            description="Will be deleted",
            due_date=date(2026, 4, 10),
            priority="Low",
            status="Pending",
            reminder_sent=False,
        )
        db_session.add(task)
        db_session.commit()

        response = client.delete(f"/api/tasks/{task.id}")

        assert response.status_code == 204

    def test_delete_task_removes_from_database(self, client, db_session):
        """DELETE /api/tasks/{id} removes the task so it is no longer returned."""
        task = Task(
            title="Ephemeral",
            description="Will disappear",
            due_date=date(2026, 4, 10),
            priority="Low",
            status="Pending",
            reminder_sent=False,
        )
        db_session.add(task)
        db_session.commit()
        task_id = task.id

        client.delete(f"/api/tasks/{task_id}")

        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404

    def test_delete_task_not_found_returns_404(self, client, db_session):
        """DELETE /api/tasks/{id} for non-existent task returns 404."""
        response = client.delete("/api/tasks/99999")

        assert response.status_code == 404
