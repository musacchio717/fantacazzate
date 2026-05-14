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
    score: int

    @field_validator("score")
    @classmethod
    def score_must_be_valid(cls, v):
        if not 1 <= v <= 10:
            raise ValueError("Il punteggio deve essere tra 1 e 10")
        return v

class CazzataOut(BaseModel):
    id: int
    cazzaro_id: int
    cazzaro_nickname: str | None = None      # ← aggiunto
    submitted_by: int | None
    submitted_by_nickname: str | None = None # ← aggiunto
    season_id: int
    date: date
    month: int
    description: str
    score: int | None
    status: CazzataStatus

    model_config = {"from_attributes": True}

class CazzataUpdate(BaseModel):
    description: str | None = None
    score: int | None = None

    @field_validator("score")
    @classmethod
    def score_must_be_valid(cls, v):
        if v is not None and not 1 <= v <= 10:
            raise ValueError("Il punteggio deve essere tra 1 e 10")
        return v