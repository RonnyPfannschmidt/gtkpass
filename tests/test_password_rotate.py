"""The rotation wizard: replacing a password without losing the account.

Rotating is the operation people reach for most often after reading an entry,
and doing it through the editor gets the order wrong. The editor writes the
store first, and the site second -- so if the site refuses the new password
(too long, no symbols, a change form that fails) the store now holds a password
the site does not, and the account is only reachable through a reset.

So the wizard puts the store last. It makes the new value, hands it over to be
pasted into the site, asks whether that worked, and only then writes. Until it
writes, the store still holds the password that works, and the wizard keeps
that one available to be copied.
"""

from pathlib import Path

import pytest

from gtkpass._gi import Adw
from gtkpass.backends import PasswordEntry
from gtkpass.ui.password_rotate import PasswordRotateDialog

pytestmark = pytest.mark.gui

CURRENT = "the-password-that-works"


@pytest.fixture(scope="session", autouse=True)
def adwaita():
    """Initialise libadwaita once; widget construction needs it."""
    Adw.init()


def entry(content: str, name: str = "email/work") -> PasswordEntry:
    return PasswordEntry(name=name, path=Path(f"/store/{name}.gpg"), content=content)


FULL = (
    f"{CURRENT}\n"
    "username: alice@example.invalid\n"
    "url: https://example.invalid/account\n"
    "note: the recovery codes are in the safe\n"
)


@pytest.fixture
def dialog():
    return PasswordRotateDialog()


@pytest.fixture
def loaded(dialog):
    dialog.load(entry(FULL), store_name="My Vault")
    return dialog


def rotations(dialog):
    seen: list[str] = []
    dialog.connect("rotated", lambda _dialog, content: seen.append(content))
    return seen


class TestWhatItStartsWith:
    def test_it_opens_on_the_page_that_makes_the_new_password(self, loaded):
        assert loaded.navigation.get_visible_page().get_tag() == "new"

    def test_the_entry_is_named(self, loaded):
        """ "Rotate this password" is a question nobody can answer."""
        assert loaded.entry_row.get_title() == "email/work"

    def test_the_store_it_is_in_is_named(self, loaded):
        assert "My Vault" in (loaded.entry_row.get_subtitle() or "")

    def test_the_password_that_works_is_still_reachable(self, loaded):
        """Until the write lands it is the only one that opens the account."""
        assert loaded.current_row.get_text() == CURRENT

    def test_a_replacement_is_generated_without_being_asked(self, loaded):
        """Nobody opens this wizard not wanting a new password."""
        assert loaded.new_row.get_text()
        assert loaded.new_row.get_text() != CURRENT

    def test_generating_again_replaces_it(self, loaded):
        first = loaded.new_row.get_text()

        loaded.generator.generate_button.emit("clicked")

        assert loaded.new_row.get_text() != first

    def test_the_scheme_on_offer_is_the_one_used(self, loaded):
        from gtkpass.utils.generate import Scheme

        loaded.generator.scheme_row.set_selected(
            loaded.generator.SCHEMES.index(Scheme.DIGITS)
        )
        loaded.generator.generate_button.emit("clicked")

        assert loaded.new_row.get_text().isdigit()

    def test_a_password_can_be_typed_instead(self, loaded):
        """A site with rules the generator does not know about."""
        loaded.new_row.set_text("chosen-by-hand")

        assert loaded.content.startswith("chosen-by-hand\n")


class TestGoingForward:
    def test_it_moves_to_the_page_about_the_site(self, loaded):
        loaded.to_site_button.emit("clicked")

        assert loaded.navigation.get_visible_page().get_tag() == "site"

    def test_an_empty_replacement_goes_nowhere(self, loaded):
        loaded.new_row.set_text("")

        loaded.to_site_button.emit("clicked")

        assert loaded.navigation.get_visible_page().get_tag() == "new"

    def test_a_replacement_that_is_the_old_one_goes_nowhere(self, loaded):
        """Rotating to the same value is not a rotation."""
        loaded.new_row.set_text(CURRENT)

        loaded.to_site_button.emit("clicked")

        assert loaded.navigation.get_visible_page().get_tag() == "new"

    def test_the_site_page_leads_to_the_question(self, loaded):
        loaded.to_site_button.emit("clicked")
        loaded.to_confirm_button.emit("clicked")

        assert loaded.navigation.get_visible_page().get_tag() == "confirm"

    def test_going_back_is_possible_the_whole_way(self, loaded):
        """The site refused it, and the old password has to be reachable again."""
        loaded.to_site_button.emit("clicked")
        loaded.to_confirm_button.emit("clicked")

        loaded.navigation.pop()
        loaded.navigation.pop()

        assert loaded.navigation.get_visible_page().get_tag() == "new"
        assert loaded.current_row.get_text() == CURRENT


