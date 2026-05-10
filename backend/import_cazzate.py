# backend/import_cazzate.py
from app.core.database import SessionLocal
from app.models.cazzata import Cazzata, CazzataStatus
from datetime import date

# Mappa nickname → cazzaro_id
CAZZARI = {
    "LUCA F": 1,
    "LUCA R": 2,
    "DAVIDE": 3,
    "CICCIO": 4,
}

# Mappa mese → numero
MESI = {
    "FEBBRAIO": 2,
    "MARZO": 3,
    "APRILE": 4,
    "MAGGIO": 5,
}

CAZZATE = [
    ("15/02/2026", "FEBBRAIO", "LUCA F",  "Dimentica borraccia, scarpe, mutande ecc...", 1),
    ("17/02/2026", "FEBBRAIO", "LUCA F",  "Dimentica meeting con manager lavoro", 2),
    ("17/02/2026", "FEBBRAIO", "LUCA R",  "Salta uno stop mentre guida, rischia arresto", 4),
    ("17/02/2026", "FEBBRAIO", "LUCA R",  "Va in giro senza documenti, rischia estradizione", 4),
    ("18/02/2026", "FEBBRAIO", "LUCA R",  "Scorda codice lucchetto palestra", 1),
    ("23/02/2026", "FEBBRAIO", "LUCA F",  "Prenota albergo con date sbagliate", 3),
    ("28/02/2026", "FEBBRAIO", "DAVIDE",  "Multa per semaforo rosso", 6),
    ("04/03/2026", "FEBBRAIO", "LUCA R",  "Scorda lezione con bambini", 2),
    ("04/03/2026", "FEBBRAIO", "CICCIO",  "Va in autostrada senza fari accesi", 2),
    ("04/03/2026", "FEBBRAIO", "CICCIO",  "Sbaglia numero scarpe, spedizione scatola ecc...", 5),
    ("05/03/2026", "FEBBRAIO", "LUCA R",  "Guida senza fari", 1),
    ("05/03/2026", "FEBBRAIO", "DAVIDE",  "Fa un lavoro che non deve fare", 1),
    ("10/03/2026", "FEBBRAIO", "DAVIDE",  "Fa cose stupide a lavoro", 1),
    ("14/03/2026", "MARZO",    "LUCA F",  "Paga caffè e non lo beve", 1),
    ("15/03/2026", "MARZO",    "LUCA F",  "Scorda il caricatore", 2),
    ("22/03/2026", "MARZO",    "CICCIO",  "Sbaglia seggio elettorale più volte", 3),
    ("24/03/2026", "MARZO",    "LUCA R",  "Lavora per 5-6 ore inutilmente rovinandosi la vita", 3),
    ("26/03/2026", "MARZO",    "LUCA R",  "Spacca schermo pc", 4),
    ("31/03/2026", "MARZO",    "DAVIDE",  "Spacca bicchiere con cuscino", 2),
    ("08/04/2026", "MARZO",    "DAVIDE",  "Vestiti non lavati per viaggio", 2),
    ("09/04/2026", "MARZO",    "DAVIDE",  "Sporca valigia con liquido svapo", 1),
    ("09/04/2026", "MARZO",    "CICCIO",  "Scorda le chiavi in casa", 2),
    ("09/04/2026", "MARZO",    "CICCIO",  "Butta la pasta a terra", 1),
    ("10/04/2026", "MARZO",    "DAVIDE",  "Si versa merda addosso", 1),
    ("11/04/2026", "MARZO",    "CICCIO",  "Scorda chiavi garage", 1),
    ("11/04/2026", "MARZO",    "LUCA R",  "Perde compiti in classe", 3),
    ("11/04/2026", "MARZO",    "LUCA F",  "Macchia maglietta barbecue", 1),
    ("11/04/2026", "MARZO",    "DAVIDE",  "Non pusha aggiornamenti", 1),
    ("14/04/2026", "APRILE",   "LUCA R",  "Falsifica test arrotondando voti", 3),
    ("20/04/2026", "APRILE",   "CICCIO",  "Perde cappello in treno, si brucia la testa", 4),
    ("21/04/2026", "APRILE",   "CICCIO",  "Non porta le ciabatte su percorso appuntito", 2),
    ("22/04/2026", "APRILE",   "LUCA R",  "Scorda lezione con bambini online", 2),
    ("22/04/2026", "APRILE",   "LUCA R",  "Fa lezioni non pagate online", 4),
    ("23/04/2026", "APRILE",   "CICCIO",  "Scorda luce accesa a casa", 2),
    ("24/04/2026", "APRILE",   "LUCA F",  "Consuma internet a cazzo", 1),
    ("26/04/2026", "APRILE",   "LUCA F",  "Non consuntiva ore a lavoro", 1),
    ("28/04/2026", "APRILE",   "CICCIO",  "Perde occhiali da sole", 4),
    ("01/05/2026", "APRILE",   "CICCIO",  "Scorda luci moto accesa", 3),
    ("07/05/2026", "APRILE",   "LUCA R",  "Mette plastica in friggitrice ad aria", 3),
    ("07/05/2026", "APRILE",   "LUCA R",  "Scorda asciugamano in palestra", 1),
    ("07/05/2026", "APRILE",   "LUCA F",  "Non usa buoni pasto", 1),
    ("08/05/2026", "APRILE",   "LUCA F",  "Fa bordelli con certificato patente", 1),
]

def import_cazzate():
    db = SessionLocal()
    try:
        # Controlla se ci sono già cazzate
        from app.models.cazzata import Cazzata
        existing = db.query(Cazzata).count()
        if existing > 0:
            print(f"Attenzione: ci sono già {existing} cazzate nel DB.")
            risposta = input("Vuoi continuare e aggiungerne altre? (s/n): ")
            if risposta.lower() != 's':
                print("Import annullato.")
                return

        importate = 0
        for data_str, mese, nickname, descrizione, score in CAZZATE:
            giorno, mese_num, anno = data_str.split("/")
            data = date(int(anno), int(mese_num), int(giorno))

            cazzata = Cazzata(
                cazzaro_id=CAZZARI[nickname],
                submitted_by=1,           # importate da Luca F
                season_id=1,
                date=data,
                month=MESI[mese],
                description=descrizione,
                score=score,
                status=CazzataStatus.CONFIRMED
            )
            db.add(cazzata)
            importate += 1
            print(f"  ✓ [{mese}] {nickname}: {descrizione[:45]} (score={score})")

        db.commit()
        print(f"\n✅ Import completato — {importate} cazzate inserite!")

    except Exception as e:
        db.rollback()
        print(f"❌ Errore: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_cazzate()