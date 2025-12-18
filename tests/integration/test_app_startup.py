"""Integration tests for the application startup."""

import pytest


@pytest.mark.integration
class TestApplicationStartup:
    """Test application startup and initialization."""

    def test_background_service_integration(self):
        """Test that background service integrates properly."""
        from gtkpass.services.background import BackgroundService

        with BackgroundService() as bg_service:
            # Test that we can submit a simple task
            future = bg_service.submit(lambda: "test")
            result = future.result(timeout=1.0)
            assert result == "test"
