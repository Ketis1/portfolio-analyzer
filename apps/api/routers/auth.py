"""
Authentication router — GitHub OAuth + JWT flow.

Placeholder: endpoints will be implemented in a later phase.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login():
    """Redirect to GitHub OAuth authorization page."""
    return {"detail": "Not implemented yet"}


@router.get("/callback")
async def callback():
    """Handle GitHub OAuth callback, issue JWT."""
    return {"detail": "Not implemented yet"}


@router.get("/me")
async def me():
    """Return the current authenticated user."""
    return {"detail": "Not implemented yet"}
