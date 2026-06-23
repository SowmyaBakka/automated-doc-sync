"""To-do items REST API router.

Defines three endpoints:
- POST /todos — create a new to-do item
- GET /todos — retrieve all to-do items
- GET /todos/{id} — retrieve a single to-do item by ID
"""

from fastapi import APIRouter, HTTPException, status
from src.models.todo import TodoCreate, TodoItem
from src.store.json_store import JsonStore

router = APIRouter(prefix="/todos", tags=["todos"])

# Store instance (will be injected by the app)
_store: JsonStore = None


def set_store(store: JsonStore) -> None:
    """Set the store instance for the router.
    
    Called by the FastAPI app during startup.
    """
    global _store
    _store = store


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TodoItem)
async def create_todo(todo_create: TodoCreate) -> TodoItem:
    """Create a new to-do item.
    
    Args:
        todo_create: Request body with title and optional description.
        
    Returns:
        The created to-do item with id, title, description, done, createdAt.
        
    Raises:
        400: If title is missing or empty.
    """
    if not _store:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Store not initialized"
        )
    
    # Convert Pydantic model to dict for store
    todo_dict = {
        "title": todo_create.title,
        "description": todo_create.description,
    }
    
    # Add to store and get full item back
    created_item = await _store.add(todo_dict)
    
    # Convert back to Pydantic model for response
    return TodoItem(**created_item)


@router.get("", response_model=list[TodoItem])
async def get_todos() -> list[TodoItem]:
    """Retrieve all to-do items.
    
    Returns:
        List of all to-do items (may be empty).
    """
    if not _store:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Store not initialized"
        )
    
    items = await _store.get_all()
    
    # Convert each item to Pydantic model
    return [TodoItem(**item) for item in items]


@router.get("/{item_id}", response_model=TodoItem)
async def get_todo(item_id: int) -> TodoItem:
    """Retrieve a single to-do item by ID.
    
    Args:
        item_id: The ID of the to-do item to retrieve.
        
    Returns:
        The to-do item if found.
        
    Raises:
        404: If no item with the given ID exists.
    """
    if not _store:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Store not initialized"
        )
    
    item = await _store.get_by_id(item_id)
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"To-do item with id {item_id} not found"
        )
    
    return TodoItem(**item)
