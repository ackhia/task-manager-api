from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.user import User

# ----------------------------
# Create a new task
# ----------------------------
def create_task(db: Session, task_in: TaskCreate, owner: User) -> Task:
    """
    Creates a new task in the database, linked to the owner (user).
    """
    task = Task(
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        owner_id=owner.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# ----------------------------
# Get a task by ID (only for owner)
# ----------------------------
def get_task(db: Session, task_id: UUID, owner: User) -> Optional[Task]:
    """
    Returns a single task owned by the user, or None if not found.
    """
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner.id).first()


# ----------------------------
# List all tasks for a user
# ----------------------------
def list_tasks(db: Session, owner: User, skip: int = 0, limit: int = 100) -> List[Task]:
    """
    Returns all tasks for a specific user, with optional pagination.
    """
    return db.query(Task).filter(Task.owner_id == owner.id).offset(skip).limit(limit).all()


# ----------------------------
# Update a task
# ----------------------------
def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    """
    Updates a task instance with new data from a TaskUpdate schema.
    """
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task


# ----------------------------
# Delete a task
# ----------------------------
def delete_task(db: Session, task: Task) -> None:
    """
    Deletes a task instance from the database.
    """
    db.delete(task)
    db.commit()