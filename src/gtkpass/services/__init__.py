"""Service layer for GTKPass.

This package contains service classes that handle business logic
and interactions with external systems (GPG, Git, filesystem, etc.).
"""

from typing import Protocol


class Service(Protocol):
    """Base protocol for all services."""

    def initialize(self) -> None:
        """Initialize the service."""
        ...

    def cleanup(self) -> None:
        """Clean up resources used by the service."""
        ...


__all__ = ["Service"]
