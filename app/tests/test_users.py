import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import create_user
from app.api.dependencies import get_current_user
from .conftest import prefix


def test_read_current_user(client: TestClient, db_session):
    prefix_ = prefix()

    user = create_user(db_session, email="me@example.com", full_name="Me", password="supersecret")

    app.dependency_overrides[get_current_user] = lambda: user

    r = client.get(f"{prefix_}/users/me")
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "me@example.com"
    assert data["full_name"] == "Me"

    app.dependency_overrides.pop(get_current_user, None)


def test_read_user_and_not_found(client: TestClient, db_session):
    prefix_ = prefix()

    a = create_user(db_session, email="a@example.com", full_name="A", password="password123")
    b = create_user(db_session, email="b@example.com", full_name="B", password="password123")

    # Auth as A
    app.dependency_overrides[get_current_user] = lambda: a

    # Read B by id
    r = client.get(f"{prefix_}/users/{b.id}")
    assert r.status_code == 200
    got = r.json()
    assert got["email"] == "b@example.com"

    # Random UUID -> 404
    r = client.get(f"{prefix_}/users/{uuid.uuid4()}")
    assert r.status_code == 404

    app.dependency_overrides.pop(get_current_user, None)


def test_list_users(client: TestClient, db_session):
    prefix_ = prefix()

    # Create several users
    emails = ["list1@example.com", "list2@example.com", "list3@example.com"]
    created = []
    for i, e in enumerate(emails):
        u = create_user(db_session, email=e, full_name=f"User{i}", password="password123")
        created.append(u)

    # Authenticate as first user
    app.dependency_overrides[get_current_user] = lambda: created[0]

    r = client.get(f"{prefix_}/users/")
    assert r.status_code == 200
    data = r.json()
    returned_emails = {u["email"] for u in data}
    for e in emails:
        assert e in returned_emails

    app.dependency_overrides.pop(get_current_user, None)
