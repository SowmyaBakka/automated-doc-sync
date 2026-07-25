"""Shared fixtures for SCRUM-10 tests."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.SCRUM_10.main import app
from src.SCRUM_10.routes.auth import reset_auth_state


@pytest.fixture(autouse=True)
def reset_state() -> None:
    """Reset in-memory auth state before each SCRUM-10 test."""
    reset_auth_state()


@pytest.fixture
def auth_client() -> TestClient:
    """Provide a FastAPI client bound to SCRUM-10 app."""
    return TestClient(app)
