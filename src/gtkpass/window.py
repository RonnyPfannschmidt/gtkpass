"""Main application window."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, Gtk  # noqa: E402


@Gtk.Template(filename="src/gtkpass/ui/blueprints/window.ui")
class GTKPassWindow(Adw.ApplicationWindow):
    """Main application window for GTKPass.

    UI is defined in ui/blueprints/window.blp and compiled to window.ui.

    This window provides the main password manager interface with:
    - A sidebar for the password list
    - A detail pane for viewing selected password
    - Search functionality
    - Add password button
    """

    __gtype_name__ = "GTKPassWindow"

    # Template children
    split_view = Gtk.Template.Child()
    password_list = Gtk.Template.Child()
    search_entry = Gtk.Template.Child()
    placeholder_page = Gtk.Template.Child()

    def __init__(self, **kwargs):
        """Initialize the main window."""
        super().__init__(**kwargs)
        self._setup_actions()
        self._setup_password_list()

    def _setup_actions(self):
        """Set up window actions."""
        # Add password action
        add_action = Gio.SimpleAction.new("add-password", None)
        add_action.connect("activate", self._on_add_password)
        self.add_action(add_action)

    def _setup_password_list(self):
        """Set up the password list with placeholder data."""
        # Add placeholder rows to demonstrate the UI
        # In a real implementation, these would come from the password store
        placeholder_passwords = [
            ("GitHub", "github.com/username"),
            ("Email", "user@example.com"),
            ("Bank", "mybank.com"),
            ("Social Media", "social.example.com"),
        ]

        for name, detail in placeholder_passwords:
            row = Adw.ActionRow(
                title=name,
                subtitle=detail,
            )
            row.add_suffix(Gtk.Image.new_from_icon_name("go-next-symbolic"))
            self.password_list.append(row)

        # Connect selection handler
        self.password_list.connect("row-selected", self._on_password_selected)

    def _on_add_password(self, action, param):
        """Handle add password button click."""
        # Placeholder - will be implemented in future
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="Add Password",
            body="Password creation UI will be implemented in the next phase.",
        )
        dialog.add_response("ok", "OK")
        dialog.present()

    def _on_password_selected(self, listbox, row):
        """Handle password selection from the list."""
        if row is None:
            return

        # Placeholder - will show actual password details in future
        # For now, just demonstrate the interaction
        # This is where we would show the detail view
        pass
