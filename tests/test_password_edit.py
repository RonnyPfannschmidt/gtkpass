"""The edit dialog: what it shows, and what it hands back to be saved.

Entries are stored as free text -- the password on the first line, arbitrary
lines after it -- so the dialog splits on that boundary and joins it back. It
must not lose or reorder anything it did not touch, because whatever it hands
over replaces the entry wholesale.
"""

import pytest

from gtkpass._gi import Adw
from gtkpass.backends import PasswordEntry
from gtkpass.ui.password_edit import PasswordEditDialog

pytestmark = pytest.mark.gui

SECRET = "correct-horse-battery-staple"


@pytest.fixture(scope="session", autouse=True)
def adwaita():
    """Initialise libadwaita once; widget construction needs it."""
    Adw.init()


def entry(content: str) -> PasswordEntry:
    from pathlib import Path

    return PasswordEntry(
        name="email/work", path=Path("/store/email/work.gpg"), content=content
    )


@pytest.fixture
def dialog():
    return PasswordEditDialog()


def details(dialog) -> str:
    buffer = dialog.details_view.get_buffer()
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)


def set_details(dialog, text: str) -> None:
    dialog.details_view.get_buffer().set_text(text)


class TestPrefill:
    def test_the_entry_name_is_shown(self, dialog):
        dialog.load(entry(f"{SECRET}\n"))

        assert dialog.name_row.get_subtitle() == "email/work"

    def test_the_password_is_the_first_line(self, dialog):
        dialog.load(entry(f"{SECRET}\nusername: alice\n"))

        assert dialog.password_row.get_text() == SECRET

    def test_the_remaining_lines_become_the_details(self, dialog):
        dialog.load(entry(f"{SECRET}\nusername: alice\nurl: example.invalid\n"))

        assert details(dialog) == "username: alice\nurl: example.invalid\n"

    def test_an_entry_with_no_details_leaves_them_empty(self, dialog):
        dialog.load(entry(f"{SECRET}\n"))

        assert details(dialog) == ""

    def test_an_entry_that_never_loaded_shows_nothing(self, dialog):
        dialog.load(entry(""))

        assert dialog.password_row.get_text() == ""
        assert details(dialog) == ""


class TestAssembly:
    def test_an_untouched_entry_round_trips(self, dialog):
        original = f"{SECRET}\nusername: alice\nurl: example.invalid\n"
        dialog.load(entry(original))

        assert dialog.content == original

    def test_a_new_password_replaces_only_the_first_line(self, dialog):
        dialog.load(entry(f"{SECRET}\nusername: alice\n"))

        dialog.password_row.set_text("replaced")

        assert dialog.content == "replaced\nusername: alice\n"

    def test_new_details_replace_everything_after_it(self, dialog):
        dialog.load(entry(f"{SECRET}\nusername: alice\n"))

        set_details(dialog, "username: bob\n")

        assert dialog.content == f"{SECRET}\nusername: bob\n"

    def test_an_entry_without_a_trailing_newline_gains_one(self, dialog):
        """Stores conventionally end an entry with a newline; normalise to it."""
        dialog.load(entry(SECRET))

        assert dialog.content == f"{SECRET}\n"


class TestSaving:
    def saved_content(self, dialog):
        seen = []
        dialog.connect("saved", lambda _dialog, content: seen.append(content))
        return seen

    def test_saving_hands_over_the_edited_content(self, dialog):
        dialog.load(entry(f"{SECRET}\nusername: alice\n"))
        seen = self.saved_content(dialog)

        dialog.password_row.set_text("replaced")
        dialog.save_button.emit("clicked")

        assert seen == ["replaced\nusername: alice\n"]

    def test_cancelling_hands_over_nothing(self, dialog):
        dialog.load(entry(f"{SECRET}\n"))
        seen = self.saved_content(dialog)

        dialog.cancel_button.emit("clicked")

        assert seen == []

    def test_an_empty_password_cannot_be_saved(self, dialog):
        """An empty first line would leave an entry with no password at all."""
        dialog.load(entry(f"{SECRET}\n"))
        seen = self.saved_content(dialog)

        dialog.password_row.set_text("")
        dialog.save_button.emit("clicked")

        assert seen == []


class TestGeneratingAReplacement:
    """The generator was in the add dialog only, which is the wrong half.

    Adding an entry is the one time a password is *not* being replaced. Every
    rotation goes through here, and it went through here with nothing but an
    empty field to type into -- so the strongest thing the application can make
    was unavailable at exactly the moment it was wanted.
    """

    def test_the_generator_is_offered(self, dialog):
        dialog.load(entry(f"{SECRET}\n"))

        assert dialog.generator.get_visible()

    def test_generating_replaces_the_password(self, dialog):
        dialog.load(entry(f"{SECRET}\nusername: alice\n"))

        dialog.generator.generate_button.emit("clicked")

        assert dialog.password_row.get_text() != SECRET
        assert dialog.password_row.get_text()

    def test_generating_leaves_everything_below_it_alone(self, dialog):
        """The whole point of rotating rather than deleting and re-adding."""
        dialog.load(entry(f"{SECRET}\nusername: alice\nurl: example.invalid\n"))

        dialog.generator.generate_button.emit("clicked")

        assert details(dialog) == "username: alice\nurl: example.invalid\n"

    def test_the_scheme_on_offer_is_the_one_used(self, dialog):
        from gtkpass.utils.generate import Scheme

        dialog.load(entry(f"{SECRET}\n"))
        dialog.generator.scheme_row.set_selected(
            dialog.generator.SCHEMES.index(Scheme.DIGITS)
        )

        dialog.generator.generate_button.emit("clicked")

        assert dialog.password_row.get_text().isdigit()

    def test_a_generated_password_is_shown_rather_than_dotted_out(self, dialog):
        """Somebody who has just generated one has not seen it yet."""
        dialog.load(entry(f"{SECRET}\n"))

        dialog.generator.generate_button.emit("clicked")

        assert dialog.password_row.get_delegate().get_visibility() is True

    def test_it_is_the_generated_value_that_gets_saved(self, dialog):
        dialog.load(entry(f"{SECRET}\nusername: alice\n"))
        seen: list[str] = []
        dialog.connect("saved", lambda _dialog, content: seen.append(content))

        dialog.generator.generate_button.emit("clicked")
        generated = dialog.password_row.get_text()
        dialog.save_button.emit("clicked")

        assert seen == [f"{generated}\nusername: alice\n"]
