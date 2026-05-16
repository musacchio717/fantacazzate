# backend/app/routers/cazzate.py
from app.schemas.cazzata import CazzataCreate, CazzataUpdate, CazzataOut
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user, require_admin
from app.services.cazzata_service import CazzataService
from app.models.player import Cazzaro, Player
from app.schemas.player import CazzaroOut, PlayerOut

router = APIRouter(prefix="/cazzate", tags=["cazzate"])

@router.post("/", response_model=CazzataOut, status_code=status.HTTP_201_CREATED)
def create_cazzata(
    data: CazzataCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)   # solo admin
):
    service = CazzataService(db)
    return service.create_cazzata(data)

@router.get("/", response_model=list[CazzataOut])
def get_cazzate(
    season_id: int | None = None,
    cazzaro_id: int | None = None,
    month: int | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # admin e observer
):
    service = CazzataService(db)
    return service.get_all(season_id=season_id,
                           cazzaro_id=cazzaro_id,
                           month=month)

@router.get("/meta/cazzari", response_model=list[CazzaroOut])
def get_cazzari(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # admin e observer
):
    """Lista cazzari per il dropdown nel form."""
    return db.query(Cazzaro).filter(Cazzaro.is_active == True).all()

@router.get("/meta/players", response_model=list[PlayerOut])
def get_players(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # admin e observer
):
    """Lista players per il dropdown nel form."""
    return db.query(Player).filter(Player.is_active == True).all()

@router.get("/{cazzata_id}", response_model=CazzataOut)
def get_cazzata(
    cazzata_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # admin e observer
):
    service = CazzataService(db)
    cazzata = service.get_cazzata(cazzata_id)
    if not cazzata:
        raise HTTPException(status_code=404, detail="Cazzata non trovata")
    return cazzata

@router.patch("/{cazzata_id}", response_model=CazzataOut)
def update_cazzata(
    cazzata_id: int,
    data: CazzataUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)   # solo admin
):
    """Modifica descrizione o punteggio di una cazzata esistente."""
    service = CazzataService(db)
    cazzata = service.update_cazzata(cazzata_id, data.description, data.score)
    if not cazzata:
        raise HTTPException(status_code=404, detail="Cazzata non trovata")
    return cazzata

@router.delete("/{cazzata_id}")
def delete_cazzata(
    cazzata_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)   # solo admin
):
    service = CazzataService(db)
    cazzata = service.get_cazzata(cazzata_id)
    if not cazzata:
        raise HTTPException(status_code=404, detail="Cazzata non trovata")

    dettagli = {
        "message": "Cazzata eliminata con successo",
        "id": cazzata.id,
        "cazzaro_id": cazzata.cazzaro_id,
        "description": cazzata.description,
        "score": cazzata.score,
        "month": cazzata.month
    }

    service.delete_cazzata(cazzata_id)
    return dettagli