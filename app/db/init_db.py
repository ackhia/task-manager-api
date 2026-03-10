from app.db.session import Base, engine
from app.models.user import User
from app.models.task import Task  

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)