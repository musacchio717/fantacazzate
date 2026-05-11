# backend/app/services/auction_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.auction import Auction
from app.models.player import Player, Cazzaro
from app.models.user import User
from app.schemas.auction import AuctionCreate, AuctionUpdate

class AuctionService:
    def __init__(self, db: Session):
        self.db = db

    def _enrich(self, auction: Auction) -> Auction:
        """Aggiunge nickname al player e al cazzaro."""
        player = self.db.query(Player).filter(
            Player.id == auction.player_id).first()
        if player and player.user:
            auction.player_nickname = player.user.nickname

        cazzaro = self.db.query(Cazzaro).filter(
            Cazzaro.id == auction.cazzaro_id).first()
        if cazzaro:
            auction.cazzaro_nickname = cazzaro.nickname

        return auction

    def create_auction(self, data: AuctionCreate) -> Auction:
        player  = self.db.query(Player).filter(
                    Player.id == data.player_id).first()
        cazzaro = self.db.query(Cazzaro).filter(
                    Cazzaro.id == data.cazzaro_id).first()

        if not player or not cazzaro:
            raise ValueError("Player o Cazzaro non trovato")

        if cazzaro.user_id and cazzaro.user_id == player.user_id:
            raise ValueError("Un Player non può comprare se stesso")

        try:
            auction = Auction(**data.model_dump())
            self.db.add(auction)
            self.db.commit()
            self.db.refresh(auction)
            return self._enrich(auction)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Asta duplicata per questo mese")

    def get_auction(self, auction_id: int) -> Auction | None:
        auction = self.db.query(Auction).filter(
                    Auction.id == auction_id).first()
        if auction:
            return self._enrich(auction)
        return None

    def get_auctions(self, season_id: int,
                     month: int | None = None) -> list[Auction]:
        query = self.db.query(Auction).filter(
                    Auction.season_id == season_id)
        if month:
            query = query.filter(Auction.month == month)
        auctions = query.all()
        return [self._enrich(a) for a in auctions]

    def update_auction(self, auction_id: int,
                       data: AuctionUpdate) -> Auction | None:
        auction = self.get_auction(auction_id)
        if not auction:
            return None

        if data.cazzaro_id:
            player  = self.db.query(Player).filter(
                        Player.id == auction.player_id).first()
            cazzaro = self.db.query(Cazzaro).filter(
                        Cazzaro.id == data.cazzaro_id).first()
            if cazzaro and cazzaro.user_id == player.user_id:
                raise ValueError("Un Player non può comprare se stesso")
            auction.cazzaro_id = data.cazzaro_id

        if data.cost is not None:
            auction.cost = data.cost

        try:
            self.db.commit()
            self.db.refresh(auction)
            return self._enrich(auction)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Modifica non valida — vincolo violato")

    def delete_auction(self, auction_id: int) -> bool:
        auction = self.db.query(Auction).filter(
                    Auction.id == auction_id).first()
        if not auction:
            return False
        self.db.delete(auction)
        self.db.commit()
        return True