from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.postgres import init_db
from app.models import applications  # ← this line — forces model to register with Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting {settings.APP_NAME}...")
    await init_db()
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
    }
