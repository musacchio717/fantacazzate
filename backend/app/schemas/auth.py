# backend/app/schemas/auth.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str   # nome di chi accede, solo per tracciare
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"