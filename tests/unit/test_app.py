"""Unit tests for the main application."""

import pytest


@pytest.mark.unit
class TestGTKPassApp:
    """Test cases for the GTKPass application."""

    def test_app_module_exists(self):
        """Test that the app module exists."""
        # Test without importing GTK which may not be available
        import importlib.util

        spec = importlib.util.find_spec("gtkpass.app")
        assert spec is not None

    def test_app_has_main_function(self):
        """Test that the app module has a main function."""
        # We can import without instantiating
        pytest.importorskip("gi.repository.Gtk", minversion="4.0")
        from gtkpass.app import main

        assert callable(main)
