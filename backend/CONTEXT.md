# FANTACAZZATE — CONTESTO PROGETTO

## Cos'è
Fantasy game tra 4 amici (LUCA F, LUCA R, DAVIDE, CICCIO) basato su cazzate reali. Ogni mese si fa un'asta per comprare i "cazzari" (gli amici che fanno cazzate). Chi fa più cazzate genera più punti. Vince chi accumula più punti nella stagione.

## Stack
- **Backend**: Python 3.12 + FastAPI + SQLAlchemy + Alembic
- **DB Produzione**: PostgreSQL su Railway
- **DB Locale**: SQLite (`fantacazzate.db`)
- **Deploy**: Railway (backend), Vercel (frontend Davide)
- **Auth**: JWT con username + password individuali
- **Repo**: github.com/musacchio717/fantacazzate

## URL Produzione
- **Backend**: https://fantacazzate-production-bb3a.up.railway.app
- **Swagger**: https://fantacazzate-production-bb3a.up.railway.app/docs
- **DB Railway**: turntable.proxy.rlwy.net:10738

## Credenziali DB Railway
```
DATABASE_URL=postgresql://postgres:ERNVDcvMqXzYKFImBohgOLCJfnALLzQH@turntable.proxy.rlwy.net:10738/railway
```

## Credenziali Utenti (Produzione)
| Nickname | Username | Password | Ruolo |
|----------|----------|----------|-------|
| LUCA F | luca_f | QxwMx | admin |
| LUCA R | luca_r | IWqDd | admin |
| DAVIDE | davide | TI5Iq | admin |
| CICCIO | ciccio | RSJlU | admin |

> Observer di test: username=gay, da ricreare via endpoint se serve

## IDs nel DB
- LUCA F: user_id=1, player_id=1, cazzaro_id=1
- LUCA R: user_id=2, player_id=2, cazzaro_id=2
- DAVIDE: user_id=3, player_id=3, cazzaro_id=3
- CICCIO: user_id=4, player_id=4, cazzaro_id=4
- Stagione attiva: id=1, budget iniziale=500

## Struttura Progetto
```
fantacazzate/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── auth.py          ← JWT, hash_password, verify_password, require_admin, get_current_user
│   │   │   ├── database.py      ← SessionLocal, get_db
│   │   │   └── config.py
│   │   ├── models/
│   │   │   ├── user.py          ← User (username, nickname, hashed_password, role, is_active)
│   │   │   ├── player.py        ← Player, Cazzaro
│   │   │   ├── cazzata.py       ← Cazzata (DateTime per date)
│   │   │   ├── auction.py       ← Auction
│   │   │   └── season.py        ← Season
│   │   ├── routers/
│   │   │   ├── auth.py          ← POST /auth/login, POST /auth/users/create, GET /auth/me
│   │   │   ├── cazzate.py       ← CRUD cazzate
│   │   │   ├── auctions.py      ← CRUD aste
│   │   │   ├── seasons.py       ← CRUD stagioni
│   │   │   └── stats.py         ← GET standings, players, budgets
│   │   ├── schemas/
│   │   │   ├── auth.py          ← LoginRequest, LoginResponse, UserCreate, UserCreateResponse
│   │   │   ├── cazzata.py       ← CazzataCreate, CazzataOut (date: datetime)
│   │   │   ├── stats.py         ← StandingOut, PlayerStatsOut, BudgetOut
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── user_service.py  ← login(), create_user(), _generate_password()
│   │   │   ├── cazzata_service.py
│   │   │   ├── auction_service.py
│   │   │   ├── season_service.py
│   │   │   └── stats_service.py
│   │   └── main.py
│   ├── alembic/
│   │   └── versions/
│   │       ├── 102c6d5855e9_initial_schema.py
│   │       ├── a1b2c3d4e5f6_cazzata_date_to_datetime.py
│   │       └── a1b2c3d4e5f7_add_user_role.py
│   ├── requirements.txt
│   ├── seed.py
│   ├── migrate_users_to_auth.py
│   ├── set_credentials.py
│   └── create_local_db.py
└── frontend/                    ← gestito da Davide (Vercel)
```

