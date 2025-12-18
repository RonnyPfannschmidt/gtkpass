"""Acceptance tests for GTKPass application.

These tests verify end-to-end functionality from a user perspective.
"""

import pytest


@pytest.mark.acceptance
class TestApplicationAcceptance:
    """Acceptance tests for the GTKPass application."""

    def test_background_service_handles_long_running_tasks(self):
        """
        As a user, I want long-running tasks to run in the background
        So that the UI remains responsive.
        """
        import time
        from gtkpass.services.background import BackgroundService

        def long_task():
            time.sleep(0.1)
            return "completed"

        with BackgroundService() as service:
            start = time.time()
            future = service.submit(long_task)
            # Task submission should be immediate
            assert time.time() - start < 0.05

            # Wait for completion
            result = future.result(timeout=2.0)
            assert result == "completed"
