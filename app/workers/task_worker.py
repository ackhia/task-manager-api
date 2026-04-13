

import dramatiq
from google import genai
from types import SimpleNamespace
from app.db.session import SessionLocal
from app.models import Job
from uuid import UUID


@dramatiq.actor
def enqueue_create_tasks(desc: str, job_id: str):
    client = genai.Client()

    # resp = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents=desc
    # )

    resp = SimpleNamespace()
    resp.text = "Generated tasks based on description: " + desc  # Placeholder response text

    db = SessionLocal()
    job = db.query(Job).filter(Job.id == UUID(job_id)).first()
    job.status = "completed"
    job.result = resp.text
    db.commit()