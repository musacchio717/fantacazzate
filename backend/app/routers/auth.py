from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_admin, get_current_user
from app.services.user_service import UserService
from app.schemas.auth import LoginRequest, LoginResponse, UserCreate, UserCreateResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    try:
        result = UserService(db).login(credentials.username, credentials.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/users/create", response_model=UserCreateResponse)
def create_user(
    user_data: UserCreate,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    return UserService(db).create_user(
        nickname=user_data.nickname,
        role=user_data.role
    )

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "role": current_user["role"]
    }