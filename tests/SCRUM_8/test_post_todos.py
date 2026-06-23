"""Integration tests for the POST /todos endpoint."""

import pytest
from fastapi.testclient import TestClient

from src.SCRUM_8.main import app
from src.SCRUM_8.store.json_store import JsonStore


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_post_todos_valid_body_returns_201():
    """Test POST /todos with valid body returns 201 + full TodoItem."""
    client = TestClient(app)
    
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


@pytest.mark.asyncio
async def test_post_todos_missing_title_returns_400():
    """Test POST /todos without title returns 400 with error detail."""
    client = TestClient(app)
    
    response = client.post(
        "/todos",
        json={"description": "Some description"}
    )
    
    assert response.status_code == 422  # Pydantic validation error
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_post_todos_empty_title_returns_400():
    """Test POST /todos with empty title returns 400."""
    client = TestClient(app)
    
    response = client.post(
        "/todos",
        json={"title": "", "description": "Something"}
    )
    
    assert response.status_code == 422  # Pydantic validation error
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_post_todos_whitespace_only_title_returns_400():
    """Test POST /todos with whitespace-only title returns 400."""
    client = TestClient(app)
    
    response = client.post(
        "/todos",
        json={"title": "   ", "description": "Something"}
    )
    
    assert response.status_code == 422  # Pydantic validation error
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_post_todos_description_optional():
    """Test POST /todos works without description (optional field)."""
    client = TestClient(app)
    
    response = client.post(
        "/todos",
        json={"title": "Just a title"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Just a title"
    assert data["description"] is None
