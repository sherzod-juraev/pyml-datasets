"""The ``pyml-datasets`` command line.

This subpackage is private and is not imported by ``pyml_datasets``, so ``import pyml_datasets``
does not load ``rich``. It is reached through the ``pyml-datasets`` command and through
``python -m pyml_datasets``.

The output is meant to be read by people. Its layout can change in any release, so a program
should use ``list_datasets``, ``get_info`` and ``load_dataset`` instead of parsing it.
"""

import sys
from collections.abc import Sequence
from typing import Final

__all__ = ["main"]

# The packages that only the command line needs, they are the ``cli`` extra of the package.
_CLI_PACKAGES: Final = frozenset({"rich", "rich_argparse"})
_MISSING_DEPENDENCY_CODE: Final = 3


def _keep_going_on_unencodable_text() -> None:
    """Print ``?`` for a character that the output cannot encode, instead of failing.

    A pipe or a file on Windows often uses cp1252, which has no ``ı`` for the name of a
    creator. The streams are changed only when they can be (a replaced ``sys.stdout`` may
    not allow it), and the encoding itself is kept.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="replace")


def _missing_dependency(error: ModuleNotFoundError) -> int | None:
    """Report a missing package of the ``cli`` extra on the standard error stream.

    Parameters
    ----------
    error : ModuleNotFoundError
        The error raised while the parser was imported.

    Returns
    -------
    int or None
        The exit code of the program if ``error`` is about ``rich`` or ``rich_argparse``,
        ``None`` for any other module. An error about another module is a bug, so the caller
        raises it again with its traceback.
    """
    name = error.name or ""
    if name.partition(".")[0] not in _CLI_PACKAGES:
        return None
    print(
        "pyml-datasets: the command line needs the packages rich and rich-argparse, "
        f"and {name!r} cannot be imported.\n"
        'Install them with "pip install rich rich-argparse", or install pyml-datasets '
        'with its "cli" extra.',
        file=sys.stderr,
    )
    return _MISSING_DEPENDENCY_CODE


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line.

    Parameters
    ----------
    argv : sequence of str, optional
        Command line arguments, ``sys.argv[1:]`` if not given.

    Returns
    -------
    int
        Exit code: 0 on success, 1 if a data file cannot be read, 2 for an unknown
        dataset name and 3 if ``rich`` or ``rich-argparse`` is not installed. A wrong command
        line makes the parser exit with code 2.

    Notes
    -----
    A character that the standard output cannot encode is printed as ``?``. For this the
    ``errors`` setting of ``sys.stdout`` and ``sys.stderr`` is changed to ``"replace"``.

    ``rich`` and ``rich-argparse`` belong to the ``cli`` extra, so they are imported here and
    not at the top of the module. If they are missing, a short message tells what to install,
    instead of a traceback.
    """
    _keep_going_on_unencodable_text()
    try:
        from ._parser import build_parser
    except ModuleNotFoundError as error:
        missing = _missing_dependency(error)
        if missing is None:
            raise
        return missing
    args = build_parser().parse_args(argv)
    code: int = args.handler(args)
    return code
