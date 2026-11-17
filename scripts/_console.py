"""Console output of the development scripts, written with ``rich``.

Every script prints through this module, so the messages look the same everywhere. ``rich``
decides about the color: there is none when the output is not a terminal (CI, a pipe), the
``NO_COLOR`` environment variable turns it off and ``FORCE_COLOR`` turns it on. Errors go to
``stderr``, everything else to ``stdout``.

Text that comes from outside, such as a dataset name or an error message, is printed as
plain :class:`~rich.text.Text`, so the ``[...]`` in it is never taken for markup.
"""

import os
from collections.abc import Iterable, Sequence
from typing import Final

from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

out: Final = Console(highlight=False)
err: Final = Console(stderr=True, highlight=False)

Cell = str | Text

_PLAIN_WIDTH: Final = 120
_SHORT_COLUMN: Final = 14
_GAP: Final = 3


def _fit(console: Console) -> None:
    """Make a console that is not a real terminal wide enough for a table.

    A CI log or a pipe has no width, and ``rich`` would use 80 characters and squeeze the
    columns. The ``COLUMNS`` environment variable, if set, decides instead.
    """
    if "COLUMNS" not in os.environ and not console.file.isatty():
        console.width = _PLAIN_WIDTH


def green(text: str) -> Text:
    """Return ``text`` in green, for something that is fine.

    Parameters
    ----------
    text : str
        Plain text.

    Returns
    -------
    Text
        The styled text.
    """
    return Text(text, style="green")


def yellow(text: str) -> Text:
    """Return ``text`` in yellow, for a reminder.

    Parameters
    ----------
    text : str
        Plain text.

    Returns
    -------
    Text
        The styled text.
    """
    return Text(text, style="yellow")


def red(text: str) -> Text:
    """Return ``text`` in red, for a problem.

    Parameters
    ----------
    text : str
        Plain text.

    Returns
    -------
    Text
        The styled text.
    """
    return Text(text, style="red")


def dim(text: str) -> Text:
    """Return ``text`` in a muted style, for something that was left as it was.

    Parameters
    ----------
    text : str
        Plain text.

    Returns
    -------
    Text
        The styled text.
    """
    return Text(text, style="dim")


def _line(label: str, style: str, message: str) -> Text:
    """Build a line made of a colored label and a plain message."""
    return Text.assemble((f"{label} ", f"bold {style}"), message)


def ok(message: str) -> None:
    """Print a message about something that worked.

    Parameters
    ----------
    message : str
        Plain text.
    """
    out.print(_line("ok", "green", message), soft_wrap=True)


def warn(message: str) -> None:
    """Print a warning, which does not make a command fail.

    Parameters
    ----------
    message : str
        Plain text.
    """
    out.print(_line("warning", "yellow", message), soft_wrap=True)


def fail(message: str) -> None:
    """Print an error to ``stderr``.

    Parameters
    ----------
    message : str
        Plain text.
    """
    err.print(_line("error", "red", message), soft_wrap=True)


def step(message: str) -> None:
    """Print the title of a step of a longer command.

    Parameters
    ----------
    message : str
        Plain text.
    """
    out.print(Text(f"==> {message}", style="bold"), soft_wrap=True)


def note(message: str) -> None:
    """Print a plain line of information.

    Parameters
    ----------
    message : str
        Plain text.
    """
    out.print(Text(message), soft_wrap=True)


def print_table(
    title: str,
    columns: Sequence[str],
    rows: Iterable[Sequence[Cell]],
    *,
    numeric: Sequence[int] = (),
    caption: str | None = None,
) -> None:
    """Print a table.

    Long values wrap instead of being cut, so nothing is lost in a narrow terminal. The
    first column and the short ones (dates, counts, yes/no) are never wrapped, only the
    columns with long text are. When the output is not a terminal (a
    CI log, a pipe) the table is 120 characters wide, so it is not squeezed into 80.

    Parameters
    ----------
    title : str
        Title above the table.
    columns : sequence of str
        Column headers.
    rows : iterable of sequence of (str or Text)
        The cells of every row. A plain ``str`` is printed as it is, a ``Text`` keeps its
        style.
    numeric : sequence of int, default=()
        Indexes of the columns that are aligned to the right.
    caption : str, optional
        Line below the table.
    """
    table = Table(
        title=title,
        title_justify="left",
        title_style="bold",
        caption=caption,
        caption_justify="left",
        box=box.SIMPLE_HEAD,
        header_style="bold",
        pad_edge=False,
        collapse_padding=True,
    )
    body = [list(row) for row in rows]
    widths = [
        max([len(column), *(len(str(row[i])) for row in body)]) for i, column in enumerate(columns)
    ]
    _fit(out)
    # Keep the short columns whole only when the whole table fits; if it does not, every
    # column may wrap, which is better than a table cut off at the edge.
    fits = sum(widths) + _GAP * (len(widths) - 1) <= out.width
    for index, column in enumerate(columns):
        widest = widths[index]
        short = fits and (index == 0 or widest <= _SHORT_COLUMN)
        table.add_column(
            column,
            justify="right" if index in numeric else "left",
            overflow="fold",
            no_wrap=short,
            min_width=widest if short else None,
        )
    for row in body:
        table.add_row(*(cell if isinstance(cell, Text) else Text(cell) for cell in row))
    out.print(table)
