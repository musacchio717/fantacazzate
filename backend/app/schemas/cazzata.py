# backend/app/schemas/cazzata.py
from pydantic import BaseModel
from datetime import date

class CazzataOut(BaseModel):
    id: int
    player: str
    date: date
    month: str
    description: str
    score: int | None  # None se PENDING
    status: str        # "confirmed" o "pending"