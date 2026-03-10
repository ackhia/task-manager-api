
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Ensure folder exists
os.makedirs("./data", exist_ok=True)

# ----------------------------
# Database URL
# ----------------------------
DATABASE_URL = "sqlite:///./data/task-manager.db"

# ----------------------------
# SQLAlchemy engine
# ----------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
)

# ----------------------------
# Session factory
# ----------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ----------------------------
# Base class for models
# ----------------------------
Base = declarative_base()

# ----------------------------
# Dependency for FastAPI routes
# ----------------------------
def get_db():
    """
    Yields a SQLAlchemy Session for FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()