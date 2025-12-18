"""Password list component for GTKPass.

This module provides the password list view that displays all passwords
in a hierarchical tree structure.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk  # noqa: E402


class PasswordListRow(Adw.ActionRow):
    """A row in the password list.

    Displays password name, path, and provides click interaction.
    """

    def __init__(self, name: str, path: str = "", **kwargs):
        """Initialize a password list row.

        Args:
            name: Display name of the password entry
            path: Path or additional info (e.g., username, URL)
            **kwargs: Additional arguments passed to ActionRow
        """
        super().__init__(**kwargs)
        self.set_title(name)
        if path:
            self.set_subtitle(path)

        # Add arrow icon
        icon = Gtk.Image.new_from_icon_name("go-next-symbolic")
        self.add_suffix(icon)

        # Store password metadata
        self.password_name = name
        self.password_path = path


class PasswordList(Gtk.ListBox):
    """Password list widget.

    Displays all passwords in a scrollable list with search capability.
    """

    def __init__(self, **kwargs):
        """Initialize the password list."""
        super().__init__(**kwargs)
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.add_css_class("navigation-sidebar")

    def add_password(self, name: str, path: str = ""):
        """Add a password entry to the list.

        Args:
            name: Password name/title
            path: Additional info (username, URL, etc.)
        """
        row = PasswordListRow(name, path)
        self.append(row)

    def clear_passwords(self):
        """Remove all password entries from the list."""
        while True:
            row = self.get_row_at_index(0)
            if row is None:
                break
            self.remove(row)

    def get_selected_password(self):
        """Get the currently selected password row.

        Returns:
            PasswordListRow or None if no selection
        """
        return self.get_selected_row()
