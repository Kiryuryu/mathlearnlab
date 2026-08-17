"""Tests for admin secret checking — no network, no database."""

from fastapi import HTTPException
from server.routers import admin


def test_check_secret_correct(monkeypatch):
    monkeypatch.setattr(admin.settings, "admin_secret", "test-secret-abc")
    # Should not raise
    admin._check_secret("test-secret-abc")


def test_check_secret_wrong_raises(monkeypatch):
    monkeypatch.setattr(admin.settings, "admin_secret", "test-secret-abc")
    try:
        admin._check_secret("wrong-secret")
        assert False, "should have raised"
    except HTTPException as e:
        assert e.status_code == 403


def test_check_secret_empty_raises(monkeypatch):
    monkeypatch.setattr(admin.settings, "admin_secret", "test-secret-abc")
    try:
        admin._check_secret("")
        assert False, "should have raised"
    except HTTPException as e:
        assert e.status_code == 403


def test_check_secret_unconfigured_raises(monkeypatch):
    monkeypatch.setattr(admin.settings, "admin_secret", "")
    try:
        admin._check_secret("anything")
        assert False, "should have raised"
    except HTTPException as e:
        assert e.status_code == 500
