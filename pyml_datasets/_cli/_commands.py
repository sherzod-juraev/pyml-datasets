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
from . import _facts, _formats, _output, _render

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


def _deliver(destination: _output.Destination, text: str) -> int:
    """Write the output and return the exit code of the command.

    Parameters
    ----------
    destination : Destination
        Where the output goes.
    text : str
        The output.

    Returns
    -------
    int
        0 if the output was written, 1 if the file cannot be written.
    """
    try:
        _output.emit(destination, text)
    except OSError as error:
        _fail(str(error))
        return 1
    return 0


def _say(destination: _output.Destination, lines: list[str]) -> int:
    """Print sentences instead of a table, for example that no dataset matches.

    Parameters
    ----------
    destination : Destination
        Where the output goes.
    lines : list of str
        The sentences. JSON gets an empty list instead of them.

    Returns
    -------
    int
        0 if the output was written, 1 if the file cannot be written.
    """
    if destination.format == "json":
        return _deliver(destination, "[]\n")
    if destination.format == "md":
        return _deliver(destination, _formats.messages_markdown(lines))
    if destination.path is None:
        console = Console(highlight=False)
        for line in lines:
            console.print(Text(line))
        return 0
    return _deliver(destination, "\n".join(lines) + "\n")


def list_command(args: argparse.Namespace) -> int:
    """Print a table of the datasets.

    The datasets are filtered first (``task``, ``name``, ``missing``), then ordered, and the
    output shows the page that ``offset`` and ``limit`` choose.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments: ``task`` (a task name or ``None`` for all), ``name`` (a glob pattern
        or ``None``), ``missing`` (``True`` or ``False`` to keep the datasets with or without
        missing values, ``None`` for both), ``sort`` (the column to order by), ``reverse``,
        ``offset`` (rows to skip), ``limit`` (most rows to show, ``None`` for the default),
        ``show_all`` (show every row), ``format`` (``"text"``, ``"md"``, ``"json"`` or
        ``None``), ``output`` (a file, ``"-"`` or ``None``) and ``force``. The default limit
        does not apply to JSON.

    Returns
    -------
    int
        0 if the output was written or nothing matches, 1 if a data file is missing or
        unreadable or the file cannot be written, 2 if the options of the output do not fit.
    """
    try:
        destination = _output.choose_destination(args.format, args.output, args.force)
    except _output.OutputError as error:
        _fail(str(error))
        return 2
    rows: list[_render.ListRow] = []
    try:
        for name in list_datasets(args.task):
            if args.name is not None and not matches_name(name, args.name):
                continue
            info = get_info(name)
            if args.missing is not None and info.has_missing != args.missing:
                continue
            n_samples, n_features = _facts.read_shape(name)
            rows.append(
                _render.ListRow(
                    name, info.task, info.license, n_samples, n_features, info.has_missing
                )
            )
    except (FileNotFoundError, ValueError) as error:
        _fail(str(error))
        return 1
    total = len(rows)
    tip = None if args.name is None else _name_tip(args.name, list_datasets(args.task))
    if total == 0:
        return _say(destination, ["No dataset matches the filters.", *([tip] if tip else [])])
    if args.offset >= total:
        verb = "dataset matches" if total == 1 else "datasets match"
        return _say(destination, [f"The offset {args.offset} is past the end: {total} {verb}."])
    rows = sort_rows(rows, args.sort, args.reverse)
    if args.show_all:
        limit = None
    else:
        limit = args.limit or (None if destination.format == "json" else DEFAULT_LIMIT)
    page = rows[args.offset :] if limit is None else rows[args.offset : args.offset + limit]
    if destination.format == "json":
        return _deliver(destination, _formats.list_json(page, ascii_only=destination.path is None))
    notes = [tip] if tip else []
    if len(page) < total:
        notes.append(_page_note(args.offset + 1, args.offset + len(page), total))
    counts = Counter(row.task for row in page)
    totals = {task: counts[task] for task in TASKS if counts[task]}
    if destination.format == "md":
        return _deliver(destination, _formats.list_markdown(page, totals, notes))
    table = _render.list_table(page, totals, "\n".join(notes) or None)
    if destination.path is None:
        Console(highlight=False).print(table)
        return 0
    return _deliver(destination, _output.plain(table))


def show_command(args: argparse.Namespace) -> int:
    """Print the facts about one dataset.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments: the dataset name in ``name``, ``full``, which adds the changes made
        to the data and the notes (JSON always has them), ``format``, ``output`` and ``force``.

    Returns
    -------
    int
        0 if the report was written, 2 if no dataset has this name or the options of the
        output do not fit, 1 if its data file is missing or unreadable or the file cannot be
        written.
    """
    try:
        destination = _output.choose_destination(args.format, args.output, args.force)
    except _output.OutputError as error:
        _fail(str(error))
        return 2
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
    shape = (data.X.shape[0], data.X.shape[1])
    if destination.format == "json":
        text = _formats.show_json(
            info,
            shape=shape,
            size=size,
            feature_names=data.feature_names,
            target_names=data.target_names,
            ascii_only=destination.path is None,
        )
        return _deliver(destination, text)
    if destination.format == "md":
        text = _formats.show_markdown(
            info,
            shape=shape,
            size=size,
            feature_names=data.feature_names,
            target_names=data.target_names,
            full=args.full,
        )
        return _deliver(destination, text)
    report = _render.show_report(
        info,
        shape=shape,
        size=size,
        feature_names=data.feature_names,
        target_names=data.target_names,
        full=args.full,
    )
    if destination.path is None:
        Console(highlight=False).print(report)
        return 0
    return _deliver(destination, _output.plain(report))
