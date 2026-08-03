"""Tests for auth utilities — password hashing, JWT (no network, no database)."""

from server.models.auth import hash_password, verify_password, create_access_token, decode_access_token


def test_hash_password_roundtrip():
    pwd = "secret-password-123"
    hashed = hash_password(pwd)
    assert hashed.startswith("$pbkdf2-sha256$")
    assert verify_password(pwd, hashed)


def test_hash_password_wrong_password():
    pwd = "secret-password-123"
    hashed = hash_password(pwd)
    assert not verify_password("wrong-password", hashed)


def test_hash_is_salted():
    h1 = hash_password("same-password")
    h2 = hash_password("same-password")
    assert h1 != h2


def test_jwt_roundtrip():
    token = create_access_token("user123", "alice")
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["username"] == "alice"


def test_jwt_invalid():
    assert decode_access_token("not-a-token") is None
