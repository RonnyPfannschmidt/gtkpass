"""The rename dialog: where an entry is moving to, and what it refuses.

Renaming and moving are the same operation -- an entry's name *is* its path --
so one dialog does both, and the only thing it collects is the new path. It
writes nothing itself: it emits ``renamed`` and the window puts it through the
backend, as the add and edit dialogs do.
"""

import pytest

from gtkpass._gi import Adw
from gtkpass.ui.password_rename import PasswordRenameDialog

pytestmark = pytest.mark.gui


@pytest.fixture(scope="session", autouse=True)
def adwaita():
    """Initialise libadwaita once; widget construction needs it."""
    Adw.init()


@pytest.fixture
def dialog():
    return PasswordRenameDialog()


def offered(dialog, current="email/work", taken=("email/work", "email/home")):
    dialog.offer(current_name=current, taken=set(taken), store_name="My Vault")
    return dialog


def renames(dialog):
    seen: list[str] = []
    dialog.connect("renamed", lambda _dialog, new_name: seen.append(new_name))
    return seen


class TestPrefill:
    def test_the_current_name_is_offered_to_be_edited(self, dialog):
        offered(dialog)

        assert dialog.name_row.get_text() == "email/work"

    def test_the_store_it_stays_in_is_named(self, dialog):
        """A move goes nowhere else: crossing stores is not this operation."""
        offered(dialog)

        assert "My Vault" in dialog.store_row.get_subtitle()


class TestTheNameItHandsBack:
    def test_empty_segments_are_dropped(self, dialog):
        offered(dialog)

        dialog.name_row.set_text("/work//email/")

        assert dialog.name == "work/email"

    def test_surrounding_whitespace_does_not_become_a_folder(self, dialog):
        offered(dialog)

        dialog.name_row.set_text("  email/work2  ")

        assert dialog.name == "email/work2"


class TestRenaming:
    def test_a_new_name_is_handed_over(self, dialog):
        offered(dialog)
        seen = renames(dialog)

        dialog.name_row.set_text("email/work-old")
        dialog.rename_button.emit("clicked")

        assert seen == ["email/work-old"]

    def test_moving_into_a_folder_is_the_same_operation(self, dialog):
        offered(dialog)
        seen = renames(dialog)

        dialog.name_row.set_text("archive/2019/email/work")
        dialog.rename_button.emit("clicked")

        assert seen == ["archive/2019/email/work"]

    def test_cancelling_hands_over_nothing(self, dialog):
        offered(dialog)
        seen = renames(dialog)

        dialog.cancel_button.emit("clicked")

        assert seen == []

    def test_an_empty_name_is_refused(self, dialog):
        offered(dialog)
        seen = renames(dialog)

        dialog.name_row.set_text("   ")
        dialog.rename_button.emit("clicked")

        assert seen == []

    def test_a_name_already_in_the_store_is_refused(self, dialog):
        """The backend would raise FileExistsError; say so before the round trip."""
        offered(dialog)
        seen = renames(dialog)

        dialog.name_row.set_text("email/home")
        dialog.rename_button.emit("clicked")

        assert seen == []
        assert dialog.name_row.has_css_class("error")

    def test_the_clash_is_reported_while_it_is_still_being_typed(self, dialog):
        offered(dialog)

        dialog.name_row.set_text("email/home")

        assert dialog.name_row.has_css_class("error")
        assert "already" in dialog.name_row.get_title()

    def test_typing_past_the_clash_clears_the_complaint(self, dialog):
        offered(dialog)

        dialog.name_row.set_text("email/home")
        dialog.name_row.set_text("email/home2")

        assert not dialog.name_row.has_css_class("error")

    def test_its_own_name_is_not_a_clash(self, dialog):
        """The entry being renamed is in the store, and is not in its own way."""
        offered(dialog)

        assert not dialog.name_row.has_css_class("error")

    def test_handing_back_its_own_name_does_nothing(self, dialog):
        """A rename to the same name is a no-op the backend need never see."""
        offered(dialog)
        seen = renames(dialog)

        dialog.rename_button.emit("clicked")

        assert seen == []
