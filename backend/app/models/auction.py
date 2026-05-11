# backend/app/models/auction.py
from sqlalchemy import CheckConstraint, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class Auction(Base, TimestampMixin):
    """
    Asta mensile — un Player compra un Cazzaro per un mese.
    Vincolo: stesso Player non può comprare due Cazzari nello stesso mese.
    Vincolo: un Cazzaro non può essere comprato due volte nello stesso mese.
    """
    __tablename__ = "auctions"

    id          = Column(Integer, primary_key=True, index=True)
    season_id   = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    player_id   = Column(Integer, ForeignKey("players.id"), nullable=False)
    cazzaro_id  = Column(Integer, ForeignKey("cazzari.id"), nullable=False)
    month = Column(Integer, nullable=False)  # 1=Gennaio, 12=Dicembre
    cost        = Column(Integer, nullable=False)  # crediti spesi
    
    # Vincoli di unicità a livello di database
    __table_args__ = (
        UniqueConstraint("season_id", "player_id", "month",
                         name="uq_player_one_auction_per_month"),
        UniqueConstraint("season_id", "cazzaro_id", "month",
                         name="uq_cazzaro_one_auction_per_month"),
        CheckConstraint("player_id != cazzaro_id",
                        name="ck_player_cannot_buy_himself"),                         
    )

    # Relazioni
    season  = relationship("Season",  back_populates="auctions")
    player  = relationship("Player",  back_populates="auctions",
                           foreign_keys=[player_id])
    cazzaro = relationship("Cazzaro", back_populates="auctions",
                           foreign_keys=[cazzaro_id])

    def __repr__(self):
        return f"<Auction {self.player_id} → {self.cazzaro_id} {self.month}>"