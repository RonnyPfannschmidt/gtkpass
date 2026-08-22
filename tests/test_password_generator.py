"""The generator rows, which three dialogs share.

Adding, editing and rotating all offer the same choice, so they offer the same
widget rather than three copies of it that drift. What it collects is a
:class:`~gtkpass.utils.generate.Recipe`; what it hands back is a generated
value.
"""

import pytest

from gtkpass._gi import Adw
from gtkpass.ui.password_generator import PasswordGeneratorGroup
from gtkpass.utils.generate import DEFAULT_LENGTH, Scheme

pytestmark = pytest.mark.gui


@pytest.fixture(scope="session", autouse=True)
def adwaita():
    """Initialise libadwaita once; widget construction needs it."""
    Adw.init()


@pytest.fixture
def group():
    return PasswordGeneratorGroup()


def choose(group, scheme: Scheme) -> None:
    """Pick a scheme the way the combo row would."""
    group.scheme_row.set_selected(list(Scheme).index(scheme))


class TestTheSchemeOnOffer:
    def test_every_scheme_is_offered(self, group):
        model = group.scheme_row.get_model()

        assert model.get_n_items() == len(list(Scheme))

    def test_each_one_is_offered_under_its_own_name(self, group):
        model = group.scheme_row.get_model()
        offered = [model.get_string(index) for index in range(model.get_n_items())]

        assert offered == [scheme.title for scheme in Scheme]

    def test_it_starts_on_characters(self, group):
        """What `pass generate` makes, and what the dialog made before this."""
        assert group.recipe.scheme is Scheme.CHARACTERS

    def test_choosing_one_is_what_the_recipe_says(self, group):
        choose(group, Scheme.PASSPHRASE)

        assert group.recipe.scheme is Scheme.PASSPHRASE


class TestTheSizeFollowsTheScheme:
    """Twelve words is not twelve characters, so the number cannot carry over."""

    def test_it_starts_at_the_character_default(self, group):
        assert group.recipe.resolved_size == DEFAULT_LENGTH

    def test_switching_scheme_moves_to_that_scheme_s_default(self, group):
        choose(group, Scheme.PASSPHRASE)

        assert group.recipe.resolved_size == Scheme.PASSPHRASE.bounds.default

    def test_switching_scheme_moves_the_bounds(self, group):
        choose(group, Scheme.DIGITS)
        adjustment = group.size_row.get_adjustment()

        assert adjustment.get_lower() == Scheme.DIGITS.bounds.lower
        assert adjustment.get_upper() == Scheme.DIGITS.bounds.upper

    def test_the_row_says_what_it_is_counting(self, group):
        choose(group, Scheme.PASSPHRASE)

        assert group.size_row.get_title() == Scheme.PASSPHRASE.size_title

    def test_a_size_that_was_chosen_is_kept(self, group):
        group.size_row.set_value(32)

        assert group.recipe.resolved_size == 32

    def test_a_size_out_of_range_for_the_new_scheme_cannot_survive(self, group):
        """The spin row clamps, so the recipe can never be ungeneratable."""
        group.size_row.set_value(120)
        choose(group, Scheme.PASSPHRASE)

        assert group.recipe.resolved_size <= Scheme.PASSPHRASE.bounds.upper


class TestSymbols:
    """Only one scheme has punctuation to allow, so only one offers the switch."""

    def test_the_switch_is_there_for_characters(self, group):
        assert group.symbols_row.get_visible()

    def test_it_goes_away_for_a_passphrase(self, group):
        choose(group, Scheme.PASSPHRASE)

        assert not group.symbols_row.get_visible()

    def test_it_goes_away_for_a_pin(self, group):
        choose(group, Scheme.DIGITS)

        assert not group.symbols_row.get_visible()

    def test_turning_it_off_is_what_the_recipe_says(self, group):
        group.symbols_row.set_active(False)

        assert group.recipe.symbols is False


class TestTheEntropyItReports:
    """The only way to compare twenty characters with six words."""

    def test_it_is_shown(self, group):
        assert "bits" in group.get_description()

    def test_it_follows_the_size(self, group):
        group.size_row.set_value(8)
        short = group.get_description()
        group.size_row.set_value(64)

        assert group.get_description() != short

    def test_it_follows_the_scheme(self, group):
        before = group.get_description()
        choose(group, Scheme.DIGITS)

        assert group.get_description() != before

    def test_it_is_the_recipe_s_own_figure(self, group):
        expected = round(group.recipe.entropy_bits)

        assert str(expected) in group.get_description()


class TestGenerating:
    def test_it_generates_by_the_scheme_on_offer(self, group):
        choose(group, Scheme.DIGITS)

        assert group.generate().isdigit()

    def test_the_value_is_handed_to_whoever_asked(self, group):
        seen: list[str] = []
        group.connect("generated", lambda _group, value: seen.append(value))

        group.generate_button.emit("clicked")

        assert len(seen) == 1
        assert seen[0]

    def test_the_button_generates_by_the_scheme_on_offer(self, group):
        seen: list[str] = []
        group.connect("generated", lambda _group, value: seen.append(value))
        choose(group, Scheme.PASSPHRASE)

        group.generate_button.emit("clicked")

        assert len(seen[0].split("-")) == Scheme.PASSPHRASE.bounds.default
