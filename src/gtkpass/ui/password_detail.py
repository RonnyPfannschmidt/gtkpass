"""Password detail view component for GTKPass.

This module provides the detail view that displays full password information
when a password is selected from the list.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk  # noqa: E402


class PasswordDetailView(Gtk.Box):
    """Password detail view widget.

    Displays detailed information about a selected password including:
    - Password name
    - Username
    - Password (with show/hide)
    - URL
    - Notes
    - Copy buttons for each field
    """

    def __init__(self, **kwargs):
        """Initialize the password detail view."""
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)

        # Create scrolled window for content
        scrolled = Gtk.ScrolledWindow(vexpand=True)

        # Create preferences page for layout
        self.prefs_page = Adw.PreferencesPage()

        # Password information group
        self.info_group = Adw.PreferencesGroup(title="Password Information")

        # Name row
        self.name_row = Adw.ActionRow(title="Name")
        self.info_group.add(self.name_row)

        # Username row with copy button
        self.username_row = Adw.ActionRow(title="Username")
        copy_username_btn = Gtk.Button(
            icon_name="edit-copy-symbolic",
            valign=Gtk.Align.CENTER,
            tooltip_text="Copy username",
        )
        self.username_row.add_suffix(copy_username_btn)
        self.info_group.add(self.username_row)

        # Password row with show/hide and copy
        self.password_row = Adw.PasswordEntryRow(
            title="Password",
            editable=False,
        )
        self.info_group.add(self.password_row)

        # URL row with copy button
        self.url_row = Adw.ActionRow(title="URL")
        copy_url_btn = Gtk.Button(
            icon_name="edit-copy-symbolic",
            valign=Gtk.Align.CENTER,
            tooltip_text="Copy URL",
        )
        self.url_row.add_suffix(copy_url_btn)
        self.info_group.add(self.url_row)

        # Notes group
        self.notes_group = Adw.PreferencesGroup(title="Notes")
        self.notes_label = Gtk.Label(
            wrap=True,
            xalign=0,
            margin_top=6,
            margin_bottom=6,
            margin_start=12,
            margin_end=12,
        )
        self.notes_group.add(self.notes_label)

        # Add groups to preferences page
        self.prefs_page.add(self.info_group)
        self.prefs_page.add(self.notes_group)

        scrolled.set_child(self.prefs_page)
        self.append(scrolled)

    def set_password_data(
        self,
        name: str,
        username: str = "",
        password: str = "",
        url: str = "",
        notes: str = "",
    ):
        """Set the password data to display.

        Args:
            name: Password name
            username: Username associated with password
            password: The actual password
            url: URL/website
            notes: Additional notes
        """
        self.name_row.set_subtitle(name)
        self.username_row.set_subtitle(username or "—")
        self.password_row.set_text(password)
        self.url_row.set_subtitle(url or "—")
        self.notes_label.set_text(notes or "No notes")

    def clear(self):
        """Clear all displayed password data."""
        self.set_password_data("", "", "", "", "")
