# backend/app/schemas/auction.py
from pydantic import BaseModel

class AuctionCreate(BaseModel):
    season_id: int
    player_id: int
    cazzaro_id: int
    month: int
    cost: int

class AuctionUpdate(BaseModel):
    cazzaro_id: int | None = None
    cost: int | None = None

class AuctionOut(BaseModel):
    id: int
    season_id: int
    player_id: int
    player_nickname: str | None = None    # ← aggiunto
    cazzaro_id: int
    cazzaro_nickname: str | None = None   # ← aggiunto
    month: int
    cost: int

    model_config = {"from_attributes": True}