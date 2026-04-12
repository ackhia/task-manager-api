
from app.models.user import User
from sqlalchemy.orm import Session
from fastapi import Depends
from app.ai_clients import OpenAIClient
from app.schemas.async_job import AsyncJob
from app.models.task import Task
from app.models import Job

import uuid


# ----------------------------
# Create a set of tasks based on a description
# ----------------------------
async def create_tasks(db: Session, desc: str, owner: User, ai_client: OpenAIClient) -> Job:
    """
    Creates a new task in the database, linked to the owner (user).
    """
    job_id = await ai_client.generate_tasks(desc)

    job = Job(
        job_id=job_id,
        status="pending",
        owner_id=owner.id
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return job