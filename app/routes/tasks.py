from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import create_task, list_tasks, get_task, update_task, delete_task
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


# --------------------------
# Create a new task
# --------------------------
@router.post("/", response_model=TaskRead)
def create(task_in: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Create a new task assigned to the logged-in user.
    """
    return create_task(db, task_in, current_user)


# --------------------------
# List all tasks for current user
# --------------------------
@router.get("/", response_model=List[TaskRead])
def read_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    List all tasks belonging to the logged-in user.
    """
    return list_tasks(db, current_user)


# --------------------------
# Get a specific task by ID
# --------------------------
@router.get("/{task_id}", response_model=TaskRead)
def read_task(task_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get a task by its ID. Only accessible by the owner.
    """
    task = get_task(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# --------------------------
# Update a task
# --------------------------
@router.put("/{task_id}", response_model=TaskRead)
def update(task_id: UUID, task_in: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Update a task. Only accessible by the owner.
    """
    task = get_task(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task, task_in)


# --------------------------
# Delete a task
# --------------------------
@router.delete("/{task_id}", status_code=204)
def delete(task_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Delete a task. Only accessible by the owner.
    """
    task = get_task(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(db, task)