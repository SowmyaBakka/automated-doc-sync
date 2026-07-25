"""Password hashing primitives for SCRUM-10."""

from __future__ import annotations

import hashlib
import hmac
import os


class PasswordHasher:
    """Hash and verify passwords using salted PBKDF2-HMAC-SHA256."""

    _ALGORITHM = "pbkdf2_sha256"
    _ITERATIONS = 390000

    def hash_password(self, password: str) -> str:
        """Return a salted password hash string safe for in-memory persistence."""
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            self._ITERATIONS,
        )
        return f"{self._ALGORITHM}${self._ITERATIONS}${salt.hex()}${digest.hex()}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against a serialized PBKDF2 hash."""
        try:
            algorithm, iterations_raw, salt_hex, digest_hex = password_hash.split("$")
        except ValueError:
            return False

        if algorithm != self._ALGORITHM:
            return False

        try:
            iterations = int(iterations_raw)
            salt = bytes.fromhex(salt_hex)
            stored_digest = bytes.fromhex(digest_hex)
        except (ValueError, TypeError):
            return False

        computed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )
        return hmac.compare_digest(computed, stored_digest)
