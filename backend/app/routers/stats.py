# backend/app/routers/stats.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.stats_service import StatsService
from app.schemas.stats import StandingOut, PlayerStatsOut, BudgetOut

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/{season_id}/standings", response_model=list[StandingOut])
def get_standings(
    season_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # admin e observer
):
    service = StatsService(db)
    return service.get_standings(season_id)

@router.get("/{season_id}/players", response_model=list[PlayerStatsOut])
def get_player_stats(
    season_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # admin e observer
):
    service = StatsService(db)
    return service.get_player_stats(season_id)

@router.get("/{season_id}/budgets", response_model=list[BudgetOut])
def get_budgets(
    season_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # admin e observer
):
    service = StatsService(db)
    return service.get_budgets(season_id)