# backend/app/models/cazzata.py
import enum
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class CazzataStatus(enum.Enum):
    PENDING   = "pending"    # inserita, punteggio da decidere
    CONFIRMED = "confirmed"  # punteggio votato e confermato

class Cazzata(Base, TimestampMixin):
    """
    Singolo evento generato da un Cazzaro.
    Il punteggio (1-10) viene assegnato democraticamente dal gruppo.
    """
    __tablename__ = "cazzate"

    id          = Column(Integer, primary_key=True, index=True)
    cazzaro_id  = Column(Integer, ForeignKey("cazzari.id"), nullable=False)
    season_id   = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    date        = Column(Date, nullable=False)
    month = Column(Integer, nullable=False)  # 1=Gennaio, 12=Dicembre
    description = Column(Text, nullable=False)
    score       = Column(Integer, nullable=True)   # null finché PENDING
    status      = Column(
                    Enum(CazzataStatus),
                    default=CazzataStatus.PENDING,
                    nullable=False
                  )
    submitted_by = Column(Integer, ForeignKey("players.id"), nullable=True)

    # Relazioni
    cazzaro = relationship("Cazzaro", back_populates="cazzate")
    season  = relationship("Season",  back_populates="cazzate")

    def __repr__(self):
        return f"<Cazzata {self.cazzaro_id} {self.month} score={self.score}>"