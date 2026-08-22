"""Dialog for renaming or moving one password entry.

The same operation under two names. An entry is identified by its path, so
changing "email/work" to "email/work-old" and changing it to
"archive/email/work" are the same write -- ``move_password`` -- and asking for
either one means collecting one string.

Nothing here writes anything: the dialog emits ``renamed`` and the window
decides which backend to put it through and how to report a failure, which is
what the add and edit dialogs do as well.
"""

import importlib.resources
from typing import ClassVar

from gtkpass._gi import Adw, GObject, Gtk


def tidy_path(text: str) -> str:
    """An entry path with its empty segments dropped.

    A leading slash, a doubled one and a trailing one all mean nothing in a
    store, and the backends would take them literally: `pass mv` given
    ``email//work`` makes a folder with an empty name. The add dialog does the
    same to what it collects, and the two have to agree, because a name typed
    into one is compared against names the other made.
    """
    return "/".join(part for part in text.strip().split("/") if part.strip())


@Gtk.Template(
    filename=str(
        importlib.resources.files("gtkpass.ui.blueprints") / "password_rename.ui"
    )
)
class PasswordRenameDialog(Adw.Dialog):
    """Collects the path an entry is to move to, and emits it."""

    __gtype_name__ = "PasswordRenameDialog"

    __gsignals__: ClassVar[dict] = {
        # (the new entry name)
        "renamed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    store_row: Adw.ActionRow = Gtk.Template.Child()
    name_row: Adw.EntryRow = Gtk.Template.Child()
    cancel_button: Gtk.Button = Gtk.Template.Child()
    rename_button: Gtk.Button = Gtk.Template.Child()

    #: As in the add dialog: an Adw.EntryRow has no subtitle to report a clash
    #: in, and a label that appeared and disappeared would shift the rows under
    #: it as the user types.
    NAME_TITLE = "Name"
    NAME_TAKEN = "Name (an entry of this name is already there)"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #: What the entry is called now, so that it is not treated as being in
        #: its own way and so that renaming to it can be recognised as a no-op.
        self._current_name = ""
        #: Every other name the store holds.
        self._taken: set[str] = set()

    def offer(self, current_name: str, taken: set[str], store_name: str) -> None:
        """Say what is being renamed, and what it may not be renamed to.

        Args:
            current_name: The entry's path today.
            taken: Every entry name in the store, this one included -- it is
                removed here rather than at every call site.
            store_name: The backend's display name, shown because the move
                stays inside it.
        """
        self._current_name = current_name
        self._taken = set(taken) - {current_name}

        self.store_row.set_subtitle(store_name)
        self.name_row.set_text(current_name)
        self._validate_name()

        # After the text, so the caret lands at the end of it rather than
        # selecting the whole path -- the common edit is to the last segment.
        self.name_row.grab_focus()
        self.name_row.select_region(-1, -1)

    @property
    def name(self) -> str:
        """The path the entry is to move to, with its slashes tidied."""
        return tidy_path(self.name_row.get_text())

    @Gtk.Template.Callback()
    def _on_name_changed(self, *_args) -> None:
        """Say that a name is already taken while it is still being typed."""
        self._validate_name()

    def _validate_name(self) -> bool:
        taken = bool(self.name) and self.name in self._taken
        if taken:
            self.name_row.add_css_class("error")
            self.name_row.set_title(self.NAME_TAKEN)
        else:
            self.name_row.remove_css_class("error")
            self.name_row.set_title(self.NAME_TITLE)
        return not taken

    @Gtk.Template.Callback()
    def _on_rename(self, _widget) -> None:
        """Refuse what a backend would refuse, before it costs a round trip."""
        if not self.name:
            self.name_row.grab_focus()
            return
        if not self._validate_name():
            self.name_row.grab_focus()
            return
        if self.name == self._current_name:
            # Not an error: somebody opened the dialog and changed their mind,
            # and a move onto itself is a write with nothing to write.
            self.close()
            return

        self.emit("renamed", self.name)
        self.close()

    @Gtk.Template.Callback()
    def _on_cancel(self, _button) -> None:
        self.close()
