# backend/seed.py
from app.core.database import SessionLocal
from app.models.user import User
from app.models.player import Player, Cazzaro
from app.models.season import Season
import hashlib

def seed():
    db = SessionLocal()
    try:
        # Controlla se i dati esistono già
        if db.query(User).count() > 0:
            print("DB già popolato, skip.")
            return

        print("Popolando il database...")

        # Crea i 4 utenti
        amici = [
            {"nickname": "LUCA F", "email": "lucaf@fantacazzate.it"},
            {"nickname": "LUCA R", "email": "lucar@fantacazzate.it"},
            {"nickname": "DAVIDE", "email": "davide@fantacazzate.it"},
            {"nickname": "CICCIO", "email": "ciccio@fantacazzate.it"},
        ]

        users = []
        for amico in amici:
            user = User(
                email=amico["email"],
                nickname=amico["nickname"],
                hashed_password=hashlib.sha256(b"unused").hexdigest(),
                is_active=True
            )
            db.add(user)
            db.flush()

            # Crea Player e Cazzaro per ognuno
            player  = Player(user_id=user.id, is_active=True)
            cazzaro = Cazzaro(
                user_id=user.id,
                nickname=amico["nickname"],
                is_active=True
            )
            db.add(player)
            db.add(cazzaro)
            users.append(user)
            print(f"  ✓ {amico['nickname']} creato")

        # Crea la stagione 2026
        season = Season(
            name="2026",
            initial_budget=500,
            is_active=True
        )
        db.add(season)
        print("  ✓ Stagione 2026 creata")

        db.commit()
        print("\nSeed completato!")

    except Exception as e:
        db.rollback()
        print(f"Errore: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()