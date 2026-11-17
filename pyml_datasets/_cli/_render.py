"""Rich output of the commands: the table of ``list`` and the panel of ``show``.

Everything that comes from a dataset is wrapped in ``Text`` objects, so a ``[`` in a title or
a citation is printed as it is and never read as markup.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final

from rich import box
from rich.console import Group, RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .._types import DatasetInfo

_TASK_STYLES: Final = {"classification": "cyan", "regression": "magenta"}
_MAX_NAMES: Final = 10


@dataclass(frozen=True)
class ListRow:
    """One line of the ``list`` table.

    Attributes
    ----------
    name : str
        Dataset name.
    task : str
        ``"classification"`` or ``"regression"``.
    license : str
        SPDX identifier of the license.
    n_samples : int
        Number of rows of ``X``.
    n_features : int
        Number of columns of ``X``.
    """

    name: str
    task: str
    license: str
    n_samples: int
    n_features: int


def list_table(rows: Sequence[ListRow], totals: Mapping[str, int]) -> Table:
    """Build the table of all datasets.

    Parameters
    ----------
    rows : sequence of ListRow
        One row for every dataset, in the order they are shown.
    totals : mapping of str to int
        Number of datasets of every task, shown below the table.

    Returns
    -------
    rich.table.Table
        The table, ready to be printed.
    """
    counts = ", ".join(f"{task} {count}" for task, count in totals.items())
    table = Table(
        box=box.SIMPLE_HEAD,
        header_style="bold",
        pad_edge=False,
        collapse_padding=True,
        caption=f"{len(rows)} datasets: {counts}",
        caption_justify="left",
    )
    table.add_column("Dataset", no_wrap=True)
    table.add_column("Task", no_wrap=True)
    table.add_column("License", no_wrap=True)
    table.add_column("Samples", justify="right", no_wrap=True)
    table.add_column("Features", justify="right", no_wrap=True)
    for row in rows:
        table.add_row(
            Text(row.name, style="bold"),
            Text(row.task, style=_TASK_STYLES.get(row.task, "")),
            Text(row.license),
            Text(str(row.n_samples)),
            Text(str(row.n_features)),
        )
    return table


def _names(names: Sequence[str]) -> str:
    """Join names, keeping the first few when there are many.

    Parameters
    ----------
    names : sequence of str
        Feature or class names.

    Returns
    -------
    str
        The names separated by commas, with the number of the left out ones at the end.
    """
    shown = ", ".join(names[:_MAX_NAMES])
    if len(names) > _MAX_NAMES:
        shown += f", ... ({len(names) - _MAX_NAMES} more)"
    return shown


def _size(size: int) -> str:
    """Format a number of bytes as KiB or MiB.

    Parameters
    ----------
    size : int
        Number of bytes.

    Returns
    -------
    str
        The size with one decimal.
    """
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MiB"
    return f"{size / 1024:.1f} KiB"


def _section(title: str, items: Sequence[str]) -> RenderableType:
    """Build a titled bullet list.

    Parameters
    ----------
    title : str
        Heading of the section.
    items : sequence of str
        The bullets.

    Returns
    -------
    rich.console.RenderableType
        The heading with its bullets below, indented.
    """
    bullets = Table.grid(padding=(0, 1))
    bullets.add_column(no_wrap=True)
    bullets.add_column()
    for item in items:
        bullets.add_row(Text("-"), Text(item))
    return Group(Text(title, style="bold"), Padding(bullets, (0, 0, 0, 2)))


def show_panel(
    info: DatasetInfo,
    *,
    shape: tuple[int, int],
    size: int,
    feature_names: Sequence[str],
    target_names: Sequence[str] | None,
) -> Panel:
    """Build the panel with the facts about one dataset.

    Parameters
    ----------
    info : DatasetInfo
        Provenance and license of the dataset.
    shape : tuple of int
        Number of samples and number of features.
    size : int
        Size of the data file in bytes.
    feature_names : sequence of str
        Names of the columns of ``X``.
    target_names : sequence of str or None
        Class or target names, ``None`` if the dataset has none.

    Returns
    -------
    rich.panel.Panel
        The panel, ready to be printed.
    """
    facts: list[tuple[str, str]] = [
        ("Name", info.name),
        ("Task", info.task),
        ("License", f"{info.license} ({info.license_url})"),
        ("Source", f"{info.source} ({info.source_url})"),
        ("DOI", info.doi or "none"),
        ("Creators", ", ".join(info.creators)),
        ("Shape", f"{shape[0]} samples x {shape[1]} features"),
        ("File size", _size(size)),
        ("Features", _names(feature_names)),
    ]
    if target_names is not None:
        label = "Classes" if info.task == "classification" else "Targets"
        facts.append((label, _names(target_names)))
    if info.categorical:
        facts.append(("Categorical", _names(list(info.categorical))))
    facts.append(("Missing values", "yes, stored as NaN" if info.has_missing else "no"))
    facts.append(("License checked", info.verified_on))

    grid = Table.grid(padding=(0, 2))
    grid.add_column(no_wrap=True, style="cyan")
    grid.add_column(overflow="fold")
    for key, value in facts:
        grid.add_row(Text(key), Text(value))

    parts: list[RenderableType] = [Text(info.summary), Text(""), grid, Text("")]
    parts += [Text("Citation", style="bold"), Padding(Text(info.citation), (0, 0, 1, 2))]
    parts.append(_section("Changes made to the data", info.changes))
    if info.notes:
        parts += [Text(""), _section("Notes", info.notes)]
    return Panel(Group(*parts), title=Text(info.title, style="bold"), title_align="left")
