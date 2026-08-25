"""Generating a password, by one of three schemes.

`secrets` rather than `random`: the latter is seeded from the clock and its
state is recoverable from its output, which for a password generator is the
whole of the matter. There is still no dependency here -- the wordlist is a
data file, not a package.

Three schemes rather than one, because one was a guess about what every entry
in a store is for:

- **Characters** is what `pass generate` makes, and what a site's password
  field wants.
- **A passphrase** is what somebody has to type on a phone, a games console or
  a television remote, and what a disk or a key passphrase has to be
  remembered as. Twenty random characters and six random words are within a few
  bits of each other, and only one of them can be read aloud.
- **Digits** is what a bank, a SIM card or a door lock takes, and nothing else
  will go in.

Which of the three is right is not something the application can work out, so
it asks, and shows the entropy of each so the answer can be compared rather
than guessed at.
"""

import importlib.resources
import math
import secrets
import string
from dataclasses import dataclass
from enum import Enum

#: Characters a generated password is drawn from.
#:
#: O and 0, and l, I and 1, are left out on purpose. A generated password gets
#: read off one screen and typed into another, often on a phone, and those two
#: pairs are what cost somebody three attempts before it occurs to them to try
#: the other character.
_AMBIGUOUS = "O0lI1"

LETTERS_AND_DIGITS = "".join(
    character
    for character in string.ascii_letters + string.digits
    if character not in _AMBIGUOUS
)

#: The symbols, kept to ones that survive a shell, a URL and a form field.
SYMBOLS = "!@#$%^&*-_=+?"

ALPHABET = LETTERS_AND_DIGITS + SYMBOLS

#: Long enough that the alphabet above carries well over 100 bits.
DEFAULT_LENGTH = 20

#: Digits, as a string, because a PIN is a string: 0421 is a valid one and
#: 421 is a different one.
DIGITS = string.digits

#: Words in a default passphrase.
#:
#: Six of the EFF list is a shade over 77 bits, which is the number that list
#: was chosen against. Five is 64 and is a passphrase for something that is
#: also behind a rate limit; seven is 90 and is a passphrase for a disk.
DEFAULT_WORDS = 6

#: Digits in a default PIN, which is what a bank card has.
DEFAULT_DIGITS = 6

#: What separates the words of a passphrase unless something says otherwise.
#:
#: A separator, and not nothing: "worlddesk" is two words or it is one longer
#: one, and a passphrase somebody has to retype is a passphrase they have to be
#: able to read.
DEFAULT_SEPARATOR = "-"

_WORDLIST = "eff_large_wordlist.txt"


def _load_words() -> tuple[str, ...]:
    """Read the wordlist, dropping the header and any word the separator splits.

    The EFF list has four hyphenated entries -- drop-down, felt-tip, t-shirt,
    yo-yo -- and the separator between words is a hyphen. Left in, a passphrase
    reading ``drop-down-anchor-zoom`` is three words that look like four: nobody
    reading it back can tell where the words are, and anything that splits on
    the separator to count them is wrong.

    So they are excluded here rather than removed from the file, which stays
    the published list byte for byte and can still be diffed against it. The
    cost is 7772 words instead of 7776, which is 0.0007 of a bit each -- against
    a passphrase somebody can actually read out.

    A tuple rather than a list: nothing may add a word to the vocabulary after
    the fact, and ``secrets.choice`` is happy with either.
    """
    text = (
        importlib.resources.files("gtkpass.utils.data")
        .joinpath(_WORDLIST)
        .read_text(encoding="utf-8")
    )
    words = (
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.startswith("#")
    )
    return tuple(word for word in words if DEFAULT_SEPARATOR not in word)


#: The vocabulary a passphrase is drawn from: the EFF large list, less the four
#: entries that contain the separator. See _load_words.
#:
#: Read at import rather than on first use. It is sixty kilobytes and one pass
#: over it, which is not worth the lazy accessor it would take to avoid, and
#: a wordlist that failed to load would otherwise do so at the moment somebody
#: clicked Generate rather than when the application started.
WORDS = _load_words()


@dataclass(frozen=True)
class Bounds:
    """What a scheme's size may be, and where it starts.

    Each scheme counts something different -- characters, words, digits -- so
    the number in the interface means something different for each, and
    carrying one scheme's number over to the next would offer twenty words or a
    four-character password.
    """

    lower: int
    upper: int
    default: int


class Scheme(Enum):
    """How a generated password is put together.

    The value is what a GSettings key or a serialized preference would hold, so
    it is a string rather than an ordinal: reordering this enum must not change
    what an existing setting means.
    """

    CHARACTERS = "characters"
    PASSPHRASE = "passphrase"
    DIGITS = "digits"

    @property
    def bounds(self) -> Bounds:
        """The sizes this scheme accepts."""
        return _BOUNDS[self]

    @property
    def title(self) -> str:
        """What the interface calls this scheme."""
        return _TITLES[self]

    @property
    def size_title(self) -> str:
        """What the interface calls this scheme's size, which is not a length."""
        return _SIZE_TITLES[self]


