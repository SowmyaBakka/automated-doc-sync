"""Error contract tests for SCRUM-10 authentication endpoints."""


def _assert_error_shape(payload: dict, expected_code: str) -> None:
    assert "error" in payload
    assert payload["error"]["code"] == expected_code
    assert isinstance(payload["error"].get("message"), str)
    assert "details" in payload["error"]
    assert isinstance(payload["error"]["details"], list)


def test_400_error_shape(auth_client):
    response = auth_client.post(
        "/register",
        json={"username": "alice", "email": "bad", "password": "short"},
    )

    assert response.status_code == 400
    _assert_error_shape(response.json(), "VALIDATION_ERROR")


def test_401_error_shape(auth_client):
    response = auth_client.post(
        "/login",
        json={"email": "missing@example.com", "password": "StrongPass123"},
    )

    assert response.status_code == 401
    _assert_error_shape(response.json(), "INVALID_CREDENTIALS")


def test_409_error_shape(auth_client):
    auth_client.post(
        "/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "StrongPass123",
        },
    )
    response = auth_client.post(
        "/register",
        json={
            "username": "alice-two",
            "email": "alice@example.com",
            "password": "AnotherPass123",
        },
    )

    assert response.status_code == 409
    _assert_error_shape(response.json(), "EMAIL_ALREADY_EXISTS")
