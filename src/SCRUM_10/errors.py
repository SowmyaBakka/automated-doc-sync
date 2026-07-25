"""Shared API error types and helpers for SCRUM-10."""

from __future__ import annotations

from typing import Any

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


class ApiError(Exception):
    """Application exception that carries HTTP status and deterministic payload."""

    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or []

    def to_payload(self) -> dict[str, Any]:
        """Return the shared API error envelope."""
        payload: dict[str, Any] = {
            "error": {
                "code": self.code,
                "message": self.message,
            }
        }
        if self.details:
            payload["error"]["details"] = self.details
        return payload


class EmailAlreadyExistsError(ApiError):
    """Raised when attempting to register an existing email."""

    def __init__(self) -> None:
        super().__init__(
            status_code=409,
            code="EMAIL_ALREADY_EXISTS",
            message="email is already registered",
            details=[{"field": "email", "reason": "duplicate"}],
        )


class InvalidCredentialsError(ApiError):
    """Raised when submitted login credentials are invalid."""

    def __init__(self) -> None:
        super().__init__(
            status_code=401,
            code="INVALID_CREDENTIALS",
            message="invalid email or password",
            details=[{"field": "credentials", "reason": "invalid"}],
        )


def validation_error(message: str, details: list[dict[str, str]]) -> ApiError:
    """Build a deterministic validation error payload."""
    return ApiError(
        status_code=400,
        code="VALIDATION_ERROR",
        message=message,
        details=details,
    )


def _extract_field(loc: tuple[Any, ...]) -> str:
    """Extract the most relevant field name from validation location tuples."""
    parts = [str(part) for part in loc if str(part) != "body"]
    if not parts:
        return "body"
    return parts[-1]


def from_pydantic_validation_error(exc: ValidationError) -> ApiError:
    """Map a Pydantic validation error into the shared validation envelope."""
    details: list[dict[str, str]] = []
    for error in exc.errors():
        field = _extract_field(tuple(error.get("loc", ())))
        reason = str(error.get("type", "invalid"))
        details.append({"field": field, "reason": reason})

    if details:
        message = f"{details[0]['field']} is invalid"
    else:
        message = "invalid request payload"

    return validation_error(message=message, details=details or [{"field": "body", "reason": "invalid"}])


def from_request_validation_error(exc: RequestValidationError) -> ApiError:
    """Map framework-level validation errors into the shared validation envelope."""
    details: list[dict[str, str]] = []
    for error in exc.errors():
        field = _extract_field(tuple(error.get("loc", ())))
        reason = str(error.get("type", "invalid"))
        details.append({"field": field, "reason": reason})

    message = "invalid request payload"
    if details:
        message = f"{details[0]['field']} is invalid"

    return validation_error(message=message, details=details or [{"field": "body", "reason": "invalid"}])
