"""FastAPI application entry point for the to-do REST API.

Sets up the FastAPI app with:
- Lifespan event to load the JSON store at startup
- Mounted todos router with /todos prefix
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.SCRUM_8.routes.todos import router as todos_router, set_store
from src.SCRUM_8.store.json_store import JsonStore

# Global store instance
store = JsonStore()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager.
    
    On startup:
    - Load the JSON store from disk
    - Inject the store into the router
    
    On shutdown:
    - No special cleanup needed (file is synced on every write)
    """
    # Startup
    await store.load()
    set_store(store)
    print("✓ Application startup: loaded todos.json")
    
    yield
    
    # Shutdown
    print("✓ Application shutdown")


# Create FastAPI app
app = FastAPI(
    title="To-Do REST API",
    description="A simple REST API to create and retrieve personal to-do items",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount the todos router
app.include_router(todos_router)


@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint for testing connectivity."""
    return {"message": "Welcome to the To-Do API. See /docs for API documentation."}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