## Ruoli e Permessi
| Endpoint | ADMIN | OBSERVER |
|----------|-------|----------|
| GET (tutti) | ✅ | ✅ |
| POST /cazzate/ | ✅ | ❌ |
| PATCH /cazzate/{id} | ✅ | ❌ |
| DELETE /cazzate/{id} | ✅ | ❌ |
| POST /auctions/ | ✅ | ❌ |
| PATCH /auctions/{id} | ✅ | ❌ |
| DELETE /auctions/{id} | ✅ | ❌ |
| POST /seasons/ | ✅ | ❌ |
| POST /auth/users/create | ✅ | ❌ |

## Endpoint Principali
```
POST   /auth/login                  → login (no auth richiesta)
POST   /auth/users/create           → crea utente (solo admin)
GET    /auth/me                     → info utente corrente

GET    /cazzate/                    → lista cazzate (filtri: season_id, cazzaro_id, month)
POST   /cazzate/                    → crea cazzata (admin)
PATCH  /cazzate/{id}               → modifica cazzata (admin)
DELETE /cazzate/{id}               → elimina cazzata (admin)
GET    /cazzate/meta/cazzari       → lista cazzari
GET    /cazzate/meta/players       → lista players

GET    /auctions/{season_id}       → lista aste per stagione
POST   /auctions/                  → crea asta (admin)
PATCH  /auctions/{id}              → modifica asta (admin)
DELETE /auctions/{id}              → elimina asta (admin)

GET    /stats/{season_id}/standings → classifica
GET    /stats/{season_id}/players   → stats cazzari (total_cazzate, avg_score, total_points, rendimento)
GET    /stats/{season_id}/budgets   → budget allenatori (credits_spent, credits_remaining, max_spendable, rendimento)

GET    /seasons/
GET    /seasons/active
GET    /seasons/{id}
POST   /seasons/                   → crea stagione (admin)
PATCH  /seasons/{id}/activate      → attiva stagione (admin)
```

## Schema Stats
```json
// GET /stats/{season_id}/players
{
  "nickname": "LUCA F",
  "total_cazzate": 11,
  "avg_score": 1.64,
  "total_points": 18,
  "rendimento": 24.46   // costo_asta / punti generati (media mensile)
}

// GET /stats/{season_id}/budgets
{
  "nickname": "LUCA F",
  "initial_budget": 500,
  "credits_spent": 219,
  "credits_remaining": 281,
  "max_spendable": 231,   // credits_remaining - 50 (riserva minima per aste)
  "rendimento": 7.55      // crediti_spesi / punti_ricevuti
}
```

## Logica di Business
- **Mese di gioco**: le cazzate di febbraio sono il mese 2, marzo=3, aprile=4, maggio=5
- **Rendimento cazzaro**: per ogni mese in cui è stato comprato, calcola costo_asta/punti_quel_mese, poi fa la media dei mesi non-zero
- **Rendimento allenatore**: crediti_spesi_totali / punti_ricevuti_totali
- **max_spendable**: credits_remaining - 50 (devi mantenere minimo 50 crediti)
- **date cazzate**: DateTime (non Date), formato ISO 8601 es. "2026-05-14T13:32:00+02:00"

## Stagione 2026 — Dati Storici
- Mesi: Febbraio (2), Marzo (3), Aprile (4), Maggio (5 — in corso)
- Budget iniziale: 500 crediti a testa

