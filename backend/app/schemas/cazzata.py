# backend/app/schemas/cazzata.py
from pydantic import BaseModel, field_validator
from datetime import date
from app.models.cazzata import CazzataStatus

class CazzataCreate(BaseModel):
    cazzaro_id: int
    submitted_by: int
    season_id: int
    date: date
    month: int
    description: str
    score: int                    # obbligatorio subito

    @field_validator("score")
    @classmethod
    def score_must_be_valid(cls, v):
        if not 1 <= v <= 10:
            raise ValueError("Il punteggio deve essere tra 1 e 10")
        return v

# backend/app/schemas/cazzata.py

class CazzataOut(BaseModel):
    id: int
    cazzaro_id: int
    submitted_by: int | None
    season_id: int
    date: date
    month: int
    description: str
    score: int | None    # nullable — per compatibilità con dati vecchi
    status: CazzataStatus

    model_config = {"from_attributes": True}