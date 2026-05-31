"""
Portfolio Analyzer API — FastAPI entry point.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy import text

from config import get_settings
from database import AsyncSessionLocal
from middleware.cors import add_cors_middleware
from routers.auth import router as auth_router
from routers.repos import router as repos_router

logger = logging.getLogger("portfolio_api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: runs on startup and shutdown."""
    logger.info(
        "🚀 Portfolio Analyzer API is running — docs at http://localhost:8000/docs"
    )
    yield
    logger.info("Portfolio Analyzer API shutting down")


app = FastAPI(
    title="Portfolio Analyzer API",
    description="Analyze GitHub repositories and generate professional CV/portfolio reports.",
    version="0.1.0",
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────────────────
add_cors_middleware(app)

# ── Routers ──────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(repos_router)


# ── Health Check ─────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health_check():
    """Health endpoint that verifies the database connection is alive."""
    db_status = "ok"
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except Exception as exc:
        logger.error("Health check DB probe failed: %s", exc)
        db_status = "error"

    return {"status": "ok" if db_status == "ok" else "degraded", "db": db_status}
