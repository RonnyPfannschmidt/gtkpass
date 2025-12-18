"""Service layer for GTKPass.

This package contains service classes that handle business logic
and interactions with external systems (GPG, Git, filesystem, etc.).

All services should be context managers to ensure proper resource management.
"""

from typing import Protocol, Self


class Service(Protocol):
    """Base protocol for all services.

    Services are context managers that handle their own resource lifecycle.
    Use them with the 'with' statement to ensure proper cleanup.

    Example:
        with MyService() as service:
            service.do_something()
    """

    def __enter__(self) -> Self:
        """Enter the context manager and initialize the service.

        Returns:
            Self: The initialized service instance.
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit the context manager and clean up resources.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.

        Returns:
            False to propagate exceptions, True to suppress them.
        """
        ...


__all__ = ["Service"]
