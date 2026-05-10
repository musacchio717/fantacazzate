# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.base import Base
from app.models import User, Player, Cazzaro, Season
import hashlib

# DB in memoria solo per i test — non tocca fantacazzate.db
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

def override_get_db():
    """Sostituisce il DB reale con quello di test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_database():
    """Crea e distrugge le tabelle ad ogni test — DB sempre pulito."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    """Sessione DB per i test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    """TestClient con DB di test iniettato."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    """Esegue il login e restituisce gli header con il token."""
    response = client.post("/auth/login", json={"password": "pesciolinoduro7"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def seed_data(db):
    """Inserisce i dati base — 4 utenti, players, cazzari, stagione."""
    users_data = [
        {"nickname": "LUCA F", "email": "lucaf@test.it"},
        {"nickname": "LUCA R", "email": "lucar@test.it"},
        {"nickname": "DAVIDE", "email": "davide@test.it"},
        {"nickname": "CICCIO", "email": "ciccio@test.it"},
    ]

    users = []
    for data in users_data:
        user = User(
            email=data["email"],
            nickname=data["nickname"],
            hashed_password=hashlib.sha256(b"unused").hexdigest(),
            is_active=True
        )
        db.add(user)
        db.flush()
        player  = Player(user_id=user.id, is_active=True)
        cazzaro = Cazzaro(
            user_id=user.id,
            nickname=data["nickname"],
            is_active=True
        )
        db.add(player)
        db.add(cazzaro)
        users.append(user)

    season = Season(name="2026", initial_budget=500, is_active=True)
    db.add(season)
    db.commit()

    return {"users": users, "season": season}
