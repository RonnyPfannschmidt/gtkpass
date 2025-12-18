"""Unit tests for the background service."""

import pytest
from concurrent.futures import Future
from gtkpass.services.background import BackgroundService


@pytest.mark.unit
class TestBackgroundService:
    """Test cases for BackgroundService."""

    def test_initialization(self):
        """Test that the service can be initialized."""
        service = BackgroundService(max_workers=2)
        service.initialize()
        assert service._executor is not None
        service.cleanup()

    def test_cleanup(self):
        """Test that cleanup properly shuts down the executor."""
        service = BackgroundService()
        service.initialize()
        service.cleanup()
        assert service._executor is None

    def test_context_manager(self):
        """Test that the service works as a context manager."""
        with BackgroundService() as service:
            assert service._executor is not None
        assert service._executor is None

    def test_submit_task(self):
        """Test submitting a task to the service."""

        def sample_task(x, y):
            return x + y

        service = BackgroundService()
        service.initialize()

        try:
            future = service.submit(sample_task, 2, 3)
            assert isinstance(future, Future)
            result = future.result(timeout=1.0)
            assert result == 5
        finally:
            service.cleanup()

    def test_submit_without_initialization(self):
        """Test that submitting without initialization raises an error."""
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
