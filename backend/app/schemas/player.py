# backend/app/schemas/player.py
from pydantic import BaseModel
from app.schemas.user import UserOut

class PlayerOut(BaseModel):
    id: int
    user_id: int
    is_active: bool
    user: UserOut

    model_config = {"from_attributes": True}

class CazzaroCreate(BaseModel):
    user_id: int | None = None   # nullable — cazzari esterni
    nickname: str
    bio: str | None = None

class CazzaroOut(BaseModel):
    id: int
    user_id: int | None
    nickname: str
    bio: str | None
    is_active: bool

    model_config = {"from_attributes": True}