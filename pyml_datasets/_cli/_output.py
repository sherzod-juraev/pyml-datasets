"""Where the output of a command goes, and in which format."""

import io
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from rich.console import Console, RenderableType

FORMATS: Final = ("text", "md", "json")
_EXTENSIONS: Final = {".md": "md", ".txt": "text", ".json": "json"}
# A text file is wrapped at this width, so it does not depend on the terminal that wrote it.
_PLAIN_WIDTH: Final = 100


class OutputError(Exception):
    """The options that say where the output goes cannot be used together."""


@dataclass(frozen=True)
class Destination:
    """The format of the output and the file it is written to.

    Attributes
    ----------
    format : {"text", "md", "json"}
        The format of the output.
    path : pathlib.Path or None
        The full path of the file, ``None`` for the terminal.
    """

    format: str
    path: Path | None


def choose_destination(fmt: str | None, output: str | None, force: bool) -> Destination:
    """Decide the format and the file from the options ``--format``, ``--output`` and ``--force``.

    The file is checked here, before any work is done: its directory has to exist, and the
    file must not exist unless ``force`` is set.

    Parameters
    ----------
    fmt : {"text", "md", "json"} or None
        Value of ``--format``. Without it the format comes from the extension of the file
        (``.md``, ``.txt`` or ``.json``), and is ``"text"`` for the terminal.
    output : str or None
        Value of ``--output``: a path, ``"-"`` for the terminal, or ``None``.
    force : bool
        Whether an existing file may be overwritten.

    Returns
    -------
    Destination
        The format, and the full path of the file (``~`` is expanded and a relative path is
        taken from the current directory) or ``None`` for the terminal.

    Raises
    ------
    OutputError
        If the format cannot be told, if it does not fit the extension, if ``force`` is set
        without a file, if the directory does not exist, or if the file exists and ``force``
        is not set.
    """
    if output is None or output == "-":
        if force:
            raise OutputError("--force needs --output with a file.")
        return Destination(fmt or "text", None)
    try:
        path = Path(output).expanduser().resolve()
    except (RuntimeError, OSError) as error:
        raise OutputError(f"cannot read the path '{output}': {error}") from error
    inferred = _EXTENSIONS.get(path.suffix.lower())
    if fmt is None:
        if inferred is None:
            raise OutputError(
                f"cannot tell the format from the extension of '{path.name}'. "
                "Use .md, .txt or .json, or give --format."
            )
        fmt = inferred
    elif inferred is not None and inferred != fmt:
        raise OutputError(f"--format {fmt} does not fit the extension of '{path.name}'.")
    if not path.parent.is_dir():
        raise OutputError(f"the directory '{path.parent}' does not exist.")
    if path.is_dir():
        raise OutputError(f"'{path}' is a directory.")
    if path.exists() and not force:
        raise OutputError(f"'{path}' exists. Use --force to overwrite it.")
    return Destination(fmt, path)


def emit(destination: Destination, text: str) -> None:
    """Write the output to the terminal or to its file.

    A file is always written in UTF-8, without a byte order mark and with a line feed as the end
    of a line, whatever the console, the locale and the platform are. Nothing is replaced: a
    character that UTF-8 cannot write is an error.

    Parameters
    ----------
    destination : Destination
        Where the output goes.
    text : str
        The output.

    Raises
    ------
    OSError
        If the file cannot be written.
    """
    if destination.path is None:
        sys.stdout.write(text)
        return
    destination.path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {destination.path}", file=sys.stderr)


def plain(renderable: RenderableType) -> str:
    """Draw a rich renderable as text for a file: no colors, no links, a fixed width.

    Parameters
    ----------
    renderable : rich.console.RenderableType
        The table or the report.

    Returns
    -------
    str
        The lines without the spaces at their ends.
    """
    buffer = io.StringIO()
    console = Console(
        file=buffer,
        width=_PLAIN_WIDTH,
        color_system=None,
        force_terminal=False,
        legacy_windows=False,
        highlight=False,
    )
    console.print(renderable)
    return "\n".join(line.rstrip() for line in buffer.getvalue().splitlines()) + "\n"
