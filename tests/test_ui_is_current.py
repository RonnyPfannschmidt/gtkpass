"""The committed .ui files are the ones the .blp files compile to.

`.ui` is generated and committed, and nothing checked that the two agreed.
Editing a .blp without running `make ui` passed everything: `make check` clean,
the whole suite green -- and the application then ran the *previous* interface,
built, installed, and indistinguishable from the current one until something
was clicked.

`make ui` is a prerequisite of every target that runs or packages the
application, so a local run recompiles. This is for the case that dependency
cannot reach: a .blp committed without its .ui, after which every checkout,
every CI job and every package is built from a stale one.

Skipped where blueprint-compiler is absent, which is every environment that
tests an installed package -- there is no source tree to check there, only the
wheel that was built from one.
"""

import filecmp
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS = ROOT / "src" / "gtkpass" / "ui" / "blueprints"


def find_compiler() -> str | None:
    """blueprint-compiler, beside this interpreter or else on PATH.

    Beside the interpreter first, and that ordering is the whole of it: the
    suite runs as `.venv/bin/python -m pytest`, which does not put `.venv/bin`
    on PATH. Asking PATH alone answered None in the one environment that has
    the compiler, and every check in this file skipped -- silently, and looking
    exactly like passing.
    """
    beside = Path(sys.executable).parent / "blueprint-compiler"
    if beside.is_file() and os.access(beside, os.X_OK):
        return str(beside)
    return shutil.which("blueprint-compiler")


COMPILER = find_compiler()

#: Whether this is a checkout with .blp files in it. An installed wheel or RPM
#: has none, and runs this same suite with a different interpreter.
IN_A_CHECKOUT = BLUEPRINTS.is_dir() and (ROOT / "pyproject.toml").is_file()

#: Whether the interpreter running this is the development environment, which
#: is the one that has blueprint-compiler installed. `make test-wheel` and the
#: RPM job run the suite out of this same checkout under a different
#: interpreter, so "there are .blp files here" does not answer this.
IN_THE_DEV_ENVIRONMENT = Path(sys.executable).is_relative_to(ROOT / ".venv")

#: Applied to the classes below rather than as a module-level ``pytestmark``,
#: and that is the whole point of it being spelled out here.
#:
#: A module-level mark applies to *every* test in the file, the guard at the
#: bottom included -- so the check written to notice that the rest had all
#: skipped skipped along with them, and reported it as a pass. Which is the
#: same fault this file exists to catch, one level up.
needs_the_compiler = pytest.mark.skipif(
    COMPILER is None or not IN_A_CHECKOUT,
    reason="no blueprint-compiler, or no source tree to check",
)


def compile_into(destination: Path) -> subprocess.CompletedProcess[str]:
    """Compile every .blp into ``destination`` instead of beside its source."""
    sources = sorted(BLUEPRINTS.glob("*.blp"))
    assert sources, "no .blp files were found, so this checks nothing"
    return subprocess.run(
        [
            str(COMPILER),
            "batch-compile",
            str(destination),
            str(BLUEPRINTS),
            *(str(source) for source in sources),
        ],
        capture_output=True,
        text=True,
        check=False,
        # Deprecation warnings about Gtk.ShortcutsWindow are expected and are
        # not what this is about; see the note in shortcuts.blp.
        env={**os.environ, "NO_COLOR": "1"},
    )


@pytest.fixture(scope="module")
def freshly_compiled(tmp_path_factory) -> Path:
    destination = tmp_path_factory.mktemp("ui")
    result = compile_into(destination)
    assert result.returncode == 0, (
        f"the .blp sources do not compile at all:\n{result.stderr}"
    )
    return destination


def blueprint_names() -> list[str]:
    return sorted(source.stem for source in BLUEPRINTS.glob("*.blp"))


@needs_the_compiler
class TestEveryUiFileIsCurrent:
    def test_there_is_something_to_check(self):
        """Every assertion below passes vacuously if this finds nothing."""
        assert blueprint_names()

    @pytest.mark.parametrize("name", blueprint_names())
    def test_it_matches_its_blueprint(self, name, freshly_compiled):
        committed = BLUEPRINTS / f"{name}.ui"
        fresh = freshly_compiled / f"{name}.ui"

        assert committed.is_file(), f"{name}.blp has no .ui beside it; run `make ui`"
        assert fresh.is_file(), f"{name}.blp compiled to nothing"
        assert filecmp.cmp(committed, fresh, shallow=False), (
            f"{name}.ui is not what {name}.blp compiles to. Run `make ui` and "
            "commit both files -- until then the application runs the previous "
            "interface."
        )

    def test_no_ui_file_is_left_over_from_a_deleted_blueprint(self, freshly_compiled):
        """A .blp removed leaves its .ui behind, and it is still packaged."""
        committed = {path.stem for path in BLUEPRINTS.glob("*.ui")}

        assert committed == set(blueprint_names())


@needs_the_compiler
class TestTheCheckWouldNotice:
    """A comparison that cannot fail is worse than none: it reads as coverage.

    So this makes the failure happen, against a copy, and asserts that it is
    seen. Against a copy because the real ones are what the rest of the suite
    and the running application load.
    """

    def test_a_stale_file_is_detected(self, tmp_path, freshly_compiled):
        name = blueprint_names()[0]
        stale = tmp_path / f"{name}.ui"
        shutil.copy(freshly_compiled / f"{name}.ui", stale)
        stale.write_text(stale.read_text().replace("<property", "<x-property", 1))

        assert not filecmp.cmp(stale, freshly_compiled / f"{name}.ui", shallow=False)

    def test_an_identical_file_is_not_detected(self, tmp_path, freshly_compiled):
        name = blueprint_names()[0]
        same = tmp_path / f"{name}.ui"
        shutil.copy(freshly_compiled / f"{name}.ui", same)

        assert filecmp.cmp(same, freshly_compiled / f"{name}.ui", shallow=False)


@needs_the_compiler
def test_the_compiler_is_the_one_the_makefile_uses():
    """`make ui` runs it through uv; this runs whatever is on PATH.

    The two have to be the same program, or a version difference shows up as
    every file being stale -- which reads as "somebody forgot to run make ui"
    and is not.
    """
    through_make = subprocess.run(
        ["uv", "run", "blueprint-compiler", "--version"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "UV_NO_SYNC": "1"},
    )
    if through_make.returncode != 0:
        pytest.skip("uv is not usable here")

    on_path = subprocess.run(
        [str(COMPILER), "--version"], capture_output=True, text=True, check=False
    )

    assert on_path.stdout.strip() == through_make.stdout.strip(), (
        f"{sys.executable} sees a different blueprint-compiler than `make ui` does"
    )


@pytest.mark.skipif(
    not IN_THE_DEV_ENVIRONMENT,
    reason="only the development environment is expected to have the compiler",
)
def test_the_checks_above_are_not_all_skipping():
    """A whole file that skips looks identical to a whole file that passes.

    Deliberately outside ``needs_the_compiler``: a check that skips whenever
    the compiler is missing cannot report that the compiler is missing. The
    first two versions of this file both got that wrong -- one found no
    compiler and skipped everything silently, and the one written to catch that
    was marked alongside the rest and skipped with them.

    So the condition here is the interpreter, not the compiler. The
    development environment has blueprint-compiler as a dev dependency; if this
    is running under it and none was found, the checks above did not run.
    """
    assert COMPILER is not None, (
        "blueprint-compiler was not found, so nothing above this line ran. "
        "It is a dev dependency; run `make sync`."
    )
