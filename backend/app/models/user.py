from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class UserRole(str, Enum):
    ADMIN = "admin"
    OBSERVER = "observer"

class User(Base, TimestampMixin):  # ← AGGIUNGI TimestampMixin
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=True)
    nickname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.OBSERVER, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relazioni
    player = relationship("Player", back_populates="user", uselist=False)
    cazzaro = relationship("Cazzaro", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"