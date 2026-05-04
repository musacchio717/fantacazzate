# backend/app/models/base.py
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    """Aggiunge created_at e updated_at a ogni modello che lo usa."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)