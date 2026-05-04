# backend/app/models/player.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Player(Base, TimestampMixin):
    """
    Rappresenta un utente che partecipa come ALLENATORE.
    Ha un budget, compra i Cazzari alle aste, accumula punti.
    """
    __tablename__ = "players"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"),
                         nullable=False, unique=True)
    is_active   = Column(Boolean, default=True, nullable=False)

    # Relazioni
    user     = relationship("User", back_populates="player")
    auctions = relationship("Auction", back_populates="player",
                            foreign_keys="Auction.player_id")

    def __repr__(self):
        return f"<Player user_id={self.user_id}>"


class Cazzaro(Base, TimestampMixin):
    """
    Rappresenta chi genera le cazzate e i punti.
    user_id è nullable — in futuro potremmo avere Cazzari
    senza account (personaggi pubblici, ecc.)
    """
    __tablename__ = "cazzari"

    id        = Column(Integer, primary_key=True, index=True)
    user_id   = Column(Integer, ForeignKey("users.id"),
                       nullable=True, unique=True)  # nullable = espandibile
    nickname  = Column(String, nullable=False)
    bio       = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relazioni
    user     = relationship("User", back_populates="cazzaro")
    cazzate  = relationship("Cazzata", back_populates="cazzaro")
    auctions = relationship("Auction", back_populates="cazzaro",
                            foreign_keys="Auction.cazzaro_id")

    def __repr__(self):
        return f"<Cazzaro {self.nickname}>"