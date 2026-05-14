"""
Purge + Reimport delle cazzate per la stagione attiva.
(versione con datetime — colonna date ora è TIMESTAMP)

Esegui da `backend/` con .venv attiva:

    cd ~/progetti/fantacazzate/backend
    source .venv/bin/activate
    python purge_and_reimport_cazzate.py

Le cazzate storiche usano orario 12:00:00 come placeholder,
dato che l'ora non era registrata prima.
"""

import os
import sys
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.cazzata import Cazzata, CazzataStatus

# --- CONFIGURAZIONE ---------------------------------------------------------

SEASON_ID = 1
SUBMITTED_BY = 1  # Luca F. Cambia se vuoi un altro player_id.

CAZZARI = {"LUCA F": 1, "LUCA R": 2, "DAVIDE": 3, "CICCIO": 4}
MESI = {"FEBBRAIO": 2, "MARZO": 3, "APRILE": 4, "MAGGIO": 5, "GIUGNO": 6}

# (datetime_iso, mese_gioco, cazzaro, descrizione, punteggio)
# Le cazzate storiche hanno orario 12:00:00 (ora non disponibile).
# Cazzata #38 corretta da 2025-05-01 → 2026-05-01 (typo nel file Excel).
# La PENDING di Luca R 22/04 ora confermata con score=4.
CAZZATE = [
    # --- FEBBRAIO ---
    ("2026-02-15T12:00:00", "FEBBRAIO", "LUCA F", "Dimentica borraccia, scarpe, mutande ecc\u2026", 1),
    ("2026-02-17T12:00:00", "FEBBRAIO", "LUCA F", "Dimentica meeting con manager lavoro", 2),
    ("2026-02-17T12:00:00", "FEBBRAIO", "LUCA R", "Salta uno stop mentre guida, rischia arresto", 1),
    ("2026-02-17T12:00:00", "FEBBRAIO", "LUCA R", "Va in giro senza documenti, rischia estradizione", 4),
    ("2026-02-18T12:00:00", "FEBBRAIO", "LUCA R", "Scorda codice lucchetto palestra", 1),
    ("2026-02-23T12:00:00", "FEBBRAIO", "LUCA F", "Prenota albergo con date sbagliate", 3),
    ("2026-02-28T12:00:00", "FEBBRAIO", "DAVIDE", "Multa per semaforo rosso", 6),
    # febbraio di gioco, data marzo
    ("2026-03-04T12:00:00", "FEBBRAIO", "LUCA R", "Scorda lezione con bambini", 2),
    ("2026-03-04T12:00:00", "FEBBRAIO", "CICCIO", "Va in autostrada senza fari accesi", 2),
    ("2026-03-04T12:00:00", "FEBBRAIO", "CICCIO", "Sbaglia numero scarpe, spedizione scatola ecc\u2026", 5),
    ("2026-03-05T12:00:00", "FEBBRAIO", "LUCA R", "Guida senza fari", 1),
    ("2026-03-05T12:00:00", "FEBBRAIO", "DAVIDE", "Fa un lavoro che non deve fare", 1),
    ("2026-03-10T12:00:00", "FEBBRAIO", "DAVIDE", "Fa cose stupide a lavoro", 1),
    # --- MARZO ---
    ("2026-03-14T12:00:00", "MARZO", "LUCA F", "Paga caff\u00e8 e non lo beve", 1),
    ("2026-03-15T12:00:00", "MARZO", "LUCA F", "Scorda il caricatore", 1),
    ("2026-03-22T12:00:00", "MARZO", "CICCIO", "Sbaglia seggio elettorale pi\u00f9 volte", 2),
    ("2026-03-24T12:00:00", "MARZO", "LUCA R", "Lavora per 5-6 ore inutilmente rovinandosi la vita", 3),
    ("2026-03-26T12:00:00", "MARZO", "LUCA R", "Spacca schermo pc", 4),
    ("2026-03-31T12:00:00", "MARZO", "DAVIDE", "Spacca bicchiere con cuscino", 1),
    # marzo di gioco, data aprile
    ("2026-04-08T12:00:00", "MARZO", "DAVIDE", "Vestiti non lavati per viaggio", 2),
    ("2026-04-09T12:00:00", "MARZO", "DAVIDE", "Sporca valigia con liquido svapo", 1),
    ("2026-04-09T12:00:00", "MARZO", "CICCIO", "Scorda le chiavi in casa", 1),
    ("2026-04-09T12:00:00", "MARZO", "CICCIO", "Butta la pasta a terra", 1),
    ("2026-04-10T12:00:00", "MARZO", "DAVIDE", "Si versa merda addosso", 1),
    ("2026-04-11T12:00:00", "MARZO", "CICCIO", "Scorda chiavi garage", 1),
    ("2026-04-11T12:00:00", "MARZO", "LUCA R", "Perde compiti in classe", 3),
    ("2026-04-11T12:00:00", "MARZO", "LUCA F", "Macchia maglietta barbecue", 1),
    ("2026-04-11T12:00:00", "MARZO", "DAVIDE", "Non pusha aggiornamenti", 1),
    # --- APRILE ---
    ("2026-04-14T12:00:00", "APRILE", "LUCA R", "Falsifica test arrotondando voti", 3),
    ("2026-04-20T12:00:00", "APRILE", "CICCIO", "Perde cappello in treno, si brucia la testa", 4),
    ("2026-04-21T12:00:00", "APRILE", "CICCIO", "Non porta le ciabatte su percorso appuntito", 2),
    ("2026-04-22T12:00:00", "APRILE", "LUCA R", "Scorda lezione con bambini online", 2),
    ("2026-04-22T12:00:00", "APRILE", "LUCA R", "Fa lezioni non pagate online", 4),
    ("2026-04-23T12:00:00", "APRILE", "CICCIO", "Scorda luce accesa a casa", 2),
    ("2026-04-24T12:00:00", "APRILE", "LUCA F", "Consuma internet a cazzo", 1),
    ("2026-04-26T12:00:00", "APRILE", "LUCA F", "Non consuntiva ore a lavoro", 2),
    ("2026-04-28T12:00:00", "APRILE", "CICCIO", "Perde occhiali da sole", 4),
    # aprile di gioco, data maggio (data corretta da 2025 a 2026)
    ("2026-05-01T12:00:00", "APRILE", "CICCIO", "Scorda luci moto accesa", 3),
    ("2026-05-07T12:00:00", "APRILE", "LUCA R", "Mette plastica in friggitrice ad aria", 3),
    ("2026-05-07T12:00:00", "APRILE", "LUCA R", "Scorda asciugamano in palestra", 1),
    ("2026-05-07T12:00:00", "APRILE", "LUCA F", "Non usa buoni pasto", 1),
    ("2026-05-08T12:00:00", "APRILE", "LUCA F", "Fa bordelli con certificato patente", 3),
]


