import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://openhive:openhive@localhost:5432/openhive'

# Create engine
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def init_db():
    # Import here to avoid circular imports when models import Base
    from . import db_models
    Base.metadata.create_all(bind=engine)

# Utility: update task status generically
def update_task_status_by_id(task_id: str, status: str, result: dict = None):
    from .db_models import Task
    db = SessionLocal()
    try:
        t = db.query(Task).filter(Task.task_id == task_id).first()
        if not t:
            return False
        t.status = status
        if result is not None:
            t.result = result
        db.commit()
        return True
    finally:
        db.close()
