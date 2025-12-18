"""Unit tests for the background service."""

import pytest
from concurrent.futures import Future
from gtkpass.services.background import BackgroundService


@pytest.mark.unit
class TestBackgroundService:
    """Test cases for BackgroundService."""

    def test_context_manager_initialization(self):
        """Test that the service initializes when entering context."""
        service = BackgroundService(max_workers=2)
        assert service._executor is None

        with service:
            assert service._executor is not None

        assert service._executor is None

    def test_context_manager_cleanup(self):
        """Test that cleanup properly shuts down the executor."""
        with BackgroundService() as service:
            assert service._executor is not None
        # After exiting context, executor should be cleaned up
        assert service._executor is None

    def test_context_manager_returns_self(self):
        """Test that __enter__ returns the service instance."""
        with BackgroundService() as service:
            assert isinstance(service, BackgroundService)
            assert service._executor is not None

    def test_submit_task(self):
        """Test submitting a task to the service."""

        def sample_task(x, y):
            return x + y

        with BackgroundService() as service:
            future = service.submit(sample_task, 2, 3)
            assert isinstance(future, Future)
            result = future.result(timeout=1.0)
            assert result == 5

    def test_submit_without_context(self):
        """Test that submitting without context manager raises an error."""
        service = BackgroundService()

        with pytest.raises(RuntimeError, match="not initialized"):
            service.submit(lambda: None)

    def test_multiple_tasks(self):
        """Test submitting multiple tasks."""

        def task(n):
            return n * 2

        with BackgroundService(max_workers=2) as service:
            futures = [service.submit(task, i) for i in range(5)]
            results = [f.result(timeout=1.0) for f in futures]
            assert results == [0, 2, 4, 6, 8]

    def test_reusable_context_manager(self):
        """Test that the service can be used multiple times as context manager."""
        service = BackgroundService()

        # First use
        with service as svc1:
            assert svc1._executor is not None
            future = svc1.submit(lambda: "first")
            assert future.result() == "first"

        assert service._executor is None

        # Second use
        with service as svc2:
            assert svc2._executor is not None
            future = svc2.submit(lambda: "second")
            assert future.result() == "second"

        assert service._executor is None