# --- SANITY CHECK -----------------------------------------------------------

def sanity_check() -> None:
    expected = {
        ("LUCA R", 2): (5, 9),  ("LUCA F", 2): (3, 6),
        ("DAVIDE", 2): (3, 8),  ("CICCIO", 2): (2, 7),
        ("LUCA R", 3): (3, 10), ("LUCA F", 3): (3, 3),
        ("DAVIDE", 3): (5, 6),  ("CICCIO", 3): (4, 5),
        ("LUCA R", 4): (5, 13), ("LUCA F", 4): (4, 7),
        ("DAVIDE", 4): (0, 0),  ("CICCIO", 4): (5, 15),
    }
    counts: dict = {}
    for _, mese_str, cazzaro, _, score in CAZZATE:
        key = (cazzaro, MESI[mese_str])
        n, s = counts.get(key, (0, 0))
        counts[key] = (n + 1, s + score)

    errors = []
    for key, exp in expected.items():
        got = counts.get(key, (0, 0))
        if got != exp:
            errors.append(f"  {key}: atteso {exp}, trovato {got}")
    if errors:
        print("\u274c SANITY CHECK FAILED:")
        for e in errors:
            print(e)
        sys.exit(1)
    print(f"\u2713 Sanity check OK \u2014 {len(CAZZATE)} cazzate, 89 punti totali")


# --- MAIN -------------------------------------------------------------------

def main() -> None:
    sanity_check()

    db = SessionLocal()
    try:
        existing = db.query(Cazzata).filter(Cazzata.season_id == SEASON_ID).all()
        print(f"\nDB attuale: {len(existing)} cazzate per stagione {SEASON_ID}")
        if existing:
            for c in existing[:3]:
                print(f"  id={c.id} cazzaro={c.cazzaro_id} date={c.date} '{c.description[:50]}'")

        confirm = input(
            f"\n\u26a0  Eliminer\u00f2 TUTTE le {len(existing)} cazzate della stagione {SEASON_ID} "
            f"e ne inserir\u00f2 {len(CAZZATE)} nuove.\nDigita 'yes' per procedere: "
        )
        if confirm.strip().lower() != "yes":
            print("Annullato.")
            return

        deleted = db.query(Cazzata).filter(Cazzata.season_id == SEASON_ID).delete()
        db.commit()
        print(f"\u2713 Eliminate {deleted} cazzate")

        for dt_iso, mese_str, cazzaro_name, desc, score in CAZZATE:
            db.add(Cazzata(
                cazzaro_id=CAZZARI[cazzaro_name],
                submitted_by=SUBMITTED_BY,
                season_id=SEASON_ID,
                date=datetime.fromisoformat(dt_iso),
                month=MESI[mese_str],
                description=desc,
                score=score,
                status=CazzataStatus.CONFIRMED,
            ))
        db.commit()
        print(f"\u2713 Inserite {len(CAZZATE)} cazzate")

        final_count = db.query(Cazzata).filter(Cazzata.season_id == SEASON_ID).count()
        print(f"\nDB finale: {final_count} cazzate")

        from sqlalchemy import func
        rows = (
            db.query(Cazzata.cazzaro_id, Cazzata.month,
                     func.count(Cazzata.id), func.sum(Cazzata.score))
            .filter(Cazzata.season_id == SEASON_ID)
            .group_by(Cazzata.cazzaro_id, Cazzata.month)
            .order_by(Cazzata.month, Cazzata.cazzaro_id)
            .all()
        )
        id_to_name = {v: k for k, v in CAZZARI.items()}
        mese_to_name = {v: k for k, v in MESI.items()}
        for cazzaro_id, month, n, tot in rows:
            print(f"  {mese_to_name[month]:10} {id_to_name[cazzaro_id]:8} \u2192 {n} cazzate, {tot} punti")

    except Exception as e:
        db.rollback()
        print(f"\n\u274c ERRORE: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
