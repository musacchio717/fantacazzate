# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import cazzate

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend del Fantacazzate 🎯"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Next.js di Davide in locale
        "http://localhost:5173",    # Vite (nel caso)
        "http://localhost:4200",    # Angular (nel caso)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cazzate.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}