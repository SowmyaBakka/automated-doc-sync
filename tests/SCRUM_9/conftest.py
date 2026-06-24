"""Shared fixtures for SCRUM-9 API tests."""

import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.SCRUM_9.main import app
from src.SCRUM_9.routes.expenses import set_store
from src.SCRUM_9.store.json_store import JsonStore


@pytest.fixture
def expense_client() -> TestClient:
    """Provide a TestClient backed by an isolated temp JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as handle:
        handle.write("[]")
        temp_file = handle.name

    test_store = JsonStore(temp_file)
    set_store(test_store)
    client = TestClient(app)
    client.test_store = test_store

    try:
        yield client
    finally:
        Path(temp_file).unlink(missing_ok=True)
