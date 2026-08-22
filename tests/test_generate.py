"""Generating a password.

Short enough to be obviously right, and the one place it matters that it is:
this is `secrets` and nothing else, because a generator seeded from the clock
or drawn from `random` produces passwords somebody can reproduce.
"""

import pytest

from gtkpass.utils.generate import ALPHABET, DEFAULT_LENGTH, generate_password


class TestLength:
    def test_the_default_is_long_enough_to_be_worth_generating(self):
        assert len(generate_password()) == DEFAULT_LENGTH
        assert DEFAULT_LENGTH >= 16

    def test_a_length_is_honoured(self):
        assert len(generate_password(length=32)) == 32

    def test_a_useless_length_is_refused(self):
        """Rather than quietly handing back something unusable."""
        with pytest.raises(ValueError):
            generate_password(length=0)


class TestAlphabet:
    def test_only_the_declared_characters_are_used(self):
        assert set(generate_password(length=200)) <= set(ALPHABET)

    def test_symbols_can_be_left_out(self):
        """Some sites still refuse them, and a refused password is a retype."""
        generated = generate_password(length=200, symbols=False)

        assert generated.isalnum()

    def test_ambiguous_characters_are_left_out(self):
        """A generated password gets read off a screen and typed on a phone.

        O and 0, l and 1 and I are the pairs that cost somebody three attempts
        before they think to try the other one.
        """
        assert not set("O0lI1") & set(ALPHABET)


class TestUnpredictability:
    def test_two_passwords_differ(self):
        assert generate_password() != generate_password()

    def test_it_draws_from_secrets(self, monkeypatch):
        """The module has to be the audited one, whatever it is called here.

        `random` is seeded from the clock and its state can be recovered from
        its output, which for a password generator is the whole ballgame.
        """
        import gtkpass.utils.generate as module

        calls = []

        def record(sequence):
            calls.append(sequence)
            return sequence[0]

        monkeypatch.setattr(module.secrets, "choice", record)

        generate_password(length=5)

        assert len(calls) == 5


class TestTheWordlist:
    """Diceware needs a list, and this one is the EFF large list verbatim.

    Verbatim matters: the whole value of a published wordlist is that somebody
    can check the copy against the original. A list quietly tidied -- the four
    hyphenated entries removed, say -- would still be 7776 lines and would no
    longer be the thing it says it is.
    """

    def test_it_is_the_size_five_dice_give(self):
        from gtkpass.utils.generate import WORDS

        assert len(WORDS) == 6**5

    def test_no_word_appears_twice(self):
        from gtkpass.utils.generate import WORDS

        assert len(set(WORDS)) == len(WORDS)

    def test_the_header_is_not_in_it(self):
        from gtkpass.utils.generate import WORDS

        assert not [word for word in WORDS if word.startswith("#")]
        assert not [word for word in WORDS if not word.strip()]

    def test_every_word_is_typeable(self):
        """Read off one screen and typed into another, as generated ones are."""
        from gtkpass.utils.generate import WORDS

        assert all(word.isascii() and word.islower() for word in WORDS)


class TestPassphrases:
    def test_it_hands_back_the_number_of_words_asked_for(self):
        from gtkpass.utils.generate import generate_passphrase

        assert len(generate_passphrase(words=5).split("-")) == 5

    def test_the_separator_is_the_one_asked_for(self):
        from gtkpass.utils.generate import generate_passphrase

        assert len(generate_passphrase(words=4, separator=".").split(".")) == 4

    def test_every_word_comes_from_the_list(self):
        from gtkpass.utils.generate import WORDS, generate_passphrase

        vocabulary = set(WORDS)
        for _ in range(20):
            assert set(generate_passphrase(words=6).split("-")) <= vocabulary

    def test_a_passphrase_of_no_words_is_refused(self):
        from gtkpass.utils.generate import generate_passphrase

        with pytest.raises(ValueError):
            generate_passphrase(words=0)

    def test_two_passphrases_differ(self):
        from gtkpass.utils.generate import generate_passphrase

        assert generate_passphrase() != generate_passphrase()

    def test_it_draws_from_secrets(self, monkeypatch):
        """Same reason as the character generator: `random` is reproducible."""
        import gtkpass.utils.generate as module
        from gtkpass.utils.generate import generate_passphrase

        calls = []

        def record(sequence):
            calls.append(sequence)
            return sequence[0]

        monkeypatch.setattr(module.secrets, "choice", record)

        generate_passphrase(words=4)

        assert len(calls) == 4

    def test_words_repeat_rather_than_being_drawn_without_replacement(
        self, monkeypatch
    ):
        """Each word must be an independent draw from the whole list.

        Removing a word once it is used makes the second draw one of 7775 and
        the third one of 7774, which is a smaller number than the entropy
        figure beside it claims -- and the interface shows that figure.
        """
        import gtkpass.utils.generate as module
        from gtkpass.utils.generate import generate_passphrase

        seen = []

        def record(sequence):
            seen.append(len(sequence))
            return sequence[0]

        monkeypatch.setattr(module.secrets, "choice", record)

        generate_passphrase(words=4)

        assert seen == [6**5] * 4


