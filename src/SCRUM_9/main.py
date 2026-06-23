"""FastAPI entry point for the SCRUM-9 expense tracking API."""

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI

from src.SCRUM_9.routes.expenses import router as expenses_router, set_store
from src.SCRUM_9.store.json_store import JsonStore


def get_storage_file_path() -> str:
    """Resolve JSON storage file path from environment.

    The default keeps local development simple while allowing tests and
    runtime environments to point at an isolated file.
    """
    return os.getenv("SCRUM_9_STORAGE_PATH", "expenses.json")


store = JsonStore(file_path=get_storage_file_path())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load store and inject dependencies at startup."""
    await store.load()
    set_store(store)
    yield


app = FastAPI(
    title="Expense Tracker API",
    description="SCRUM-9 API for recording and reading expenses",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(expenses_router)


@app.get("/", tags=["root"])
async def read_root() -> dict[str, str]:
    """Simple root endpoint for connectivity checks."""
    return {"message": "Welcome to the Expense Tracker API. See /docs."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
