"""Acceptance tests for GTKPass application.

These tests verify end-to-end functionality from a user perspective.
"""

import pytest


@pytest.mark.acceptance
class TestApplicationAcceptance:
    """Acceptance tests for the GTKPass application."""

    def test_application_module_structure(self):
        """
        As a user, I want the application to have a clear module structure
        So that I can understand and navigate the codebase.
        """
        import importlib.util

        # Core modules should exist
        assert importlib.util.find_spec("gtkpass") is not None
        assert importlib.util.find_spec("gtkpass.services") is not None
        assert importlib.util.find_spec("gtkpass.services.background") is not None

    @pytest.mark.skipif(
        not pytest.importorskip("gi.repository.Gtk", minversion="4.0"),
        reason="GTK4 not available",
    )
    def test_application_can_be_imported(self):
        """
        As a user, I want to import the application
        So that I can use it in my environment.
        """
        from gtkpass import app

        assert hasattr(app, "GTKPassApp")
        assert hasattr(app, "main")

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

    def test_service_protocol_compliance(self):
        """
        As a developer, I want services to follow the Service protocol
        So that they can be used consistently.
        """
        from gtkpass.services.background import BackgroundService

        # Check that BackgroundService implements the Service protocol
        service = BackgroundService()

        # Should have initialize and cleanup methods
        assert hasattr(service, "initialize")
        assert hasattr(service, "cleanup")
        assert callable(service.initialize)
        assert callable(service.cleanup)

        # Should work correctly
        service.initialize()
        service.cleanup()
