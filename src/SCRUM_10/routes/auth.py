"""Authentication routes for SCRUM-10.

Endpoint handlers are implemented in later tasks.
"""

from typing import Any

from fastapi import APIRouter, Body
from pydantic import ValidationError

from src.SCRUM_10.errors import from_pydantic_validation_error, validation_error
from src.SCRUM_10.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from src.SCRUM_10.security.password_hasher import PasswordHasher
from src.SCRUM_10.security.token_provider import MockTokenProvider
from src.SCRUM_10.services.auth_service import AuthService
from src.SCRUM_10.store.in_memory_user_repo import InMemoryUserRepository

router = APIRouter(tags=["auth"])

_repo = InMemoryUserRepository()
_service = AuthService(
	repository=_repo,
	hasher=PasswordHasher(),
	token_provider=MockTokenProvider(),
)


def reset_auth_state() -> None:
	"""Clear auth state for test isolation and deterministic behavior."""
	_repo.clear()


def _validate_register_payload(payload: dict[str, Any]) -> RegisterRequest:
	"""Validate register payload and map schema failures to shared errors."""
	try:
		return RegisterRequest.model_validate(payload)
	except ValidationError as exc:
		raise from_pydantic_validation_error(exc) from exc


def _validate_login_payload(payload: dict[str, Any]) -> LoginRequest:
	"""Validate login payload and map schema failures to shared errors."""
	try:
		return LoginRequest.model_validate(payload)
	except ValidationError as exc:
		raise from_pydantic_validation_error(exc) from exc


@router.post("/register", response_model=RegisterResponse, status_code=201)
async def register(raw_payload: Any = Body(...)) -> RegisterResponse:
	"""Register a new user account with unique normalized email."""
	if not isinstance(raw_payload, dict):
		raise validation_error(
			message="body is invalid",
			details=[{"field": "body", "reason": "type_error"}],
		)

	payload = _validate_register_payload(raw_payload)
	return _service.register(payload)


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(raw_payload: Any = Body(...)) -> LoginResponse:
	"""Authenticate an existing user and return a temporary token."""
	if not isinstance(raw_payload, dict):
		raise validation_error(
			message="body is invalid",
			details=[{"field": "body", "reason": "type_error"}],
		)

	payload = _validate_login_payload(raw_payload)
	return _service.login(payload)
