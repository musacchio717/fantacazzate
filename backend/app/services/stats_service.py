# backend/app/services/stats_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cazzata import Cazzata, CazzataStatus
from app.models.auction import Auction
from app.models.player import Player, Cazzaro
from app.models.season import Season
from app.schemas.stats import StandingOut, PlayerStatsOut, BudgetOut

class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def _get_player_points(self, player_id: int, season_id: int) -> int:
        """Punti totali di un Player nella stagione."""
        auctions = self.db.query(Auction).filter(
            Auction.player_id == player_id,
            Auction.season_id == season_id
        ).all()

        total = 0
        for auction in auctions:
            points = self.db.query(func.sum(Cazzata.score)).filter(
                Cazzata.cazzaro_id == auction.cazzaro_id,
                Cazzata.season_id  == season_id,
                Cazzata.month      == auction.month,
                Cazzata.status     == CazzataStatus.CONFIRMED
            ).scalar() or 0
            total += points
        return total

    def _get_player_points_by_month(self, player_id: int,
                                     season_id: int) -> dict[int, int]:
        """Punti mensili di un Player — dizionario mese → punti."""
        auctions = self.db.query(Auction).filter(
            Auction.player_id == player_id,
            Auction.season_id == season_id
        ).all()

        monthly = {}
        for auction in auctions:
            points = self.db.query(func.sum(Cazzata.score)).filter(
                Cazzata.cazzaro_id == auction.cazzaro_id,
                Cazzata.season_id  == season_id,
                Cazzata.month      == auction.month,
                Cazzata.status     == CazzataStatus.CONFIRMED
            ).scalar() or 0
            monthly[auction.month] = points
        return monthly

    def get_standings(self, season_id: int) -> list[StandingOut]:
        """Classifica completa — aggiornata in tempo reale."""
        players = self.db.query(Player).filter(
                    Player.is_active == True).all()

        standings = []
        for player in players:
            total_points = self._get_player_points(player.id, season_id)
            monthly      = self._get_player_points_by_month(
                                player.id, season_id)
            standings.append({
                "nickname":      player.user.nickname,
                "points":        total_points,
                "monthly_points": monthly,
            })

        standings.sort(key=lambda x: x["points"], reverse=True)
        return [
            StandingOut(position=i+1, **s)
            for i, s in enumerate(standings)
        ]

    def get_player_stats(self, season_id: int) -> list[PlayerStatsOut]:
        """Statistiche per ogni Cazzaro."""
        cazzari = self.db.query(Cazzaro).filter(
                    Cazzaro.is_active == True).all()

        stats = []
        for cazzaro in cazzari:
            cazzate   = self.db.query(Cazzata).filter(
                Cazzata.cazzaro_id == cazzaro.id,
                Cazzata.season_id  == season_id
            ).all()

            confirmed = [c for c in cazzate
                         if c.status == CazzataStatus.CONFIRMED]
            pending   = [c for c in cazzate
                         if c.status == CazzataStatus.PENDING]
            scores    = [c.score for c in confirmed if c.score]
            avg       = round(sum(scores)/len(scores), 2) if scores else None

            stats.append(PlayerStatsOut(
                nickname=cazzaro.nickname,
                total_cazzate=len(cazzate),
                confirmed_cazzate=len(confirmed),
                pending_cazzate=len(pending),
                avg_score=avg,
                total_points=sum(scores)
            ))
        return stats

    def get_budgets(self, season_id: int) -> list[BudgetOut]:
        """Crediti residui e rendimento per ogni Player."""
        season  = self.db.query(Season).filter(
                    Season.id == season_id).first()
        if not season:
            return []

        players = self.db.query(Player).filter(
                    Player.is_active == True).all()

        budgets = []
        for player in players:
            spent = self.db.query(func.sum(Auction.cost)).filter(
                Auction.player_id == player.id,
                Auction.season_id == season_id
            ).scalar() or 0

            points     = self._get_player_points(player.id, season_id)
            rendimento = round(spent/points, 2) if points > 0 else None

            budgets.append(BudgetOut(
                nickname=player.user.nickname,
                initial_budget=season.initial_budget,
                credits_spent=spent,
                credits_remaining=season.initial_budget - spent,
                rendimento=rendimento
            ))
        return budgets