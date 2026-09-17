import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.postgres import Base, get_db

from app.models.applications import JobApplication 

# ============================================================
# Test Database
# ============================================================

TEST_DATABASE_URL = ("postgresql+asyncpg://postgres:Krishna721""@localhost:5432/job_tracker_test")

# Fresh engine for tests.
# NullPool prevents connections from being reused between tests.
engine_test = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)


# Test session factory
AsyncSessionTest = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ============================================================
# FastAPI Database Override
# ============================================================

async def override_get_db():
    async with AsyncSessionTest() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Override the application's real database dependency
# with the test database.
app.dependency_overrides[get_db] = override_get_db


# ============================================================
# Database Setup / Teardown
# ============================================================

@pytest.fixture(autouse=True)
async def setup_db():
    # Create all tables before each test.
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Remove all tables after each test.
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)