
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db
from fastapi.testclient import TestClient


TEST_DB_FILENAME = "./test.db"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///" + TEST_DB_FILENAME, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()     
        if os.path.exists(TEST_DB_FILENAME):
            os.remove(TEST_DB_FILENAME)  

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.pop(get_db)


def prefix():
    # Respect BASE_URI if set in environment (tests run in same environment as app)
    base = os.environ.get("BASE_URI") or ""
    return base.rstrip("/")