### Aste storiche (costo pagato per cazzaro per mese)
| Mese | LUCA F paga | LUCA R paga | DAVIDE paga | CICCIO paga |
|------|-------------|-------------|-------------|-------------|
| FEB  | 117 (LUCA R)| 50 (LUCA F) | 50 (CICCIO) | 105 (DAVIDE)|
| MAR  | 97 (DAVIDE) | 50 (LUCA F) | 125 (LUCA R)| 110 (CICCIO)|
| APR  | 110 (CICCIO)| 119 (DAVIDE)| 152 (LUCA R)| 50 (LUCA F) |

### Classifica al 14/05/2026
| Pos | Nickname | Punti |
|-----|----------|-------|
| 1 | LUCA F | 29 |
| 2 | DAVIDE | 23 |
| 3 | CICCIO | 19 |
| 4 | LUCA R | 18 |

### Crediti residui
| Nickname | Residuo |
|----------|---------|
| LUCA F | 281 |
| LUCA R | 176 |
| DAVIDE | 173 |
| CICCIO | 235 |

## Frontend (Davide)
Il frontend è gestito da Davide su Vercel. Le modifiche al sistema di auth richiedono aggiornamenti al frontend:

### Cambio Login
```javascript
// PRIMA (password condivisa)
POST /login
{ "password": "pesciolinoduro7" }

// ORA (credenziali individuali)
POST /auth/login
{ "username": "davide", "password": "TI5Iq" }

// Risposta
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "username": "davide",
  "role": "admin"
}
```

### Gestione token
```javascript
localStorage.setItem("token", response.access_token)
localStorage.setItem("role", response.role)
localStorage.setItem("username", response.username)

// Header per ogni chiamata
headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
```

### Gestione ruoli
```javascript
const role = localStorage.getItem("role")
if (role === "admin") { /* mostra bottoni modifica/elimina */ }
if (response.status === 403) { alert("Non hai i permessi") }
```

## Comandi Utili

### Locale
```bash
# Avvia server locale
cd backend && uvicorn app.main:app --reload

# Ricrea DB locale da zero
export DATABASE_URL="sqlite:///./fantacazzate.db"
python create_local_db.py && python seed.py

# SSH su Railway
export PATH="$HOME/.railway/bin:$PATH"
railway login
railway ssh --project=284ee2eb-5081-4557-950b-6ad2b87b93f1 --environment=0bcf7316-d5bc-45c4-9aba-2b7d9332a546 --service=8554fc05-4dad-494e-a3ab-9bb2759eff4d

# Punta al DB Railway da locale
export DATABASE_URL="postgresql://postgres:ERNVDcvMqXzYKFImBohgOLCJfnALLzQH@turntable.proxy.rlwy.net:10738/railway"
```

### Git Workflow
```bash
# Nuovo branch per feature
git checkout main && git pull origin main
git checkout -b feat/nome-feature

# Push e merge
git add . && git commit -m "feat: descrizione"
git push origin feat/nome-feature
# → apri PR su GitHub → mergia → Railway deploya automaticamente

# Se hai commesso su main per sbaglio
git push origin main
```

## TODO / Prossimi Step
- [ ] Aste maggio 2026 (da inserire via frontend)
- [ ] Endpoint PATCH /auth/change-password (per cambiare password dal frontend)
- [ ] Comunicare a Davide le modifiche al frontend per il nuovo sistema di auth
- [ ] Aste giugno 2026 (future)

## Note Tecniche Importanti
- **bcrypt warning**: "(trapped) error reading bcrypt version" è solo un warning innocuo, non un errore
- **Alembic su SQLite**: il comando `ALTER COLUMN` non funziona su SQLite → usare `create_local_db.py` invece di `alembic upgrade head` in locale
- **Timezone**: il backend salva datetime in UTC. Le 13:32 italiane (CEST=UTC+2) = 11:32 UTC nel DB
- **Migrazioni utenti su Railway**: vanno eseguite tramite SSH nel container Railway, non in locale (versioni bcrypt diverse)
- **max_spendable**: `max(0, credits_remaining - 50)` — non può essere negativo
