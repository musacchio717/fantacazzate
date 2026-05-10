# backend/app/routers/cazzate.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_token
from app.services.cazzata_service import CazzataService
from app.schemas.cazzata import CazzataCreate, CazzataConfirm, CazzataOut
from app.models.player import Cazzaro, Player
from app.schemas.player import CazzaroOut, PlayerOut

router = APIRouter(prefix="/cazzate", tags=["cazzate"])

@router.post("/", response_model=CazzataOut, status_code=status.HTTP_201_CREATED)
def create_cazzata(
    data: CazzataCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = CazzataService(db)
    return service.create_cazzata(data)

@router.get("/", response_model=list[CazzataOut])
def get_cazzate(
    season_id: int | None = None,
    cazzaro_id: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = CazzataService(db)
    return service.get_all(season_id=season_id,
                           cazzaro_id=cazzaro_id,
                           month=month)

@router.get("/{cazzata_id}", response_model=CazzataOut)
def get_cazzata(
    cazzata_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = CazzataService(db)
    cazzata = service.get_cazzata(cazzata_id)
    if not cazzata:
        raise HTTPException(status_code=404, detail="Cazzata non trovata")
    return cazzata

@router.patch("/{cazzata_id}/confirm", response_model=CazzataOut)
def confirm_cazzata(
    cazzata_id: int,
    data: CazzataConfirm,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = CazzataService(db)
    try:
        cazzata = service.confirm_cazzata(cazzata_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not cazzata:
        raise HTTPException(status_code=404, detail="Cazzata non trovata")
    return cazzata

@router.delete("/{cazzata_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cazzata(
    cazzata_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = CazzataService(db)
    if not service.delete_cazzata(cazzata_id):
        raise HTTPException(status_code=404, detail="Cazzata non trovata")
    
@router.get("/cazzari", response_model=list[CazzaroOut])
def get_cazzari(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """Lista dei cazzari disponibili — per il dropdown nel form."""
    cazzari = db.query(Cazzaro).filter(Cazzaro.is_active == True).all()
    return cazzari

@router.get("/players", response_model=list[PlayerOut])
def get_players(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    """Lista dei players disponibili — per il dropdown nel form."""
    players = db.query(Player).filter(Player.is_active == True).all()
    return players