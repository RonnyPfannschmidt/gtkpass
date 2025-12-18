"""Background task service for GTKPass.

This module provides functionality for running tasks in background threads
to avoid blocking the UI.
"""

import logging
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Optional, Self

logger = logging.getLogger(__name__)


class BackgroundService:
    """Service for running tasks in background threads.

    This service implements the context manager protocol for proper
    resource management. Always use it with the 'with' statement.

    Example:
        with BackgroundService(max_workers=4) as service:
            future = service.submit(my_function, arg1, arg2)
            result = future.result()
    """

    def __init__(self, max_workers: int = 4):
        """
        Initialize the background service.

        Args:
            max_workers: Maximum number of worker threads.
        """
        self._executor: Optional[ThreadPoolExecutor] = None
        self._max_workers = max_workers
        self._lock = threading.Lock()

    def submit(
        self,
        func: Callable[..., Any],
        *args,
        **kwargs,
    ) -> Future:
        """
        Submit a task to run in the background.

        Args:
            func: The function to execute in the background.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            A Future object representing the execution.

        Raises:
            RuntimeError: If the service is not initialized (not in context).
        """
        if self._executor is None:
            raise RuntimeError(
                "BackgroundService not initialized. Use it as a context manager:\n"
                "    with BackgroundService() as service:\n"
                "        service.submit(...)"
            )

        logger.debug(f"Submitting task: {func.__name__}")
        return self._executor.submit(func, *args, **kwargs)

    def __enter__(self) -> Self:
        """Enter the context manager and initialize the thread pool.

        Returns:
            Self: The initialized service instance.
        """
        with self._lock:
            if self._executor is None:
                self._executor = ThreadPoolExecutor(
                    max_workers=self._max_workers,
                    thread_name_prefix="gtkpass-worker",
                )
                logger.info(
                    f"Background service initialized with {self._max_workers} workers"
                )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit the context manager and shutdown the thread pool.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Exception traceback if an exception occurred.

        Returns:
            False to propagate exceptions.
        """
        with self._lock:
            if self._executor is not None:
                self._executor.shutdown(wait=True)
                self._executor = None
                logger.info("Background service shut down")
        return False
