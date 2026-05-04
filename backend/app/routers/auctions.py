# backend/app/routers/auctions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_token
from app.services.auction_service import AuctionService
from app.schemas.auction import AuctionCreate, AuctionOut

router = APIRouter(prefix="/auctions", tags=["auctions"])

@router.post("/", response_model=AuctionOut, status_code=status.HTTP_201_CREATED)
def create_auction(
    data: AuctionCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = AuctionService(db)
    try:
        return service.create_auction(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{season_id}", response_model=list[AuctionOut])
def get_auctions(
    season_id: int,
    month: int | None = None,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_token)
):
    service = AuctionService(db)
    return service.get_auctions(season_id=season_id, month=month)