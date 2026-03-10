

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

# Shared properties
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    is_completed: bool = False
    due_date: Optional[datetime] = None


# Used when creating a task
class TaskCreate(TaskBase):
    pass


# Used when updating (all optional)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None


# What we return to clients
class TaskRead(TaskBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  