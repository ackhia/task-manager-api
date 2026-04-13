
import uuid

from pydantic import BaseModel, Field
from typing import Any, Optional


class AsyncJob(BaseModel):
    job_id: uuid.UUID = Field(..., description="The unique identifier for the asynchronous job", alias="id")
    status: str = Field(..., description="The current status of the asynchronous job")
    result: Optional[str] = Field(None, description="The result of the asynchronous job")