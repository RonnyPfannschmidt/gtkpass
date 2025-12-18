"""Main application window."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk  # noqa: E402


class GTKPassWindow(Adw.ApplicationWindow):
    """Main application window for GTKPass."""

    def __init__(self, **kwargs):
        """Initialize the main window."""
        super().__init__(**kwargs)

        # Window properties
        self.set_title("GTKPass")
        self.set_default_size(800, 600)

        # Create header bar
        header_bar = Adw.HeaderBar()

        # Create menu button
        menu_button = Gtk.MenuButton()
        menu = Gio.Menu()
        menu.append("About GTKPass", "app.about")
        menu.append("Quit", "app.quit")
        menu_button.set_menu_model(menu)
        menu_button.set_icon_name("open-menu-symbolic")
        header_bar.pack_end(menu_button)

        # Create a placeholder status page for now
        status_page = Adw.StatusPage(
            title="Welcome to GTKPass",
            description="A modern password manager for GNOME",
            icon_name="io.github.ronnypfannschmidt.GTKPass",
        )

        # Create toolbar view (combines header bar and content)
        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.set_content(status_page)

        # Set window content
        self.set_content(toolbar_view)


# Import Gio after gi.require_version
from gi.repository import Gio  # noqa: E402
