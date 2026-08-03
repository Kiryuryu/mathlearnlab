"""Tests for admin secret checking — no network, no database."""

from fastapi import HTTPException
from server.routers import admin


def test_check_secret_correct():
    admin.ADMIN_SECRET = "test-secret-abc"
    class B: secret = "test-secret-abc"
    # Should not raise
    admin._check_secret(B())


def test_check_secret_wrong_raises():
    admin.ADMIN_SECRET = "test-secret-abc"
    class B: secret = "wrong-secret"
    try:
        admin._check_secret(B())
        assert False, "should have raised"
    except HTTPException as e:
        assert e.status_code == 403


def test_check_secret_empty_raises():
    admin.ADMIN_SECRET = "test-secret-abc"
    class B: secret = ""
    try:
        admin._check_secret(B())
        assert False, "should have raised"
    except HTTPException as e:
        assert e.status_code == 403
