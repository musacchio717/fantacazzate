# backend/app/schemas/auth.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"