"""Everything the application reads at runtime has to reach the wheel.

A file under ``src/`` that setuptools was never told about is present in a
checkout and absent from every package built from it, so it works here and
fails once installed -- which is the one place nobody runs the application
before shipping it. There is already one instance of this in the history: the
``.ui`` templates and ``demo.json`` had to be added to ``package-data`` after
the built wheel failed on import.

CI does test the installed packages, so this would be caught -- but it would be
caught as an ImportError out of an unrelated test, twenty minutes into a job on
another machine, rather than here.
"""

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src"

#: Suffixes setuptools picks up on its own, plus prose. A README beside the
#: .blp files is for whoever edits them and has no business in the wheel.
_IGNORED_SUFFIXES = {".py", ".pyc", ".pyi", ".md"}

#: Directories that are not part of the source tree at all. The egg-info is the
#: one that matters: it is a build artefact left in ``src/`` by an editable
#: install, and AGENTS.md has the longer story about what it has already
#: broken once.
_IGNORED_DIRECTORIES = {"__pycache__", ".mypy_cache", ".ruff_cache"}
_IGNORED_SUFFIX_DIRECTORIES = (".egg-info",)


def declared_package_data() -> dict[str, list[str]]:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        config = tomllib.load(handle)
    return config["tool"]["setuptools"]["package-data"]


def shipped_files() -> dict[str, set[str]]:
    """Every non-Python file under ``src/``, by the package that holds it."""
    found: dict[str, set[str]] = {}
    for path in SOURCE.rglob("*"):
        if not path.is_file() or path.suffix in _IGNORED_SUFFIXES:
            continue
        parts = set(path.relative_to(SOURCE).parts)
        if _IGNORED_DIRECTORIES & parts:
            continue
        if any(part.endswith(_IGNORED_SUFFIX_DIRECTORIES) for part in parts):
            continue
        package = ".".join(path.parent.relative_to(SOURCE).parts)
        found.setdefault(package, set()).add(path.suffix)
    return found


class TestEveryDataFileIsDeclared:
    def test_each_package_holding_one_is_named_in_package_data(self):
        declared = declared_package_data()

        undeclared = sorted(set(shipped_files()) - set(declared))

        assert undeclared == [], (
            f"these packages hold files that no package-data entry ships: {undeclared}"
        )

    def test_each_suffix_is_covered_by_a_pattern(self):
        declared = declared_package_data()

        missing = [
            f"{package}: {suffix}"
            for package, suffixes in shipped_files().items()
            for suffix in sorted(suffixes)
            if package in declared and f"*{suffix}" not in declared[package]
        ]

        assert missing == [], f"declared packages with an unshipped suffix: {missing}"

    def test_the_wordlist_is_one_of_them(self):
        """The passphrase generator reads it at import, so its absence is fatal.

        Named rather than left to the sweep above, because the sweep only sees
        what is in the checkout: this says which file the rule was written for.
        """
        assert ".txt" in shipped_files()["gtkpass.utils.data"]
        assert "*.txt" in declared_package_data()["gtkpass.utils.data"]
