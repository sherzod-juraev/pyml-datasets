"""The commands of the command line. Each one returns the exit code of the program."""

import argparse
from collections import Counter
from collections.abc import Callable
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


def _fail(message: str) -> None:
    """Print an error message to the standard error stream.

    Parameters
    ----------
    message : str
        What went wrong. It is printed as it is, never read as markup.
    """
    Console(stderr=True, highlight=False).print(Text.assemble(("error: ", "bold red"), message))


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


def list_command(args: argparse.Namespace) -> int:
    """Print a table of the datasets.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments: ``task`` (a task name or ``None`` for all), ``sort`` (the column
        to order by) and ``reverse``.

    Returns
    -------
    int
        0 if the table was printed, 1 if a data file is missing or unreadable.
    """
    rows: list[_render.ListRow] = []
    try:
        for name in list_datasets(args.task):
            info = get_info(name)
            n_samples, n_features = _facts.read_shape(name)
            rows.append(_render.ListRow(name, info.task, info.license, n_samples, n_features))
    except (FileNotFoundError, ValueError) as error:
        _fail(str(error))
        return 1
    rows = sort_rows(rows, args.sort, args.reverse)
    counts = Counter(row.task for row in rows)
    totals = {task: counts[task] for task in TASKS if counts[task]}
    Console(highlight=False).print(_render.list_table(rows, totals))
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
