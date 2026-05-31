"""
Repository management router.

Placeholder: endpoints will be implemented in a later phase.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/repos", tags=["repos"])


@router.get("/")
async def list_repos():
    """List repositories available for analysis."""
    return {"detail": "Not implemented yet"}


@router.post("/{repo_id}/analyze")
async def analyze_repo(repo_id: int):
    """Trigger analysis for a specific repository."""
    return {"detail": "Not implemented yet", "repo_id": repo_id}


@router.get("/{repo_id}/status")
async def repo_status(repo_id: int):
    """Check analysis status of a repository."""
    return {"detail": "Not implemented yet", "repo_id": repo_id}
