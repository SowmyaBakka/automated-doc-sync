"""Service-level tests for SCRUM-10 authentication workflows."""

import pytest

from src.SCRUM_10.errors import EmailAlreadyExistsError, InvalidCredentialsError
from src.SCRUM_10.schemas.auth import LoginRequest, RegisterRequest
from src.SCRUM_10.security.password_hasher import PasswordHasher
from src.SCRUM_10.security.token_provider import MockTokenProvider
from src.SCRUM_10.services.auth_service import AuthService
from src.SCRUM_10.store.in_memory_user_repo import InMemoryUserRepository


def _build_service() -> tuple[AuthService, InMemoryUserRepository]:
    repo = InMemoryUserRepository()
    service = AuthService(repo, PasswordHasher(), MockTokenProvider())
    return service, repo


def test_register_persists_hash_not_plaintext():
    service, repo = _build_service()
    payload = RegisterRequest(
        username="alice",
        email="alice@example.com",
        password="StrongPass123",
    )

    response = service.register(payload)
    stored = repo.get_by_email("alice@example.com")

    assert response.email == "alice@example.com"
    assert stored is not None
    assert stored.password_hash != "StrongPass123"
    assert stored.password_hash.startswith("pbkdf2_sha256$")


def test_register_duplicate_email_raises_conflict():
    service, _ = _build_service()
    first = RegisterRequest(
        username="alice",
        email="alice@example.com",
        password="StrongPass123",
    )
    second = RegisterRequest(
        username="alice2",
        email="ALICE@example.com",
        password="StrongPass123",
    )

    service.register(first)
    with pytest.raises(EmailAlreadyExistsError):
        service.register(second)


def test_login_success_and_invalid_password_behavior():
    service, _ = _build_service()
    service.register(
        RegisterRequest(
            username="alice",
            email="alice@example.com",
            password="StrongPass123",
        )
    )

    success = service.login(
        LoginRequest(email="alice@example.com", password="StrongPass123")
    )
    assert success.token.startswith("mock-token-")

    with pytest.raises(InvalidCredentialsError):
        service.login(LoginRequest(email="alice@example.com", password="WrongPass123"))
