from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.routers import auth, seasons, cazzate, auctions, stats

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

# Configura Swagger per usare Bearer token automaticamente
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.app_name,
        version="0.1.0",
        description="Backend del Fantacazzate 🎯",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth.router)
app.include_router(seasons.router)
app.include_router(cazzate.router)
app.include_router(auctions.router)
app.include_router(stats.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}