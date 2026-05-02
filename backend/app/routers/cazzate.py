# backend/app/routers/cazzate.py
from fastapi import APIRouter
from app.schemas.cazzata import CazzataOut
from datetime import date

router = APIRouter(prefix="/cazzate", tags=["cazzate"])

MOCK_CAZZATE = [
    {
        "id": 1,
        "player": "LUCA F",
        "date": date(2026, 2, 15),
        "month": "FEBBRAIO",
        "description": "Dimentica borraccia, scarpe, mutande ecc...",
        "score": 1,
        "status": "confirmed"
    },
    {
        "id": 2,
        "player": "DAVIDE",
        "date": date(2026, 2, 28),
        "month": "FEBBRAIO",
        "description": "Multa per semaforo rosso",
        "score": 6,
        "status": "confirmed"
    },
    {
        "id": 3,
        "player": "LUCA R",
        "date": date(2026, 4, 22),
        "month": "APRILE",
        "description": "Fa lezioni non pagate online",
        "score": None,
        "status": "pending"
    },
]

@router.get("/", response_model=list[CazzataOut])
def get_cazzate():
    return MOCK_CAZZATE