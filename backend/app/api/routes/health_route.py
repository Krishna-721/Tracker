from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.postgres import get_db

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check(db: AsyncSession=Depends(get_db)):
    try:
        await db.execute(text("select 1"))
        return {
            "status":"ok", "database":"Connected"
        }
    except Exception:
        return {
            "status":"failed", "database":"disconnected"
        }