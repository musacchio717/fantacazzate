# backend/app/routers/auctions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.auction_service import AuctionService
from app.schemas.auction import AuctionCreate, AuctionUpdate, AuctionOut

router = APIRouter(prefix="/auctions", tags=["auctions"])

@router.post("/", response_model=AuctionOut, status_code=status.HTTP_201_CREATED)
def create_auction(
    data: AuctionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
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
    current_user: dict = Depends(get_current_user)
):
    service = AuctionService(db)
    return service.get_auctions(season_id=season_id, month=month)

@router.patch("/{auction_id}", response_model=AuctionOut)
def update_auction(
    auction_id: int,
    data: AuctionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = AuctionService(db)
    try:
        auction = service.update_auction(auction_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not auction:
        raise HTTPException(status_code=404, detail="Asta non trovata")
    return auction

@router.delete("/{auction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_auction(
    auction_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = AuctionService(db)
    if not service.delete_auction(auction_id):
        raise HTTPException(status_code=404, detail="Asta non trovata")