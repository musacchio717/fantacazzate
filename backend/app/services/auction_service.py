# backend/app/services/auction_service.py
from sqlalchemy.orm import Session
from app.models.auction import Auction
from app.models.player import Player, Cazzaro
from app.schemas.auction import AuctionCreate

class AuctionService:
    def __init__(self, db: Session):
        self.db = db

    def create_auction(self, data: AuctionCreate) -> Auction:
        # Recupera Player e Cazzaro
        player  = self.db.query(Player).filter(Player.id == data.player_id).first()
        cazzaro = self.db.query(Cazzaro).filter(Cazzaro.id == data.cazzaro_id).first()

        if not player or not cazzaro:
            raise ValueError("Player o Cazzaro non trovato")

        # Vincolo: un Player non può comprare se stesso
        if cazzaro.user_id and cazzaro.user_id == player.user_id:
            raise ValueError("Un Player non può comprare se stesso come Cazzaro")

        auction = Auction(
            season_id  = data.season_id,
            player_id  = data.player_id,
            cazzaro_id = data.cazzaro_id,
            month      = data.month,
            cost       = data.cost,
        )
        
        self.db.add(auction)
        self.db.commit()
        self.db.refresh(auction)
        return auction