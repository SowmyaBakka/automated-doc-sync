"""FastAPI entry point for the SCRUM-9 expense tracking API."""

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.SCRUM_9.routes.expenses import router as expenses_router, set_store
from src.SCRUM_9.store.json_store import (
    JsonStore,
    JsonStoreCorruptedDataError,
    JsonStoreReadError,
    JsonStoreWriteError,
)


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
    set_store(store)
    yield


app = FastAPI(
    title="Expense Tracker API",
    description="SCRUM-9 API for recording and reading expenses",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(expenses_router)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc: RequestValidationError):
    """Normalize framework validation failures to HTTP 400."""
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@app.exception_handler(JsonStoreCorruptedDataError)
async def corrupted_store_exception_handler(request, exc: JsonStoreCorruptedDataError):
    """Map corrupted storage data faults to a sanitized 500 response."""
    return JSONResponse(status_code=500, content={"detail": "storage data is corrupted"})


@app.exception_handler(JsonStoreReadError)
@app.exception_handler(JsonStoreWriteError)
async def storage_io_exception_handler(request, exc: Exception):
    """Map storage IO faults to a sanitized 500 response."""
    return JSONResponse(status_code=500, content={"detail": "storage operation failed"})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc: Exception):
    """Return a generic sanitized response for unexpected failures."""
    return JSONResponse(status_code=500, content={"detail": "internal server error"})


@app.get("/", tags=["root"])
async def read_root() -> dict[str, str]:
    """Simple root endpoint for connectivity checks."""
    return {"message": "Welcome to the Expense Tracker API. See /docs."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
