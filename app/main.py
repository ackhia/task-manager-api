
import os

from fastapi import FastAPI
from app.routes import tasks, auth, users, ai
from app.db.init_db import init_db 
from dotenv import load_dotenv

load_dotenv()

def create_app() -> FastAPI:
    init_db()

    app = FastAPI(
        title="Task Manager API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    prefix = os.environ.get("BASE_URI", "")
    app.include_router(auth.router, prefix=prefix, tags=["auth"])
    app.include_router(tasks.router, prefix=prefix, tags=["tasks"])
    app.include_router(users.router, prefix=prefix, tags=["users"])
    app.include_router(ai.router, prefix=prefix, tags=["ai"])
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)