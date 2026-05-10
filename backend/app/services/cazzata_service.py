# backend/app/services/cazzata_service.py
from sqlalchemy.orm import Session
from app.models.cazzata import Cazzata, CazzataStatus
from app.schemas.cazzata import CazzataCreate
from app.core.logger import logger

class CazzataService:
    def __init__(self, db: Session):
        self.db = db

    def create_cazzata(self, data: CazzataCreate) -> Cazzata:
        cazzata = Cazzata(
            cazzaro_id=data.cazzaro_id,
            submitted_by=data.submitted_by,
            season_id=data.season_id,
            date=data.date,
            month=data.month,
            description=data.description,
            score=data.score,
            status=CazzataStatus.CONFIRMED
        )
        self.db.add(cazzata)
        self.db.commit()
        self.db.refresh(cazzata)

        logger.info(
            f"CAZZATA CREATA | id={cazzata.id} | "
            f"cazzaro_id={cazzata.cazzaro_id} | "
            f"score={cazzata.score} | "
            f"mese={cazzata.month} | "
            f"descrizione='{cazzata.description[:50]}'"
        )
        return cazzata

    def get_cazzata(self, cazzata_id: int) -> Cazzata | None:
        return self.db.query(Cazzata).filter(
                    Cazzata.id == cazzata_id).first()

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

    def update_cazzata(self, cazzata_id: int,
                       description: str | None = None,
                       score: int | None = None) -> Cazzata | None:
        cazzata = self.get_cazzata(cazzata_id)
        if not cazzata:
            return None

        vecchio_score = cazzata.score
        vecchia_desc  = cazzata.description

        if description:
            cazzata.description = description
        if score:
            cazzata.score = score

        self.db.commit()
        self.db.refresh(cazzata)

        logger.info(
            f"CAZZATA MODIFICATA | id={cazzata.id} | "
            f"cazzaro_id={cazzata.cazzaro_id} | "
            f"score: {vecchio_score} → {cazzata.score} | "
            f"descrizione: '{vecchia_desc[:30]}' → '{cazzata.description[:30]}'"
        )
        return cazzata

    def delete_cazzata(self, cazzata_id: int) -> bool:
        cazzata = self.get_cazzata(cazzata_id)
        if not cazzata:
            return False

        logger.info(
            f"CAZZATA ELIMINATA | id={cazzata.id} | "
            f"cazzaro_id={cazzata.cazzaro_id} | "
            f"score={cazzata.score} | "
            f"mese={cazzata.month} | "
            f"descrizione='{cazzata.description[:50]}'"
        )

        self.db.delete(cazzata)
        self.db.commit()
        return True