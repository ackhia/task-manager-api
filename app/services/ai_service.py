import uuid


from app.models.user import User
from sqlalchemy.orm import Session
from app.ai_clients import OpenAIClient
from app.models import Job
from app.workers.task_worker import enqueue_create_tasks

from dotenv import load_dotenv

load_dotenv()


# ----------------------------
# Create a set of tasks based on a description
# ----------------------------
async def create_tasks(db: Session, desc: str, owner: User, ai_client: OpenAIClient) -> Job:
    """
    Creates a new task in the database, linked to the owner (user).
    """
    job = Job(
        id=uuid.uuid4(),
        status="pending",
        owner_id=owner.id,
    )

    db.add(job)

    try:
        db.commit()
        db.refresh(job)

        enqueue_create_tasks.send(desc, str(job.id))

        return job

    except Exception:
        db.rollback()
        raise


class JobNotFound(Exception):
    pass

# ----------------------------
# Get the status of a job
# ----------------------------
def get_job_status(db: Session, job_id: uuid.UUID, owner: User) -> Job:
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.owner_id == owner.id)
        .first()
    )

    if not job:
        raise JobNotFound()

    return job