class TestWhatTheSitePageOffers:
    def test_the_url_from_the_entry_is_shown(self, loaded):
        loaded.to_site_button.emit("clicked")

        assert loaded.url_row.get_visible()
        assert loaded.url_row.get_subtitle() == "https://example.invalid/account"

    def test_the_username_from_the_entry_is_shown(self, loaded):
        loaded.to_site_button.emit("clicked")

        assert loaded.username_row.get_visible()
        assert loaded.username_row.get_subtitle() == "alice@example.invalid"

    def test_an_entry_without_a_url_does_not_show_an_empty_row(self, dialog):
        dialog.load(entry(f"{CURRENT}\nusername: alice\n"), store_name="My Vault")

        dialog.to_site_button.emit("clicked")

        assert not dialog.url_row.get_visible()

    def test_an_entry_without_a_username_does_not_show_an_empty_row(self, dialog):
        dialog.load(entry(f"{CURRENT}\n"), store_name="My Vault")

        dialog.to_site_button.emit("clicked")

        assert not dialog.username_row.get_visible()


class TestOpeningTheSite:
    """One click that launches a URL is wider than the button says it is.

    An entry's ``url:`` line is whatever its owner wrote, and a synced store
    carries whatever another machine wrote. The value is always shown and
    always selectable; what is withheld for anything but http and https is the
    button that hands it to the desktop.
    """

    def opened(self, dialog):
        dialog.to_site_button.emit("clicked")
        return dialog.open_url_button.get_visible()

    def test_an_https_site_is_offered(self, loaded):
        assert self.opened(loaded) is True

    def test_a_plain_http_site_is_offered(self, dialog):
        dialog.load(entry(f"{CURRENT}\nurl: http://example.invalid/\n"), store_name="V")

        assert self.opened(dialog) is True

    @pytest.mark.parametrize(
        "url",
        [
            "file:///etc/passwd",
            "smb://server/share",
            "mailto:someone@example.invalid",
            "javascript:alert(1)",
            "example.invalid/no-scheme",
        ],
    )
    def test_anything_else_is_shown_but_not_launchable(self, dialog, url):
        dialog.load(entry(f"{CURRENT}\nurl: {url}\n"), store_name="V")
        dialog.to_site_button.emit("clicked")

        assert dialog.url_row.get_visible()
        assert dialog.url_row.get_subtitle() == url
        assert dialog.open_url_button.get_visible() is False


class TestCopying:
    """The wizard does not touch the clipboard: the window owns that.

    Copies made here have to be cleared on the same timer and marked the same
    way as every other copy, and a second clipboard owner in the application
    would leave a secret behind that nothing takes back.
    """

    def copies(self, dialog):
        seen: list[tuple[str, str]] = []
        dialog.connect(
            "copy-requested",
            lambda _dialog, field, value: seen.append((field, value)),
        )
        return seen

    def test_the_new_password_can_be_copied(self, loaded):
        seen = self.copies(loaded)

        loaded.copy_new_button.emit("clicked")

        assert seen == [("Password", loaded.new_row.get_text())]

    def test_the_old_password_can_be_copied(self, loaded):
        """The site's change form asks for the current one first."""
        seen = self.copies(loaded)

        loaded.copy_current_button.emit("clicked")

        assert seen == [("Password", CURRENT)]

    def test_the_username_can_be_copied(self, loaded):
        seen = self.copies(loaded)
        loaded.to_site_button.emit("clicked")

        loaded.copy_username_button.emit("clicked")

        assert seen == [("Username", "alice@example.invalid")]


class TestWritingItDown:
    def test_confirming_hands_over_the_new_entry(self, loaded):
        seen = rotations(loaded)
        loaded.new_row.set_text("the-new-one")
        loaded.to_site_button.emit("clicked")
        loaded.to_confirm_button.emit("clicked")

        loaded.save_button.emit("clicked")

        assert seen == [FULL.replace(CURRENT, "the-new-one", 1)]

    def test_everything_below_the_password_survives(self, loaded):
        """The reason to rotate rather than delete and add again."""
        seen = rotations(loaded)
        loaded.new_row.set_text("the-new-one")
        loaded.to_site_button.emit("clicked")
        loaded.to_confirm_button.emit("clicked")

        loaded.save_button.emit("clicked")

        assert "note: the recovery codes are in the safe" in seen[0]
        assert "username: alice@example.invalid" in seen[0]

    def test_cancelling_writes_nothing(self, loaded):
        seen = rotations(loaded)

        loaded.cancel_button.emit("clicked")

        assert seen == []

    def test_cancelling_from_the_last_page_writes_nothing(self, loaded):
        """Where somebody lands when the site refused the new password."""
        seen = rotations(loaded)
        loaded.to_site_button.emit("clicked")
        loaded.to_confirm_button.emit("clicked")

        loaded.cancel_button.emit("clicked")

        assert seen == []

    def test_nothing_is_written_before_the_last_page(self, loaded):
        """The whole point: the store is last, so the site can still refuse."""
        seen = rotations(loaded)

        loaded.to_site_button.emit("clicked")

        assert seen == []


class TestAnEntryThatNeverDecrypted:
    """The pane can hand over an entry with no content; do not offer a wizard
    that would write an entry consisting of a password and nothing else."""

    def test_it_reports_that_there_is_nothing_to_rotate(self, dialog):
        assert dialog.load(entry(""), store_name="My Vault") is False

    def test_a_loaded_entry_is_accepted(self, dialog):
        assert dialog.load(entry(FULL), store_name="My Vault") is True
