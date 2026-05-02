# backend/app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.routers import cazzate

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend del Fantacazzate 🎯"
)

app.include_router(cazzate.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}