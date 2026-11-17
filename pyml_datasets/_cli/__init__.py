"""The ``pyml-datasets`` command line.

This subpackage is private and is not imported by ``pyml_datasets``, so ``import pyml_datasets``
does not load ``rich``. It is reached through the ``pyml-datasets`` command and through
``python -m pyml_datasets``.

The output is meant to be read by people. Its layout can change in any release, so a program
should use ``list_datasets``, ``get_info`` and ``load_dataset`` instead of parsing it.
"""

import sys
from collections.abc import Sequence

from ._parser import build_parser

__all__ = ["main"]


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


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line.

    Parameters
    ----------
    argv : sequence of str, optional
        Command line arguments, ``sys.argv[1:]`` if not given.

    Returns
    -------
    int
        Exit code: 0 on success, 1 if a data file cannot be read and 2 for an unknown
        dataset name. A wrong command line makes the parser exit with code 2.

    Notes
    -----
    A character that the standard output cannot encode is printed as ``?``. For this the
    ``errors`` setting of ``sys.stdout`` and ``sys.stderr`` is changed to ``"replace"``.
    """
    _keep_going_on_unencodable_text()
    args = build_parser().parse_args(argv)
    code: int = args.handler(args)
    return code
