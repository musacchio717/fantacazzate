# backend/app/schemas/auction.py
from pydantic import BaseModel

class AuctionCreate(BaseModel):
    season_id: int
    player_id: int
    cazzaro_id: int
    month: int     # 1-12
    cost: int

class AuctionOut(BaseModel):
    id: int
    season_id: int
    player_id: int
    cazzaro_id: int
    month: int
    cost: int

    model_config = {"from_attributes": True}