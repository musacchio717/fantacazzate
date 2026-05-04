# backend/app/services/cazzata_service.py
from sqlalchemy.orm import Session
from app.models.cazzata import Cazzata, CazzataStatus
from app.schemas.cazzata import CazzataCreate, CazzataConfirm

class CazzataService:
    def __init__(self, db: Session):
        self.db = db

    def create_cazzata(self, data: CazzataCreate) -> Cazzata:
        cazzata = Cazzata(
            **data.model_dump(),
            status=CazzataStatus.PENDING
        )
        self.db.add(cazzata)
        self.db.commit()
        self.db.refresh(cazzata)
        return cazzata

    def get_cazzata(self, cazzata_id: int) -> Cazzata | None:
        return self.db.query(Cazzata).filter(Cazzata.id == cazzata_id).first()

    def get_all(self, season_id: int | None = None,
                cazzaro_id: int | None = None,
                month: int | None = None) -> list[Cazzata]:
        query = self.db.query(Cazzata)
        if season_id:
            query = query.filter(Cazzata.season_id == season_id)
        if cazzaro_id:
            query = query.filter(Cazzata.cazzaro_id == cazzaro_id)
        if month:
            query = query.filter(Cazzata.month == month)
        return query.order_by(Cazzata.date.desc()).all()

    def confirm_cazzata(self, cazzata_id: int,
                        data: CazzataConfirm) -> Cazzata | None:
        cazzata = self.get_cazzata(cazzata_id)
        if not cazzata:
            return None
        if cazzata.status == CazzataStatus.CONFIRMED:
            raise ValueError("Cazzata già confermata")
        cazzata.score  = data.score
        cazzata.status = CazzataStatus.CONFIRMED
        self.db.commit()
        self.db.refresh(cazzata)
        return cazzata

    def delete_cazzata(self, cazzata_id: int) -> bool:
        cazzata = self.get_cazzata(cazzata_id)
        if not cazzata:
            return False
        self.db.delete(cazzata)
        self.db.commit()
        return True