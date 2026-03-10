import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import create_user
from app.api.dependencies import get_current_user
from .conftest import prefix 


def test_task_crud_and_permissions(client: TestClient, db_session):
    prefix_ = prefix()

    # Create two users: owner and other
    owner = create_user(db_session, email="owner@example.com", full_name="Owner", password="secret")
    other = create_user(db_session, email="other@example.com", full_name="Other", password="secret")

    # Helper to override auth dependency
    def set_current(user):
        app.dependency_overrides[get_current_user] = lambda: user

    def clear_override():
        app.dependency_overrides.pop(get_current_user, None)

    # Use owner for the following operations
    set_current(owner)

    # 1) Create a task
    payload = {"title": "Test Task", "description": "Do something important."}
    r = client.post(f"{prefix_}/tasks/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == payload["title"]
    task_id = data["id"]

    # 2) List tasks (owner should see it)
    r = client.get(f"{prefix_}/tasks/")
    assert r.status_code == 200
    items = r.json()
    assert any(t["id"] == task_id for t in items)

    # 3) Get task by id
    r = client.get(f"{prefix_}/tasks/{task_id}" if prefix_ else f"/tasks/{task_id}")
    assert r.status_code == 200
    got = r.json()
    assert got["id"] == task_id

    # 4) Update the task
    update_payload = {"title": "Updated title", "is_completed": True}
    r = client.put(f"{prefix_}/tasks/{task_id}" if prefix_ else f"/tasks/{task_id}", json=update_payload)
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"] == "Updated title"
    assert updated["is_completed"] is True

    # Get the task again to confirm update
    r = client.get(f"{prefix_}/tasks/{task_id}")
    assert r.status_code == 200
    got = r.json()
    assert got["title"] == "Updated title"  
    assert got["is_completed"] is True

    # 5) Permission check: other user cannot access owner's task
    set_current(other)
    r = client.get(f"{prefix_}/tasks/{task_id}" if prefix_ else f"/tasks/{task_id}")
    assert r.status_code == 404

    # 6) Other's list is empty
    r = client.get(f"{prefix_}/tasks/")
    assert r.status_code == 200
    assert r.json() == []

    # 7) Owner deletes the task
    set_current(owner)
    r = client.delete(f"{prefix_}/tasks/{task_id}" if prefix_ else f"/tasks/{task_id}")
    assert r.status_code == 204

    # 8) Deleted task is gone
    r = client.get(f"{prefix_}/tasks/{task_id}" if prefix_ else f"/tasks/{task_id}")
    assert r.status_code == 404

    clear_override()


def test_validation_and_not_found(client: TestClient, db_session):
    prefix_ = prefix()

    user = create_user(db_session, email="vuser@example.com", full_name="VUser", password="secret")

    # override
    app.dependency_overrides[get_current_user] = lambda: user

    # Validation: missing title should 422
    bad = {"title": "", "description": "no title"}
    r = client.post(f"{prefix_}/tasks/", json=bad)
    assert r.status_code == 422

    # Not found for random uuid
    random_id = uuid.uuid4()
    r = client.get(f"{prefix_}/tasks/{random_id}" if prefix_ else f"/tasks/{random_id}")
    assert r.status_code == 404

    # cleanup
    app.dependency_overrides.pop(get_current_user, None)
