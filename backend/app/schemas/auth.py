from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: str

class UserCreate(BaseModel):
    nickname: str
    role: str  # "admin" o "observer"

class UserCreateResponse(BaseModel):
    user_id: int
    username: str
    password: str  # password temporanea (solo nella risposta di creazione)
    nickname: str
    role: str

class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True