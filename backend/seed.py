# backend/seed.py
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.player import Player, Cazzaro
from app.models.season import Season
from app.core.auth import hash_password

def seed():
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("DB già popolato, skip.")
            return

        print("Popolando il database...")

        amici = [
            {"nickname": "LUCA F", "email": "lucaf@fantacazzate.it", "username": "luca_f"},
            {"nickname": "LUCA R", "email": "lucar@fantacazzate.it", "username": "luca_r"},
            {"nickname": "DAVIDE", "email": "davide@fantacazzate.it", "username": "davide"},
            {"nickname": "CICCIO", "email": "ciccio@fantacazzate.it", "username": "ciccio"},
        ]

        for amico in amici:
            user = User(
                username=amico["username"],
                email=amico["email"],
                nickname=amico["nickname"],
                hashed_password=hash_password("password"),  # password temporanea
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(user)
            db.flush()
            player  = Player(user_id=user.id, is_active=True)
            cazzaro = Cazzaro(
                user_id=user.id,
                nickname=amico["nickname"],
                is_active=True
            )
            db.add(player)
            db.add(cazzaro)
            print(f"  ✓ {amico['nickname']} creato (username: {amico['username']}, password: password)")

        season = Season(name="2026", initial_budget=500, is_active=True)
        db.add(season)
        print("  ✓ Stagione 2026 creata")

        db.commit()
        print("Seed completato!")

    except Exception as e:
        db.rollback()
        print(f"Errore seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()