#: 8 is the shortest a site ever accepts and the shortest worth generating; 128
#: is past every field that exists. Three words is a passphrase in name only,
#: and twelve is one nobody will type. Four digits is a PIN and sixteen is
#: every card and lock there is.
_BOUNDS = {
    Scheme.CHARACTERS: Bounds(lower=8, upper=128, default=DEFAULT_LENGTH),
    Scheme.PASSPHRASE: Bounds(lower=3, upper=12, default=DEFAULT_WORDS),
    Scheme.DIGITS: Bounds(lower=4, upper=16, default=DEFAULT_DIGITS),
}

_TITLES = {
    Scheme.CHARACTERS: "Random Characters",
    Scheme.PASSPHRASE: "Words",
    Scheme.DIGITS: "Digits Only",
}

_SIZE_TITLES = {
    Scheme.CHARACTERS: "Length",
    Scheme.PASSPHRASE: "Words",
    Scheme.DIGITS: "Digits",
}


def generate_password(length: int = DEFAULT_LENGTH, symbols: bool = True) -> str:
    """A password of ``length`` characters drawn uniformly from the alphabet.

    Args:
        length: How many characters. Must be at least one.
        symbols: Whether punctuation may appear.

    Raises:
        ValueError: If ``length`` is not positive, rather than handing back
            something unusable.
    """
    if length < 1:
        raise ValueError("A password needs at least one character")

    alphabet = ALPHABET if symbols else LETTERS_AND_DIGITS
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_passphrase(
    words: int = DEFAULT_WORDS, separator: str = DEFAULT_SEPARATOR
) -> str:
    """A passphrase of ``words`` words drawn uniformly from the EFF list.

    Each word is an independent draw from the whole list, repeats included.
    Drawing without replacement would make the second word one of 7775 and the
    third one of 7774, which is less entropy than :attr:`Recipe.entropy_bits`
    reports beside it -- and a repeated word in a six-word phrase is a one in
    a thousand event that costs nothing when it happens.

    Args:
        words: How many words. Must be at least one.
        separator: What goes between them.

    Raises:
        ValueError: If ``words`` is not positive.
    """
    if words < 1:
        raise ValueError("A passphrase needs at least one word")

    return separator.join(secrets.choice(WORDS) for _ in range(words))


def generate_digits(length: int = DEFAULT_DIGITS) -> str:
    """A PIN of ``length`` digits.

    A string rather than a number, because a leading zero is part of a PIN and
    an integer would lose it.

    Args:
        length: How many digits. Must be at least one.

    Raises:
        ValueError: If ``length`` is not positive.
    """
    if length < 1:
        raise ValueError("A PIN needs at least one digit")

    return "".join(secrets.choice(DIGITS) for _ in range(length))


@dataclass(frozen=True)
class Recipe:
    """A scheme and the size it is to be generated at.

    One object rather than three call signatures. The add dialog, the edit
    dialog and the rotation wizard all offer the same choice and all have to
    carry the answer somewhere, and a scheme without its size is not enough to
    generate from.
    """

    scheme: Scheme = Scheme.CHARACTERS
    #: Characters, words or digits, depending on the scheme. None takes the
    #: scheme's default, which is what makes ``Recipe(scheme)`` usable.
    size: int | None = None
    #: Characters only; the other two schemes have no punctuation to allow.
    symbols: bool = True
    #: Passphrases only.
    separator: str = DEFAULT_SEPARATOR

    @property
    def resolved_size(self) -> int:
        """The size to generate at, with the scheme's default filled in."""
        if self.size is None:
            return self.scheme.bounds.default
        return self.size

    def generate(self) -> str:
        """The generated value.

        Raises:
            ValueError: If the size is outside what the scheme accepts. The
                spin rows in the interface cannot produce one, but a recipe
                restored from a setting somebody edited can.
        """
        size = self.resolved_size
        bounds = self.scheme.bounds
        if not bounds.lower <= size <= bounds.upper:
            raise ValueError(
                f"{self.scheme.title} takes between {bounds.lower} and "
                f"{bounds.upper}, not {size}"
            )

        if self.scheme is Scheme.PASSPHRASE:
            return generate_passphrase(words=size, separator=self.separator)
        if self.scheme is Scheme.DIGITS:
            return generate_digits(length=size)
        return generate_password(length=size, symbols=self.symbols)

    @property
    def _choices(self) -> int:
        """How many possibilities each draw has."""
        if self.scheme is Scheme.PASSPHRASE:
            return len(WORDS)
        if self.scheme is Scheme.DIGITS:
            return len(DIGITS)
        return len(ALPHABET if self.symbols else LETTERS_AND_DIGITS)

    @property
    def entropy_bits(self) -> float:
        """How much guessing this recipe costs, in bits.

        Shown beside the generated value, because it is the only way to compare
        a twenty-character password with a six-word passphrase -- they are
        within a few bits of each other and look nothing alike. Getting this
        wrong would be worse than omitting it: it would talk somebody out of
        the stronger of the two.

        This is the entropy of the *process*, which is what there is to report:
        the value it produced has whatever entropy it has, and counting the
        characters of one particular output is the mistake every strength meter
        makes.
        """
        return self.resolved_size * math.log2(self._choices)
