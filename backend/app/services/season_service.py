# backend/app/services/season_service.py
from sqlalchemy.orm import Session
from app.models.season import Season
from app.schemas.season import SeasonCreate

class SeasonService:
    def __init__(self, db: Session):
        self.db = db

    def create_season(self, data: SeasonCreate) -> Season:
        season = Season(**data.model_dump())
        self.db.add(season)
        self.db.commit()
        self.db.refresh(season)
        return season

    def get_season(self, season_id: int) -> Season | None:
        return self.db.query(Season).filter(Season.id == season_id).first()

    def get_active_season(self) -> Season | None:
        return self.db.query(Season).filter(Season.is_active == True).first()

    def get_all_seasons(self) -> list[Season]:
        return self.db.query(Season).all()

    def set_active(self, season_id: int) -> Season | None:
        # Disattiva tutte le stagioni
        self.db.query(Season).update({"is_active": False})
        # Attiva quella richiesta
        season = self.get_season(season_id)
        if not season:
            return None
        season.is_active = True
        self.db.commit()
        self.db.refresh(season)
        return season