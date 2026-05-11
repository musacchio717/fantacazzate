# backend/import_auctions.py
from app.core.database import SessionLocal
from app.models.auction import Auction
from app.models.player import Player, Cazzaro
from app.models.user import User

# Mappa nickname → player_id e cazzaro_id
# Assumendo che gli ID siano: LUCA F=1, LUCA R=2, DAVIDE=3, CICCIO=4

def get_ids(db):
    players = {}
    cazzari = {}
    users = db.query(User).all()
    for u in users:
        player  = db.query(Player).filter(Player.user_id == u.id).first()
        cazzaro = db.query(Cazzaro).filter(Cazzaro.user_id == u.id).first()
        if player:
            players[u.nickname] = player.id
        if cazzaro:
            cazzari[u.nickname] = cazzaro.id
    return players, cazzari

ASTE = [
    # (mese, acquirente, giocatore_acquistato, costo)
    # FEBBRAIO
    (2, "LUCA R",  "LUCA F",  117),
    (2, "LUCA F",  "DAVIDE",   50),
    (2, "DAVIDE",  "CICCIO",   50),
    (2, "CICCIO",  "LUCA R",  105),
    # MARZO
    (3, "LUCA R",  "CICCIO",   97),
    (3, "LUCA F",  "DAVIDE",   50),
    (3, "DAVIDE",  "LUCA F",  125),
    (3, "CICCIO",  "LUCA R",  110),
    # APRILE
    (4, "LUCA R",  "LUCA F",  110),
    (4, "LUCA F",  "CICCIO",  119),
    (4, "DAVIDE",  "LUCA R",  152),
    (4, "CICCIO",  "DAVIDE",   50),
]

def import_auctions():
    db = SessionLocal()
    try:
        existing = db.query(Auction).count()
        if existing > 0:
            print(f"Ci sono già {existing} aste nel DB, skip.")
            return

        players, cazzari = get_ids(db)
        print("Players trovati:", players)
        print("Cazzari trovati:", cazzari)

        importate = 0
        for mese, acquirente, acquistato, costo in ASTE:
            auction = Auction(
                season_id  = 1,
                player_id  = players[acquirente],
                cazzaro_id = cazzari[acquistato],
                month      = mese,
                cost       = costo
            )
            db.add(auction)
            importate += 1
            mese_nome = {2: "FEBBRAIO", 3: "MARZO", 4: "APRILE"}[mese]
            print(f"  ✓ [{mese_nome}] {acquirente} compra {acquistato} per {costo} crediti")

        db.commit()
        print(f"\n✅ Import completato — {importate} aste inserite!")

    except Exception as e:
        db.rollback()
        print(f"❌ Errore: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_auctions()