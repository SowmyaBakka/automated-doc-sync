"""Authentication business workflows for SCRUM-10."""

from __future__ import annotations

from src.SCRUM_10.errors import EmailAlreadyExistsError, InvalidCredentialsError
from src.SCRUM_10.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from src.SCRUM_10.security.password_hasher import PasswordHasher
from src.SCRUM_10.security.token_provider import TokenProvider
from src.SCRUM_10.store.in_memory_user_repo import InMemoryUserRepository


class AuthService:
    """Route-independent registration and login logic."""

    def __init__(
        self,
        repository: InMemoryUserRepository,
        hasher: PasswordHasher,
        token_provider: TokenProvider,
    ) -> None:
        self._repository = repository
        self._hasher = hasher
        self._token_provider = token_provider

    def register(self, payload: RegisterRequest) -> RegisterResponse:
        """Register a user with hashed password storage only."""
        if self._repository.exists_by_email(payload.email):
            raise EmailAlreadyExistsError()

        password_hash = self._hasher.hash_password(payload.password)
        user = self._repository.create_user(
            username=payload.username,
            email=payload.email,
            password_hash=password_hash,
        )
        return RegisterResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            message="User registered successfully",
        )

    def login(self, payload: LoginRequest) -> LoginResponse:
        """Authenticate credentials and return a temporary mock token."""
        user = self._repository.get_by_email(payload.email)
        if user is None:
            raise InvalidCredentialsError()

        if not self._hasher.verify_password(payload.password, user.password_hash):
            raise InvalidCredentialsError()

        token = self._token_provider.generate(user)
        return LoginResponse(token=token, token_type="Bearer")
