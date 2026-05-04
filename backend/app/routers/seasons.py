# backend/app/routers/seasons.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_token
from app.services.season_service import SeasonService
from app.schemas.season import SeasonCreate, SeasonOut

router = APIRouter(prefix="/seasons", tags=["seasons"])

@router.post("/", response_model=SeasonOut, status_code=status.HTTP_201_CREATED)
def create_season(
    data: SeasonCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = SeasonService(db)
    return service.create_season(data)

@router.get("/", response_model=list[SeasonOut])
def get_seasons(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = SeasonService(db)
    return service.get_all_seasons()

@router.get("/active", response_model=SeasonOut)
def get_active_season(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = SeasonService(db)
    season = service.get_active_season()
    if not season:
        raise HTTPException(status_code=404, detail="Nessuna stagione attiva")
    return season

@router.get("/{season_id}", response_model=SeasonOut)
def get_season(
    season_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = SeasonService(db)
    season = service.get_season(season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Stagione non trovata")
    return season

@router.patch("/{season_id}/activate", response_model=SeasonOut)
def activate_season(
    season_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = SeasonService(db)
    season = service.set_active(season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Stagione non trovata")
    return season