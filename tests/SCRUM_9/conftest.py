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


def _build_client_for_path(file_path: str) -> TestClient:
    """Create a test client bound to a specific storage file path."""
    test_store = JsonStore(file_path)
    set_store(test_store)
    client = TestClient(app)
    client.test_store = test_store
    return client


@pytest.fixture
def expense_client() -> TestClient:
    """Provide a TestClient backed by an isolated temp JSON file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as handle:
        handle.write("[]")
        temp_file = handle.name

    client = _build_client_for_path(temp_file)

    try:
        yield client
    finally:
        Path(temp_file).unlink(missing_ok=True)


@pytest.fixture
def expense_client_factory():
    """Create test clients for custom storage-path scenarios."""
    created_paths: list[Path] = []

    def factory(*, initial_content: str | None = "[]", create_file: bool = True) -> TestClient:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as handle:
            temp_file = Path(handle.name)
            if initial_content is not None:
                handle.write(initial_content)

        if not create_file:
            temp_file.unlink(missing_ok=True)

        created_paths.append(temp_file)
        return _build_client_for_path(str(temp_file))

    try:
        yield factory
    finally:
        for path in created_paths:
            path.unlink(missing_ok=True)
