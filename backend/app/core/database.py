# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency FastAPI — inietta la sessione DB in ogni endpoint."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()