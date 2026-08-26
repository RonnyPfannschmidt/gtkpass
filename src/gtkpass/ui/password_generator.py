"""The generator rows, shared by every dialog that offers to make a password.

Adding an entry, editing one and rotating one all offer the same choice, and
three copies of a choice drift until two of them are wrong. So there is one
widget, and it collects a :class:`~gtkpass.utils.generate.Recipe`.

Nothing about the schemes is written here. The list, the bounds on the size and
the entropy figure all come from ``gtkpass.utils.generate``: a scheme added
there appears here without this file being touched, which is the only way two
definitions stay one.
"""

import importlib.resources
from typing import ClassVar

from gtkpass._gi import Adw, GObject, Gtk
from gtkpass.utils.generate import Recipe, Scheme


@Gtk.Template(
    filename=str(
        importlib.resources.files("gtkpass.ui.blueprints") / "password_generator.ui"
    )
)
class PasswordGeneratorGroup(Adw.PreferencesGroup):
    """Chooses how a password is to be made, and makes one when asked."""

    __gtype_name__ = "PasswordGeneratorGroup"

    __gsignals__: ClassVar[dict] = {
        # (the generated value)
        "generated": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    scheme_row: Adw.ComboRow = Gtk.Template.Child()
    size_row: Adw.SpinRow = Gtk.Template.Child()
    symbols_row: Adw.SwitchRow = Gtk.Template.Child()
    generate_button: Gtk.Button = Gtk.Template.Child()

    #: The schemes in the order the combo row offers them, fixed once so that
    #: the selected index and the enum agree in both directions.
    SCHEMES: ClassVar[list[Scheme]] = list(Scheme)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        names = Gtk.StringList()
        for scheme in self.SCHEMES:
            names.append(scheme.title)
        self.scheme_row.set_model(names)

        #: Set while the scheme's own rows are being rewritten, so that the
        #: notify handlers those writes fire do not each recompute the entropy
        #: off a half-changed state.
        self._retuning = False

        self._retune(self.scheme)

    # -- what has been chosen ------------------------------------------------

    @property
    def scheme(self) -> Scheme:
        """The scheme the combo row is on."""
        selected = self.scheme_row.get_selected()
        if 0 <= selected < len(self.SCHEMES):
            return self.SCHEMES[selected]
        return self.SCHEMES[0]

    @property
    def recipe(self) -> Recipe:
        """Everything needed to generate, as one value to hand around."""
        return Recipe(
            scheme=self.scheme,
            size=int(self.size_row.get_value()),
            symbols=self.symbols_row.get_active(),
        )

    def generate(self) -> str:
        """A value made to the recipe on offer."""
        return self.recipe.generate()

    # -- keeping the rows in step with the scheme ----------------------------

    def _retune(self, scheme: Scheme) -> None:
        """Point the size row at what this scheme counts.

        The adjustment is moved rather than replaced, and the bounds go up
        before the value does: setting a value first would have it clamped
        against the *old* upper bound on the way through -- 20 characters
        becoming 12 words, and then being clamped again to something nobody
        chose.
        """
        self._retuning = True
        try:
            bounds = scheme.bounds
            adjustment = self.size_row.get_adjustment()
            # Widen first in both directions, so neither bound clips the value
            # while the other is still where it was.
            adjustment.set_lower(min(bounds.lower, adjustment.get_lower()))
            adjustment.set_upper(max(bounds.upper, adjustment.get_upper()))
            adjustment.set_value(bounds.default)
            adjustment.set_lower(bounds.lower)
            adjustment.set_upper(bounds.upper)

            self.size_row.set_title(scheme.size_title)
            # Only the character scheme has punctuation to allow. Hidden rather
            # than insensitive: a switch that cannot be moved still reads as an
            # option this scheme has.
            self.symbols_row.set_visible(scheme is Scheme.CHARACTERS)
        finally:
            self._retuning = False
        self._show_entropy()

    def _show_entropy(self) -> None:
        """Say how much guessing this recipe costs.

        The group's description, because it describes the whole group: the
        figure is a property of the scheme and the size together, and putting
        it on either row alone would attribute it to one of them.

        Rounded to whole bits. The fraction is real and nobody needs it, and a
        description that changes in its second decimal as a spin row is held
        down is a description nobody reads.
        """
        self.set_description(f"About {round(self.recipe.entropy_bits)} bits of entropy")

    @Gtk.Template.Callback()
    def _on_scheme_changed(self, *_args) -> None:
        self._retune(self.scheme)

    @Gtk.Template.Callback()
    def _on_size_changed(self, *_args) -> None:
        if self._retuning:
            return
        self._show_entropy()

    @Gtk.Template.Callback()
    def _on_generate(self, _button) -> None:
        self.emit("generated", self.generate())
