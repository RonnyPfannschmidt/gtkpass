"""Unit tests for password data models."""

import pytest
from pathlib import Path
from gtkpass.models.password import Password, PasswordEntry


@pytest.mark.unit
class TestPassword:
    """Test cases for Password model."""

    def test_password_creation(self):
        """Test creating a password entry."""
        password = Password(
            name="Test Password",
            path=Path("/home/user/.password-store/test.gpg"),
            password="secret123",
            username="testuser",
            url="https://example.com",
            notes="Test notes",
        )

        assert password.name == "Test Password"
        assert password.password == "secret123"
        assert password.username == "testuser"

    def test_password_clear(self):
        """Test clearing sensitive data."""
        password = Password(
            name="Test",
            path=Path("/test.gpg"),
            password="secret123",
            otp_secret="JBSWY3DPEHPK3PXP",
        )

        password.clear()

        assert password.password == ""
        assert password.otp_secret == ""
        assert password.name == "Test"  # Non-sensitive data remains

    def test_password_to_dict(self):
        """Test conversion to dictionary."""
        password = Password(
            name="Test",
            path=Path("/test.gpg"),
            password="secret",
            username="user",
        )

        data = password.to_dict()

        assert data["name"] == "Test"
        assert data["username"] == "user"
        assert "password" not in data  # Password not in dict for security


@pytest.mark.unit
class TestPasswordEntry:
    """Test cases for PasswordEntry model."""

    def test_password_entry_creation(self):
        """Test creating a password entry for list display."""
        entry = PasswordEntry(
            name="GitHub",
            path=Path("/github.gpg"),
            subtitle="user@example.com",
        )

        assert entry.name == "GitHub"
        assert entry.subtitle == "user@example.com"

    def test_password_entry_string(self):
        """Test string representation."""
        entry = PasswordEntry(
            name="Test",
            path=Path("/test.gpg"),
            subtitle="info",
        )

        assert "Test" in str(entry)
        assert "info" in str(entry)
