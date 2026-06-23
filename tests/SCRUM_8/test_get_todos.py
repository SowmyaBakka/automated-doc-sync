"""Integration tests for the GET /todos endpoint."""

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


def test_get_todos_empty_store_returns_200_with_empty_list(client):
    """Test GET /todos on empty store returns 200 with []."""
    response = client.get("/todos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_todos_after_creating_items(client):
    """Test GET /todos returns 200 with array of TodoItem after creating items."""
    # Create two items
    response1 = client.post("/todos", json={"title": "First"})
    response2 = client.post("/todos", json={"title": "Second"})
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    
    # Get all items
    response = client.get("/todos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Verify items have correct structure
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "description" in item
        assert "done" in item
        assert "createdAt" in item
