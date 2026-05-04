# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_token
from app.services.users_service import UserService
from app.schemas.users import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = UserService(db)
    try:
        return service.create_user(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserOut])
def get_users(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = UserService(db)
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = UserService(db)
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user

@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = UserService(db)
    user = service.update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user