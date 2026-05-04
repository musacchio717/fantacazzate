# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id               = Column(Integer, primary_key=True, index=True)
    email            = Column(String, unique=True, nullable=False, index=True)
    nickname         = Column(String, unique=True, nullable=False)
    hashed_password  = Column(String, nullable=False)
    is_active        = Column(Boolean, default=True, nullable=False)

    # Relazioni — un User può avere UN Player e UN Cazzaro
    player  = relationship("Player",  back_populates="user", uselist=False)
    cazzaro = relationship("Cazzaro", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.nickname}>"