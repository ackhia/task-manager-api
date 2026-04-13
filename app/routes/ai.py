import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai_clients.openai import OpenAIClient
from app.db.session import get_db
from app.schemas.async_job import AsyncJob
from app.schemas.task import CreateTasksRequest
import app.services.ai_service as ai_service
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


# --------------------------
# Create a new task
# --------------------------
@router.post("/create-tasks", response_model=AsyncJob, status_code=202)
async def create_tasks(body: CreateTasksRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user), ai_client: OpenAIClient = Depends(OpenAIClient)):
    """
    Create a set of tasks based on a description. The description will be processed by an AI model to generate multiple tasks.
    """
    return await ai_service.create_tasks(db, body.desc, current_user, ai_client)


# --------------------------
# Get the status of a job
# --------------------------
@router.get("/job-status/{job_id}", response_model=AsyncJob)
async def get_job_status(job_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get the status of a job by its ID. This will return the current status of the job (e.g., pending, completed) and any results if available.
    """
    try:
        return ai_service.get_job_status(db, job_id, current_user)
    except ai_service.JobNotFound:
        raise HTTPException(status_code=404, detail="Job not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job_id")