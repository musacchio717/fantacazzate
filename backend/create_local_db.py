"""
Crea il DB locale SQLite direttamente dai modelli SQLAlchemy.
Bypassa Alembic (che ha problemi con SQLite e ALTER COLUMN).
Usare SOLO in locale, mai in produzione.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ["DATABASE_URL"] = "sqlite:///./fantacazzate.db"

from sqlalchemy import create_engine
from app.models.base import Base

# Importa tutti i modelli per registrarli in Base.metadata
from app.models.user import User
from app.models.player import Player, Cazzaro
from app.models.cazzata import Cazzata
from app.models.auction import Auction
from app.models.season import Season

engine = create_engine("sqlite:///./fantacazzate.db")

print("Creazione tabelle...")
Base.metadata.drop_all(engine)   # pulisce tutto
Base.metadata.create_all(engine)  # ricrea da zero con tutti i modelli aggiornati
print("✓ Tabelle create!")