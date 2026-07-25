"""FastAPI entry point for SCRUM-10 authentication API."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.SCRUM_10.errors import ApiError, from_request_validation_error
from src.SCRUM_10.routes.auth import router as auth_router

app = FastAPI(
    title="Auth API",
    description="SCRUM-10 API for user registration and login",
    version="1.0.0",
)

app.include_router(auth_router)


@app.exception_handler(ApiError)
async def api_error_exception_handler(request, exc: ApiError):
    """Return deterministic API error payloads for known failures."""
    return JSONResponse(status_code=exc.status_code, content=exc.to_payload())


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc: RequestValidationError):
    """Normalize framework-level validation faults into the shared error shape."""
    mapped = from_request_validation_error(exc)
    return JSONResponse(status_code=mapped.status_code, content=mapped.to_payload())


@app.get("/", tags=["root"])
async def read_root() -> dict[str, str]:
    """Simple root endpoint for connectivity checks."""
    return {"message": "Welcome to the SCRUM-10 Auth API. See /docs."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
