from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai_clients.openai import OpenAIClient
from app.db.session import get_db
from app.schemas.async_job import AsyncJob
import app.services.ai_service as ai_service
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


# --------------------------
# Create a new task
# --------------------------
@router.post("/create-tasks", response_model=AsyncJob)
async def create_tasks(desc: str, db: Session = Depends(get_db), current_user=Depends(get_current_user), ai_client: OpenAIClient = Depends(OpenAIClient)):
    """
    Create a set of tasks based on a description. The description will be processed by an AI model to generate multiple tasks.
    """

    return await ai_service.create_tasks(db, desc, current_user, ai_client)