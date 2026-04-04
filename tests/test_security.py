"""
Security tests for the Disparado_Casos_testes workflow.
"""

import pytest
import os
from unittest.mock import patch

from app.security.secrets import SecretManager, sanitize_for_logging


class TestSecretManager:
    """Test SecretManager functionality."""

    def test_get_optional_secret(self):
        """Test getting an optional secret that doesn't exist."""
        with patch.dict("os.environ", {}, clear=True):
            value = SecretManager.get("NON_EXISTENT_SECRET", "default_value")
            assert value == "default_value"

    def test_get_required_secret_missing(self):
        """Test getting a required secret that doesn't exist raises error."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(EnvironmentError, match="Required environment variable"):
                SecretManager.get_required("NON_EXISTENT_SECRET")

    def test_get_required_secret_present(self):
        """Test getting a required secret that exists."""
        with patch.dict("os.environ", {"TEST_SECRET": "secret_value"}):
            value = SecretManager.get_required("TEST_SECRET")
            assert value == "secret_value"

    def test_generate_env_example(self):
        """Test generating .env.example content."""
        content = SecretManager.generate_env_example()

        assert "# Environment variables for Disparado_Casos_testes workflow" in content
        assert "GOOGLE_SHEETS_OAUTH2_CLIENT_ID=" in content
        assert "API_KEY=" in content
        assert "LOG_LEVEL=" in content
        assert "ENVIRONMENT=" in content


class TestSanitizeForLogging:
    """Test sanitize_for_logging function."""

    def test_sanitize_basic_dict(self):
        """Test sanitizing a basic dictionary."""
        data = {
            "username": "john_doe",
            "password": "secret123",
            "api_key": "abc-def-ghi",
            "normal_field": "value",
        }

        sanitized = sanitize_for_logging(data)

        assert sanitized["username"] == "john_doe"
        assert sanitized["password"] == "***REDACTED***"
        assert sanitized["api_key"] == "***REDACTED***"
        assert sanitized["normal_field"] == "value"

    def test_sanitize_nested_dict(self):
        """Test sanitizing a nested dictionary."""
        data = {
            "user": {"username": "john_doe", "password": "secret123"},
            "api_data": {"token": "secret_token", "endpoint": "/api/users"},
        }

        sanitized = sanitize_for_logging(data)

        assert sanitized["user"]["username"] == "john_doe"
        assert sanitized["user"]["password"] == "***REDACTED***"
        assert sanitized["api_data"]["token"] == "***REDACTED***"
        assert sanitized["api_data"]["endpoint"] == "/api/users"

    def test_sanitize_list_of_dicts(self):
        """Test sanitizing a list containing dictionaries."""
        data = {
            "users": [
                {"username": "user1", "password": "pass1"},
                {"username": "user2", "password": "pass2"},
            ],
            "public_info": "visible",
        }

        sanitized = sanitize_for_logging(data)

        assert sanitized["users"][0]["username"] == "user1"
        assert sanitized["users"][0]["password"] == "***REDACTED***"
        assert sanitized["users"][1]["username"] == "user2"
        assert sanitized["users"][1]["password"] == "***REDACTED***"
        assert sanitized["public_info"] == "visible"

    def test_sanitize_case_insensitive(self):
        """Test that sanitization is case insensitive."""
        data = {"PASSWORD": "secret", "Api_Key": "key", "AUthToKen": "token"}

        sanitized = sanitize_for_logging(data)

        assert sanitized["PASSWORD"] == "***REDACTED***"
        assert sanitized["Api_Key"] == "***REDACTED***"
        assert sanitized["AUthToKen"] == "***REDACTED***"
