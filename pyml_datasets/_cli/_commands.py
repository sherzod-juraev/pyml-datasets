"""The commands of the command line. Each one returns the exit code of the program."""

import argparse
from collections import Counter

from rich.console import Console
from rich.text import Text

from .._registry import get_info, list_datasets, load_dataset
from .._types import TASKS
from . import _facts, _render


def _fail(message: str) -> None:
    """Print an error message to the standard error stream.

    Parameters
    ----------
    message : str
        What went wrong. It is printed as it is, never read as markup.
    """
    Console(stderr=True, highlight=False).print(Text.assemble(("error: ", "bold red"), message))


def list_command(args: argparse.Namespace) -> int:
    """Print a table of all datasets.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments. This command has none.

    Returns
    -------
    int
        0 if the table was printed, 1 if a data file is missing or unreadable.
    """
    del args
    rows: list[_render.ListRow] = []
    try:
        for name in list_datasets():
            info = get_info(name)
            n_samples, n_features = _facts.read_shape(name)
            rows.append(_render.ListRow(name, info.task, info.license, n_samples, n_features))
    except (FileNotFoundError, ValueError) as error:
        _fail(str(error))
        return 1
    counts = Counter(row.task for row in rows)
    totals = {task: counts[task] for task in TASKS}
    Console(highlight=False).print(_render.list_table(rows, totals))
    return 0


def show_command(args: argparse.Namespace) -> int:
    """Print the facts about one dataset.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments, with the dataset name in ``name``.

    Returns
    -------
    int
        0 if the panel was printed, 2 if no dataset has this name, 1 if its data file is
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
    panel = _render.show_panel(
        info,
        shape=(data.X.shape[0], data.X.shape[1]),
        size=size,
        feature_names=data.feature_names,
        target_names=data.target_names,
    )
    Console(highlight=False).print(panel)
    return 0
