# backend/app/routers/auth.py
from fastapi import APIRouter, HTTPException, status
from app.core.auth import create_access_token
from app.core.config import settings
from app.schemas.auth import LoginRequest, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest):
    if data.password != settings.app_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password errata"
        )
    token = create_access_token({"sub": data.username})
    return TokenOut(access_token=token)