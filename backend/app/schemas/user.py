# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    nickname: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    nickname: str | None = None
    email: EmailStr | None = None