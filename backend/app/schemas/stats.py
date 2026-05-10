# backend/app/schemas/stats.py
from pydantic import BaseModel

class StandingOut(BaseModel):
    position: int
    nickname: str
    points: int
    monthly_points: dict[int, int] = {}  # {3: 12, 4: 8} = marzo 12pt, aprile 8pt

class PlayerStatsOut(BaseModel):
    nickname: str
    total_cazzate: int
    confirmed_cazzate: int
    pending_cazzate: int
    avg_score: float | None
    total_points: int

class BudgetOut(BaseModel):
    nickname: str
    initial_budget: int
    credits_spent: int
    credits_remaining: int
    rendimento: float | None