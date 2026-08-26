"""What the Flatpak build is given to build from.

The application module's source is `type: dir` over the whole checkout, which
is the only way to build the working tree rather than a tag -- and it means
every file in the checkout is copied into the build context, whether it has
anything to do with the application or not.

On every build, too: flatpak-builder never caches a `type: dir` source, so this
module is rebuilt whether anything changed or not. There is no cache here to
invalidate, which is why the skip list is about what is copied rather than
about what looks stale.

Two things follow. Whatever is in there is inside the build sandbox, which for
`.dev/` means a password store -- a throwaway one with invented entries, but
the rule in AGENTS.md is that stores do not go where they are not needed. And
the copy is most of a gigabyte of this application's own build output, three
quarters of it previous Flatpak builds going into the next one.
"""

import re
from pathlib import Path
from typing import ClassVar

import pytest

ROOT = Path(__file__).resolve().parent.parent
APP_ID = "io.github.RonnyPfannschmidt.GTKPass"
MANIFEST = ROOT / "build-aux" / f"{APP_ID}.yml"


def read_dir_source(manifest: str) -> dict[str, object]:
    """The one ``type: dir`` source, read without a YAML parser.

    PyYAML is in the environment only as something pre-commit happens to pull
    in -- nothing declares it, so a test that imported it would be resting on
    an accident. The CI workflow is read the same way, by hand, for the same
    reason; ``test_the_reader_would_notice`` below is what keeps a hand reader
    honest, because one that finds nothing makes every assertion pass.

    Returns:
        The source's scalar values and its ``skip`` list.
    """
    lines = manifest.splitlines()
    index = 0
    for index, line in enumerate(lines):  # noqa: B007  -- index is the answer
        found = re.match(r"^(\s*)- type: dir\s*$", line)
        if found:
            break
    else:
        return {}

    # Keys of this list item are indented two past the dash that opens it.
    indent = " " * (len(found.group(1)) + 2)
    source: dict[str, object] = {"type": "dir"}
    skip: list[str] = []
    reading_skip = False

    for line in lines[index + 1 :]:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if not line.startswith(indent):
            break
        rest = line[len(indent) :]
        if rest.startswith((" ", "-")):
            if reading_skip and rest.strip().startswith("- "):
                skip.append(rest.strip()[2:].strip())
            continue
        key, _, value = rest.partition(":")
        reading_skip = key == "skip"
        if not reading_skip:
            source[key] = value.strip()

    source["skip"] = skip
    return source


@pytest.fixture(scope="module")
def checkout_source() -> dict:
    """The `type: dir` source the application module is built from."""
    return read_dir_source(MANIFEST.read_text())


def test_the_reader_would_notice():
    """Every assertion below passes vacuously if this finds nothing."""
    source = read_dir_source(MANIFEST.read_text())

    assert source, "no `type: dir` source was found in the manifest at all"
    assert source["path"] == ".."
    assert source["skip"], "the skip list was not read"


class TestTheCheckoutIsCopiedWithoutItsBuildOutput:
    """None of this is read by the build, and one of it is a password store.

    Every entry below is in .gitignore. Together they are about 1.4G, against a
    few megabytes of actual source -- and because a dir source is never cached,
    that is copied on every single build rather than once.
    """

    #: What must not reach the build context, and the reason for each.
    #:
    #: `.dev/` is the one that is not merely wasteful: it is a password store,
    #: with a GPG home beside it. Invented entries and a throwaway key, but a
    #: store belongs where it is used and nowhere else.
    UNWANTED: ClassVar[dict[str, str]] = {
        ".dev": "a password store and its GPG home",
        ".venv": "the development environment, and not the runtime's",
        "build": "wheel build output",
        "dist": "packages, including this build's own stamp",
        ".flatpak-build": "the previous Flatpak build, copied into this one",
        ".flatpak-builder": "the Flatpak module cache",
        ".flatpak-repo": "the repo `make flatpak-lint-repo` exports, 380M of it",
        "htmlcov": "coverage output",
        ".coverage": "likewise",
        ".git": "the history, which the build does not read -- the module sets"
        " SETUPTOOLS_SCM_PRETEND_VERSION because there is no repository here",
        ".pytest_cache": "rewritten by every test run",
        ".mypy_cache": "rewritten by every `make check`",
        ".ruff_cache": "likewise",
    }

    @pytest.mark.parametrize("unwanted", sorted(UNWANTED), ids=lambda name: name)
    def test_it_is_skipped(self, checkout_source, unwanted):
        skipped = set(checkout_source["skip"])

        assert unwanted in skipped, (
            f"{unwanted} is copied into the Flatpak build context "
            f"({self.UNWANTED[unwanted]})"
        )

    def test_the_source_is_still_the_checkout(self, checkout_source):
        """Skipping is not a substitute for building the working tree."""
        assert checkout_source["path"] == ".."

    def test_nothing_the_build_needs_is_skipped(self, checkout_source):
        """The manifest reads these out of the copied tree by name."""
        skipped = set(checkout_source["skip"])
        needed = {"src", "data", "pyproject.toml", "LICENSE", "uv.lock"}

        assert not (skipped & needed), f"the build reads {skipped & needed}"


class TestTheReaderIsNotFoolingItself:
    """A hand reader that quietly returns nothing passes every check above."""

    def test_a_source_with_no_skip_list_is_reported_as_having_none(self):
        manifest = MANIFEST.read_text()
        stripped = re.sub(r"\n\s*skip:\n(\s*- \S+\n)+", "\n", manifest, count=1)
        assert stripped != manifest, "the skip block was not found to remove"

        assert read_dir_source(stripped)["skip"] == []

    def test_a_manifest_with_no_dir_source_reads_as_empty(self):
        manifest = MANIFEST.read_text().replace("- type: dir", "- type: archive", 1)

        assert read_dir_source(manifest) == {}