class TestDigits:
    """A PIN. Banks, SIM cards and phone locks take nothing else."""

    def test_it_is_the_length_asked_for(self):
        from gtkpass.utils.generate import generate_digits

        assert len(generate_digits(length=6)) == 6

    def test_it_is_nothing_but_digits(self):
        from gtkpass.utils.generate import generate_digits

        assert generate_digits(length=100).isdigit()

    def test_a_leading_zero_survives(self):
        """It is a string of digits, not a number, and 0421 is a valid PIN."""
        from gtkpass.utils.generate import generate_digits

        assert any(generate_digits(length=4).startswith("0") for _ in range(200))

    def test_a_useless_length_is_refused(self):
        from gtkpass.utils.generate import generate_digits

        with pytest.raises(ValueError):
            generate_digits(length=0)


class TestRecipes:
    """What the interface carries around: a scheme and the size it wants.

    One object rather than three call signatures, because the add dialog, the
    edit dialog and the rotation wizard all offer the same choice and all have
    to hand it somewhere.
    """

    def test_each_scheme_generates_something(self):
        from gtkpass.utils.generate import Recipe, Scheme

        for scheme in Scheme:
            assert Recipe(scheme).generate()

    def test_the_characters_scheme_honours_its_length(self):
        from gtkpass.utils.generate import Recipe, Scheme

        assert len(Recipe(Scheme.CHARACTERS, size=32).generate()) == 32

    def test_the_passphrase_scheme_counts_words_and_not_characters(self):
        from gtkpass.utils.generate import Recipe, Scheme

        generated = Recipe(Scheme.PASSPHRASE, size=5).generate()

        assert len(generated.split("-")) == 5

    def test_the_digits_scheme_honours_its_length(self):
        from gtkpass.utils.generate import Recipe, Scheme

        assert len(Recipe(Scheme.DIGITS, size=6).generate()) == 6

    def test_symbols_are_left_out_when_they_are_not_wanted(self):
        from gtkpass.utils.generate import Recipe, Scheme

        assert Recipe(Scheme.CHARACTERS, size=128, symbols=False).generate().isalnum()

    def test_a_default_size_is_offered_for_every_scheme(self):
        """A scheme the user switches to has to arrive at a usable size.

        Twenty words is not a passphrase and four characters is not a password,
        so the size cannot simply carry over from the scheme before it.
        """
        from gtkpass.utils.generate import Scheme

        for scheme in Scheme:
            assert scheme.bounds.lower <= scheme.bounds.default <= scheme.bounds.upper

    def test_a_size_outside_the_bounds_is_refused(self):
        from gtkpass.utils.generate import Recipe, Scheme

        with pytest.raises(ValueError):
            Recipe(Scheme.CHARACTERS, size=0).generate()


class TestEntropy:
    """The figure the interface shows beside the generated value.

    It is the only way somebody can compare a twenty-character password with a
    six-word passphrase, and getting it wrong would be worse than not showing
    it: it would talk somebody out of the stronger of the two.
    """

    def test_a_passphrase_is_five_dice_per_word(self):
        import math

        from gtkpass.utils.generate import Recipe, Scheme

        expected = 6 * math.log2(6**5)

        assert Recipe(Scheme.PASSPHRASE, size=6).entropy_bits == pytest.approx(expected)

    def test_a_character_password_counts_its_alphabet(self):
        import math

        from gtkpass.utils.generate import ALPHABET, Recipe, Scheme

        expected = 20 * math.log2(len(ALPHABET))

        assert Recipe(Scheme.CHARACTERS, size=20).entropy_bits == pytest.approx(
            expected
        )

    def test_dropping_symbols_costs_entropy(self):
        from gtkpass.utils.generate import Recipe, Scheme

        with_symbols = Recipe(Scheme.CHARACTERS, size=20).entropy_bits
        without = Recipe(Scheme.CHARACTERS, size=20, symbols=False).entropy_bits

        assert without < with_symbols

    def test_a_pin_counts_ten_per_digit(self):
        import math

        from gtkpass.utils.generate import Recipe, Scheme

        assert Recipe(Scheme.DIGITS, size=6).entropy_bits == pytest.approx(
            6 * math.log2(10)
        )

    def test_the_default_character_password_clears_a_hundred_bits(self):
        """What the module docstring has always claimed for it."""
        from gtkpass.utils.generate import Recipe, Scheme

        assert Recipe(Scheme.CHARACTERS).entropy_bits > 100
