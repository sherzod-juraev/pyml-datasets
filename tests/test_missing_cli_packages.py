"""The command line without ``rich`` or ``rich-argparse``: a short message, not a traceback."""

import subprocess
import sys

import pytest

from pyml_datasets._cli import main

MESSAGE = 'Install them with "pip install rich rich-argparse"'

# The two ways a user starts the command: the installed command calls ``main``, and
# ``python -m pyml_datasets`` runs the ``__main__`` module.
ENTRY_POINTS = [
    "from pyml_datasets._cli import main; raise SystemExit(main(['list']))",
    "import runpy; runpy.run_module('pyml_datasets', run_name='__main__')",
]


def _import_the_modules_again(monkeypatch: pytest.MonkeyPatch) -> None:
    """Forget the modules of the command line, so ``main`` has to import them again.

    The tests put the modules back, so the other tests keep the ones they imported.
    """
    for name in [name for name in sys.modules if name.startswith("pyml_datasets._cli._")]:
        monkeypatch.delitem(sys.modules, name)


def _hide(monkeypatch: pytest.MonkeyPatch, package: str) -> None:
    """Make ``import package`` and the import of any of its modules fail.

    A module that is imported already is found in ``sys.modules`` without a look at its
    package, so the modules of the package are hidden one by one.
    """
    for name in [name for name in sys.modules if name.startswith(f"{package}.")]:
        monkeypatch.setitem(sys.modules, name, None)
    monkeypatch.setitem(sys.modules, package, None)


@pytest.mark.parametrize("package", ["rich", "rich_argparse"])
def test_a_missing_package_prints_a_message_and_exits_with_3(
    package: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _import_the_modules_again(monkeypatch)
    _hide(monkeypatch, package)
    assert main(["list"]) == 3
    captured = capsys.readouterr()
    assert captured.out == ""
    assert MESSAGE in captured.err
    assert package in captured.err
    assert "Traceback" not in captured.err


def test_a_module_of_the_package_that_cannot_be_imported_is_not_hidden(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _import_the_modules_again(monkeypatch)
    monkeypatch.setitem(sys.modules, "pyml_datasets._cli._commands", None)
    with pytest.raises(ModuleNotFoundError, match="_commands"):
        main(["list"])


@pytest.mark.parametrize("package", ["rich", "rich_argparse"])
@pytest.mark.parametrize("entry", ENTRY_POINTS)
def test_a_program_without_the_packages_does_not_fail_with_a_traceback(
    package: str, entry: str
) -> None:
    code = f"import sys; sys.modules[{package!r}] = None; {entry}"
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=False
    )
    assert result.returncode == 3, result.stderr
    assert result.stdout == ""
    assert MESSAGE in result.stderr
    assert "Traceback" not in result.stderr
