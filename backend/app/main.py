# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, seasons, cazzate, auctions, stats

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend del Fantacazzate 🎯"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(seasons.router)
app.include_router(cazzate.router)
app.include_router(auctions.router)
app.include_router(stats.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}