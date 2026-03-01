from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.postgres import init_db

from app.models import applications
from backend.app.api.routes.health_route import router as health_router

from app.api.routes.applications_route import router as application_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"=======🚀 Starting {settings.APP_NAME}...======")
    await init_db()
    yield
    print("=======👋 Shutting down...========")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(application_router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
    }
