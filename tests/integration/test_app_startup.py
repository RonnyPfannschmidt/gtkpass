"""Integration tests for the application startup."""

import pytest


@pytest.mark.integration
class TestApplicationStartup:
    """Test application startup and initialization."""

    def test_core_modules_import(self):
        """Test that core modules (non-GTK) can be imported."""
        # Test modules that don't require GTK
        import gtkpass
        import gtkpass.services
        import gtkpass.services.background

        assert gtkpass is not None
        assert gtkpass.services is not None
        assert gtkpass.services.background is not None

    @pytest.mark.skipif(
        not pytest.importorskip("gi.repository.Gtk", minversion="4.0"),
        reason="GTK4 not available",
    )
    def test_gtk_modules_import(self):
        """Test that GTK modules can be imported when GTK is available."""
        import gtkpass.app
        import gtkpass.window

        assert gtkpass.app is not None
        assert gtkpass.window is not None

    def test_service_integration(self):
        """Test that services can be initialized together."""
        from gtkpass.services.background import BackgroundService

        with BackgroundService() as bg_service:
            # Test that we can submit a simple task
            future = bg_service.submit(lambda: "test")
            result = future.result(timeout=1.0)
            assert result == "test"
