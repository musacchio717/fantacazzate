# backend/app/models/season.py
from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Season(Base, TimestampMixin):
    """
    Contenitore di tutto — una stagione di gioco.
    Tutte le aste e cazzate appartengono a una Season.
    """
    __tablename__ = "seasons"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String, nullable=False)
    initial_budget = Column(Integer, nullable=False, default=500)
    start_date     = Column(Date, nullable=True)
    end_date       = Column(Date, nullable=True)
    is_active      = Column(Boolean, default=False, nullable=False)

    # Relazioni
    cazzate  = relationship("Cazzata",  back_populates="season")
    auctions = relationship("Auction",  back_populates="season")

    def __repr__(self):
        return f"<Season {self.name} active={self.is_active}>"