"""Integration tests for the POST /todos endpoint."""

import pytest
from fastapi.testclient import TestClient
import tempfile
from pathlib import Path

from src.SCRUM_8.main import app, store


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app with initialized store."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
        f.write('[]')
    
    # Recreate store with temp file
    test_store = store.__class__(temp_file)
    
    # Setup: initialize
    import asyncio
    asyncio.run(test_store.load())
    
    # Inject into router
    from src.SCRUM_8.routes.todos import set_store
    set_store(test_store)
    
    client = TestClient(app)
    
    yield client
    
    # Cleanup
    Path(temp_file).unlink(missing_ok=True)


def test_post_todos_valid_body_returns_201(client):
    """Test POST /todos with valid body returns 201 + full TodoItem."""
    response = client.post(
        "/todos",
        json={"title": "Buy groceries", "description": "Milk and eggs"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk and eggs"
    assert data["done"] is False
    assert "createdAt" in data


def test_post_todos_missing_title_returns_400(client):
    """Test POST /todos without title returns 400 with error detail."""
    response = client.post(
        "/todos",
        json={"description": "Some description"}
    )
    
    assert response.status_code == 422  # Pydantic validation error
    data = response.json()
    assert "detail" in data


def test_post_todos_empty_title_returns_400(client):
    """Test POST /todos with empty title returns 400."""
    response = client.post(
        "/todos",
        json={"title": "", "description": "Something"}
    )
    
    assert response.status_code == 422  # Pydantic validation error
    data = response.json()
    assert "detail" in data


def test_post_todos_whitespace_only_title_returns_400(client):
    """Test POST /todos with whitespace-only title returns 400."""
    response = client.post(
        "/todos",
        json={"title": "   ", "description": "Something"}
    )
    
    assert response.status_code == 422  # Pydantic validation error
    data = response.json()
    assert "detail" in data


def test_post_todos_description_optional(client):
    """Test POST /todos works without description (optional field)."""
    response = client.post(
        "/todos",
        json={"title": "Just a title"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Just a title"
    assert data["description"] is None
