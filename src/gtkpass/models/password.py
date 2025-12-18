"""Password data model.

This module defines the data structures for password entries.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Password:
    """Represents a password entry.

    This is the core data structure for storing password information.
    Compatible with passwordstore format.
    """

    name: str
    """Display name of the password entry"""

    path: Path
    """Path to the password file in the store"""

    password: str
    """The actual password (decrypted)"""

    username: Optional[str] = None
    """Username associated with this password"""

    url: Optional[str] = None
    """URL/website this password is for"""

    notes: Optional[str] = None
    """Additional notes about this password"""

    otp_secret: Optional[str] = None
    """OTP secret if TOTP/HOTP is configured"""

    def clear(self) -> None:
        """Clear sensitive data from memory.

        This should be called when the password data is no longer needed
        to minimize time sensitive data stays in memory.
        """
        self.password = ""
        if self.otp_secret:
            self.otp_secret = ""

    def to_dict(self) -> dict:
        """Convert to dictionary representation.

        Returns:
            Dictionary with password data (excluding OTP secret for security)
        """
        return {
            "name": self.name,
            "path": str(self.path),
            "username": self.username,
            "url": self.url,
            "notes": self.notes,
        }


@dataclass
class PasswordEntry:
    """Lightweight password entry for list display.

    Contains minimal information needed to display in the password list.
    Full password data is loaded only when selected.
    """

    name: str
    """Display name"""

    path: Path
    """Path in the password store"""

    subtitle: Optional[str] = None
    """Subtitle to display (username, URL, or path)"""

    def __str__(self) -> str:
        """String representation."""
        return f"{self.name} ({self.subtitle or self.path})"
