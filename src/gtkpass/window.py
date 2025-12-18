"""Main application window."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, Gtk  # noqa: E402


@Gtk.Template(filename="src/gtkpass/ui/blueprints/window.ui")
class GTKPassWindow(Adw.ApplicationWindow):
    """Main application window for GTKPass.

    UI is defined in ui/blueprints/window.blp and compiled to window.ui.
    """

    __gtype_name__ = "GTKPassWindow"

    def __init__(self, **kwargs):
        """Initialize the main window."""
        super().__init__(**kwargs)

