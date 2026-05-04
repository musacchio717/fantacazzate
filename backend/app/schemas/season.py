# backend/app/schemas/season.py
from pydantic import BaseModel
from datetime import date

class SeasonCreate(BaseModel):
    name: str
    initial_budget: int = 500
    start_date: date | None = None
    end_date: date | None = None

class SeasonOut(BaseModel):
    id: int
    name: str
    initial_budget: int
    start_date: date | None
    end_date: date | None
    is_active: bool

    model_config = {"from_attributes": True}