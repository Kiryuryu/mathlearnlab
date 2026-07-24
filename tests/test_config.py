"""Tests for server configuration — no network, no database."""

import os
import subprocess
import sys
import tempfile


def test_debug_mode_allows_missing_jwt():
    """When DEBUG=true, missing JWT_SECRET_KEY should not crash."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["DEBUG"] = "true"
        env.pop("JWT_SECRET_KEY", None)
        env.pop("DEEPSEEK_API_KEY", None)
        env.pop("ADMIN_SECRET", None)
        env.pop("DATABASE_URL", None)
        env.pop("SMTP_HOST", None)
        env.pop("SMTP_USER", None)
        env.pop("SMTP_PASS", None)
        env.pop("ADMIN_EMAIL", None)
        # Clear test/CI context so subprocess runs in "production" mode
        env.pop("PYTEST_CURRENT_TEST", None)
        env.pop("CI", None)

        result = subprocess.run(
            [sys.executable, "-c",
             "from server.config import Settings; s = Settings(); assert s.debug == True"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"


def test_production_requires_jwt():
    """When DEBUG=false and JWT_SECRET_KEY is missing, startup should fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["DEBUG"] = "false"
        env.pop("JWT_SECRET_KEY", None)
        env.pop("DEEPSEEK_API_KEY", None)
        env.pop("ADMIN_SECRET", None)
        env.pop("DATABASE_URL", None)
        env.pop("SMTP_HOST", None)
        env.pop("SMTP_USER", None)
        env.pop("SMTP_PASS", None)
        env.pop("ADMIN_EMAIL", None)
        env.pop("PYTEST_CURRENT_TEST", None)
        env.pop("CI", None)

        result = subprocess.run(
            [sys.executable, "-c",
             "from server.config import get_settings; get_settings()"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            capture_output=True,
            text=True,
        )
        # Should fail with RuntimeError
        assert result.returncode != 0
        assert "JWT_SECRET_KEY" in result.stderr or "JWT_SECRET_KEY" in result.stdout


def test_production_requires_deepseek_key():
    """When DEBUG=false and DEEPSEEK_API_KEY is missing, startup should fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["DEBUG"] = "false"
        env["JWT_SECRET_KEY"] = "test-secret-key-12345"
        env.pop("DEEPSEEK_API_KEY", None)
        env.pop("ADMIN_SECRET", None)
        env.pop("DATABASE_URL", None)
        env.pop("SMTP_HOST", None)
        env.pop("SMTP_USER", None)
        env.pop("SMTP_PASS", None)
        env.pop("ADMIN_EMAIL", None)
        env.pop("PYTEST_CURRENT_TEST", None)
        env.pop("CI", None)

        result = subprocess.run(
            [sys.executable, "-c",
             "from server.config import get_settings; get_settings()"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            capture_output=True,
            text=True,
        )
        # Should fail with RuntimeError
        assert result.returncode != 0
        assert "DEEPSEEK_API_KEY" in result.stderr or "DEEPSEEK_API_KEY" in result.stdout


def test_production_with_valid_config_succeeds():
    """When DEBUG=false and all required vars are set, startup should succeed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["DEBUG"] = "false"
        env["JWT_SECRET_KEY"] = "test-secret-key-12345"
        env["DEEPSEEK_API_KEY"] = "sk-test-key-12345"
        env.pop("ADMIN_SECRET", None)
        env.pop("DATABASE_URL", None)
        env.pop("SMTP_HOST", None)
        env.pop("SMTP_USER", None)
        env.pop("SMTP_PASS", None)
        env.pop("ADMIN_EMAIL", None)
        env.pop("PYTEST_CURRENT_TEST", None)
        env.pop("CI", None)

        result = subprocess.run(
            [sys.executable, "-c",
             "from server.config import get_settings; s = get_settings(); assert s.debug == False"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"


def test_settings_has_expected_fields():
    """Settings should have the expected config fields."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["DEBUG"] = "true"
        env.pop("JWT_SECRET_KEY", None)
        env.pop("DEEPSEEK_API_KEY", None)
        env.pop("ADMIN_SECRET", None)
        env.pop("DATABASE_URL", None)
        env.pop("SMTP_HOST", None)
        env.pop("SMTP_USER", None)
        env.pop("SMTP_PASS", None)
        env.pop("ADMIN_EMAIL", None)
        env.pop("PYTEST_CURRENT_TEST", None)
        env.pop("CI", None)

        result = subprocess.run(
            [sys.executable, "-c",
             """
from server.config import get_settings
s = get_settings()
assert hasattr(s, 'app_name')
assert hasattr(s, 'deepseek_api_key')
assert hasattr(s, 'deepseek_model')
assert hasattr(s, 'jwt_secret_key')
assert hasattr(s, 'jwt_algorithm')
assert hasattr(s, 'jwt_expire_minutes')
assert hasattr(s, 'smtp_host')
assert hasattr(s, 'database_url')
assert s.deepseek_model == 'deepseek-chat'
             """],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"


def test_no_anthropic_references_in_config():
    """Settings should not have anthropic_api_key field anymore."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["DEBUG"] = "true"
        env.pop("JWT_SECRET_KEY", None)
        env.pop("DEEPSEEK_API_KEY", None)
        env.pop("ADMIN_SECRET", None)
        env.pop("DATABASE_URL", None)
        env.pop("SMTP_HOST", None)
        env.pop("SMTP_USER", None)
        env.pop("SMTP_PASS", None)
        env.pop("ADMIN_EMAIL", None)
        env.pop("PYTEST_CURRENT_TEST", None)
        env.pop("CI", None)

        result = subprocess.run(
            [sys.executable, "-c",
             "from server.config import get_settings; s = get_settings(); assert not hasattr(s, 'anthropic_api_key')"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
