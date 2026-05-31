"""
Async SQLAlchemy engine, session factory, and helpers.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a database session.

    Commits on success, rolls back on exception, and always closes.
    """
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def create_all_tables() -> None:
    """Create all tables defined by the SQLAlchemy Base metadata."""
    from models.base import Base  # noqa: avoid circular imports

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
