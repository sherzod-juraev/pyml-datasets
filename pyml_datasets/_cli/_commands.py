"""The commands of the command line. Each one returns the exit code of the program."""

import argparse
from collections import Counter
from collections.abc import Callable, Iterable
from fnmatch import fnmatchcase
from typing import Final

from rich.console import Console
from rich.text import Text

from .._registry import get_info, list_datasets, load_dataset
from .._types import TASKS
from . import _facts, _render

_SORT_COLUMNS: Final[dict[str, Callable[[_render.ListRow], str | int]]] = {
    "name": lambda row: row.name,
    "samples": lambda row: row.n_samples,
    "features": lambda row: row.n_features,
}
SORT_KEYS: Final = tuple(_SORT_COLUMNS)
DEFAULT_LIMIT: Final = 25
# The characters that make a pattern more than a name. ``%`` is ``*`` of SQL.
_WILDCARDS: Final = "*?[%"


def _fail(message: str) -> None:
    """Print an error message to the standard error stream.

    Parameters
    ----------
    message : str
        What went wrong. It is printed as it is, never read as markup.
    """
    Console(stderr=True, highlight=False).print(Text.assemble(("error: ", "bold red"), message))


def matches_name(name: str, pattern: str) -> bool:
    """Tell whether a dataset name matches a pattern, as ``LIKE`` does in SQL.

    The pattern is a glob: ``*`` (or ``%``, as in SQL) stands for any characters, ``?`` for
    one character and ``[abc]`` for one of the listed characters. A pattern without them has
    to match the whole name. ``_`` is an ordinary character, because the names have it.
    Capital letters and small letters are the same.

    Parameters
    ----------
    name : str
        Name of a dataset.
    pattern : str
        Glob pattern, for example ``"wine*"`` for the names that start with ``wine``.

    Returns
    -------
    bool
        ``True`` if the whole name matches.

    Examples
    --------
    >>> matches_name("wine_quality", "wine*")
    True
    >>> matches_name("wine_quality", "*QUALITY")
    True
    >>> matches_name("wine_quality", "wine%")
    True
    >>> matches_name("wine_quality", "wine")
    False
    """
    return fnmatchcase(name.lower(), pattern.lower().replace("%", "*"))


def _name_tip(pattern: str, names: Iterable[str]) -> str | None:
    """Tell the user that a pattern without wildcards has to match the whole name.

    The tip is given only when it would have helped: some other name contains the pattern.

    Parameters
    ----------
    pattern : str
        The pattern of ``--name``.
    names : iterable of str
        Names of the datasets that the pattern is tried on.

    Returns
    -------
    str or None
        The sentence for the user, ``None`` if the pattern has a wildcard or no other name
        contains it.
    """
    if any(char in pattern for char in _WILDCARDS):
        return None
    if not any(
        matches_name(name, f"*{pattern}*") and not matches_name(name, pattern) for name in names
    ):
        return None
    return (
        f'Tip: "{pattern}" has to match the whole name. Use "{pattern}*" for the names that '
        f'start with it or "*{pattern}*" for the names that contain it.'
    )


def sort_rows(rows: list[_render.ListRow], key: str, reverse: bool) -> list[_render.ListRow]:
    """Order the rows of the ``list`` table.

    Rows with an equal value stay in the order of their names, also when the order is
    reversed, so the output is the same on every run.

    Parameters
    ----------
    rows : list of ListRow
        The rows to order.
    key : {"name", "samples", "features"}
        The column to order by.
    reverse : bool
        Put the largest value (the last name) first.

    Returns
    -------
    list of ListRow
        New list with the rows in the asked order.
    """
    by_name = sorted(rows, key=_SORT_COLUMNS["name"])
    # A reversed sort keeps equal values in their earlier order, so the ties stay by name.
    return sorted(by_name, key=_SORT_COLUMNS[key], reverse=reverse)


def _page_note(first: int, last: int, total: int) -> str:
    """Say which rows of the matching datasets the table shows.

    Parameters
    ----------
    first : int
        Position of the first shown row, counted from 1.
    last : int
        Position of the last shown row.
    total : int
        Number of datasets that match the filters.

    Returns
    -------
    str
        The sentence for the line below the table.
    """
    note = f"Showing {first}-{last} of {total}."
    if last < total:
        note += " Use --offset or --all to see more."
    return note


def list_command(args: argparse.Namespace) -> int:
    """Print a table of the datasets.

    The datasets are filtered first (``task``, ``name``, ``missing``), then ordered, and the
    table shows the page that ``offset`` and ``limit`` choose.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments: ``task`` (a task name or ``None`` for all), ``name`` (a glob pattern
        or ``None``), ``missing`` (``True`` or ``False`` to keep the datasets with or without
        missing values, ``None`` for both), ``sort`` (the column to order by), ``reverse``,
        ``offset`` (rows to skip), ``limit`` (most rows to show, ``None`` for the default)
        and ``show_all`` (show every row).

    Returns
    -------
    int
        0 if the table or the message that nothing matches was printed, 1 if a data file is
        missing or unreadable.
    """
    rows: list[_render.ListRow] = []
    try:
        for name in list_datasets(args.task):
            if args.name is not None and not matches_name(name, args.name):
                continue
            info = get_info(name)
            if args.missing is not None and info.has_missing != args.missing:
                continue
            n_samples, n_features = _facts.read_shape(name)
            rows.append(_render.ListRow(name, info.task, info.license, n_samples, n_features))
    except (FileNotFoundError, ValueError) as error:
        _fail(str(error))
        return 1
    console = Console(highlight=False)
    total = len(rows)
    tip = None if args.name is None else _name_tip(args.name, list_datasets(args.task))
    if total == 0:
        console.print(Text("No dataset matches the filters."))
        if tip:
            console.print(Text(tip))
        return 0
    if args.offset >= total:
        verb = "dataset matches" if total == 1 else "datasets match"
        console.print(Text(f"The offset {args.offset} is past the end: {total} {verb}."))
        return 0
    rows = sort_rows(rows, args.sort, args.reverse)
    limit = None if args.show_all else (args.limit or DEFAULT_LIMIT)
    page = rows[args.offset :] if limit is None else rows[args.offset : args.offset + limit]
    notes = [tip] if tip else []
    if len(page) < total:
        notes.append(_page_note(args.offset + 1, args.offset + len(page), total))
    note = "\n".join(notes) or None
    counts = Counter(row.task for row in page)
    totals = {task: counts[task] for task in TASKS if counts[task]}
    console.print(_render.list_table(page, totals, note))
    return 0


def show_command(args: argparse.Namespace) -> int:
    """Print the facts about one dataset.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments: the dataset name in ``name`` and ``full``, which adds the changes
        made to the data and the notes.

    Returns
    -------
    int
        0 if the report was printed, 2 if no dataset has this name, 1 if its data file is
        missing or unreadable.
    """
    try:
        info = get_info(args.name)
    except ValueError as error:
        _fail(str(error))
        return 2
    try:
        data = load_dataset(info.name)
        size = _facts.read_size(info.name)
    except (FileNotFoundError, ValueError) as error:
        _fail(str(error))
        return 1
    report = _render.show_report(
        info,
        shape=(data.X.shape[0], data.X.shape[1]),
        size=size,
        feature_names=data.feature_names,
        target_names=data.target_names,
        full=args.full,
    )
    Console(highlight=False).print(report)
    return 0
