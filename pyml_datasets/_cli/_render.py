"""Rich output of the commands: the table of ``list`` and the report of ``show``.

Everything that comes from a dataset is wrapped in ``Text`` objects, so a ``[`` in a title or
a citation is printed as it is and never read as markup.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final

from rich import box
from rich.console import Console, ConsoleOptions, Group, RenderableType, RenderResult
from rich.padding import Padding
from rich.rule import Rule
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .._types import DatasetInfo

_TASK_STYLES: Final = {"classification": "cyan", "regression": "magenta"}
_LABEL_STYLES: Final = {"classification": "black on cyan", "regression": "black on magenta"}
_LICENSE_LABEL: Final = "black on green"
_LINK_STYLE: Final = Style(color="bright_blue", underline=True)


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


def list_table(
    rows: Sequence[ListRow], totals: Mapping[str, int], note: str | None = None
) -> Table:
    """Build the table of all datasets.

    Parameters
    ----------
    rows : sequence of ListRow
        One row for every dataset, in the order they are shown.
    totals : mapping of str to int
        Number of shown datasets of every task, shown below the table.
    note : str, optional
        A sentence for a second line below the table, for example which part of the
        datasets is shown.

    Returns
    -------
    rich.table.Table
        The table, ready to be printed.
    """
    counts = ", ".join(f"{task} {count}" for task, count in totals.items())
    caption = f"{_plural(len(rows), 'dataset')}: {counts}" + (f"\n{note}" if note else "")
    table = Table(
        box=box.SIMPLE_HEAD,
        header_style="bold",
        pad_edge=False,
        collapse_padding=True,
        caption=caption,
        caption_justify="left",
    )
    table.add_column("Dataset", justify="left", no_wrap=True)
    table.add_column("Task", justify="center", no_wrap=True)
    table.add_column("License", justify="center", no_wrap=True)
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


def _plural(count: int, word: str) -> str:
    """Write a count with its noun.

    Parameters
    ----------
    count : int
        The number of things.
    word : str
        The noun in the singular.

    Returns
    -------
    str
        For example ``"1 note"`` or ``"5 notes"``.
    """
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


class _Divider:
    """A thin line across the terminal.

    ``rich.rule.Rule`` without a title draws ``─`` even when the output cannot encode it, for
    example a pipe on Windows that uses cp1252, and printing then fails. This line draws a
    hyphen there.
    """

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Draw the line with a character that the output can encode.

        Parameters
        ----------
        console : rich.console.Console
            The console that prints the line.
        options : rich.console.ConsoleOptions
            The options of the console, which say whether the output is ASCII only.

        Yields
        ------
        rich.rule.Rule
            The line.
        """
        yield Rule(characters="-" if options.ascii_only else "─", style="dim")


def _heading(title: str) -> RenderableType:
    """Build the heading of a section: the title and a thin line after it.

    Parameters
    ----------
    title : str
        Text of the heading.

    Returns
    -------
    rich.console.RenderableType
        The heading, aligned to the left.
    """
    return Rule(Text(title, style="bold"), align="left", style="dim")


def _link(url: str) -> Text:
    """Make a URL that is also a link in terminals that support links.

    The URL is the visible text, so it is not lost when links are not drawn.

    Parameters
    ----------
    url : str
        The address.

    Returns
    -------
    rich.text.Text
        The address, underlined and linked to itself.
    """
    return Text(url, style=_LINK_STYLE + Style(link=url))


def _facts(rows: Sequence[tuple[str, RenderableType]]) -> RenderableType:
    """Build an indented list of facts: a key and its value on every line.

    Parameters
    ----------
    rows : sequence of tuple
        The key and the value of every fact.

    Returns
    -------
    rich.console.RenderableType
        The keys in one column and the values in another.
    """
    grid = Table.grid(padding=(0, 2))
    grid.add_column(no_wrap=True, style="cyan")
    grid.add_column(overflow="fold")
    for key, value in rows:
        grid.add_row(Text(key), value)
    return Padding(grid, (0, 0, 0, 2))


def _bullets(title: str, items: Sequence[str]) -> RenderableType:
    """Build a section with a bullet list.

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
    return Group(_heading(title), Padding(bullets, (0, 0, 0, 2)))


def _header(info: DatasetInfo) -> RenderableType:
    """Build the first line: the title on the left, the task and the license on the right.

    Parameters
    ----------
    info : DatasetInfo
        Provenance and license of the dataset.

    Returns
    -------
    rich.console.RenderableType
        The line and a thin line below it.
    """
    labels = Text.assemble(
        Text(f" {info.task} ", style=_LABEL_STYLES.get(info.task, "")),
        " ",
        Text(f" {info.license} ", style=_LICENSE_LABEL),
    )
    line = Table.grid(expand=True, padding=(0, 2))
    line.add_column(ratio=1)
    line.add_column(justify="right", no_wrap=True)
    line.add_row(Text(info.title, style="bold"), labels)
    return Group(line, _Divider())


def _hidden_parts(info: DatasetInfo) -> Text:
    """Tell what the default output leaves out and how to read it.

    Parameters
    ----------
    info : DatasetInfo
        Provenance and license of the dataset.

    Returns
    -------
    rich.text.Text
        A line that counts the changes and the notes. It stands out when there are notes,
        because a note can hold a warning.
    """
    parts = [_plural(len(info.changes), "change")]
    if info.notes:
        parts.append(_plural(len(info.notes), "note"))
    many = len(parts) > 1 or len(info.changes) > 1
    message = (
        f"{' and '.join(parts)} {'are' if many else 'is'} not shown. "
        f"Run with --full to read {'them' if many else 'it'}."
    )
    return Text(message, style="yellow" if info.notes else "dim")


def show_report(
    info: DatasetInfo,
    *,
    shape: tuple[int, int],
    size: int,
    feature_names: Sequence[str],
    target_names: Sequence[str] | None,
    full: bool = False,
) -> RenderableType:
    """Build the report with the facts about one dataset.

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
    full : bool, default=False
        Add the changes made to the data and the notes. Without it a line says how many
        there are.

    Returns
    -------
    rich.console.RenderableType
        The report, ready to be printed.
    """
    categorical = [name for name in feature_names if name in info.categorical]
    numeric = [name for name in feature_names if name not in info.categorical]
    kinds = (
        f"{shape[1]} ({len(categorical)} categorical, {len(numeric)} numeric)"
        if categorical
        else f"{shape[1]} (all numeric)"
    )
    overview: list[tuple[str, RenderableType]] = [
        ("Samples", Text(str(shape[0]))),
        ("Features", Text(kinds)),
    ]
    if target_names is not None:
        label = "Classes" if info.task == "classification" else "Targets"
        overview.append((label, Text(", ".join(target_names))))
    overview.append(("Missing", Text("yes, stored as NaN" if info.has_missing else "no")))
    overview.append(("File size", Text(_size(size))))

    provenance: list[tuple[str, RenderableType]] = [
        ("Source", Text.assemble(info.source, "\n", _link(info.source_url))),
        (
            "License",
            Text.assemble(
                f"{info.license}, checked {info.verified_on}", "\n", _link(info.license_url)
            ),
        ),
    ]
    if info.doi:
        provenance.append(("DOI", Text(info.doi, style=Style(link=f"https://doi.org/{info.doi}"))))
    provenance.append(("Creators", Text(", ".join(info.creators))))

    features: list[tuple[str, RenderableType]] = []
    if numeric:
        features.append((f"Numeric ({len(numeric)})", Text(", ".join(numeric))))
    if categorical:
        features.append((f"Categorical ({len(categorical)})", Text(", ".join(categorical))))

    parts: list[RenderableType] = [
        _header(info),
        Text(""),
        Text(info.summary),
        Text(""),
        _heading("Overview"),
        _facts(overview),
        Text(""),
        _heading("Provenance"),
        _facts(provenance),
        Text(""),
        _heading("Features"),
        _facts(features),
        Text(""),
        _heading("Citation"),
        Padding(Text(info.citation), (0, 0, 0, 2)),
        Text(""),
    ]
    if full:
        parts.append(_bullets("Changes made to the data", info.changes))
        if info.notes:
            parts += [Text(""), _bullets("Notes", info.notes)]
    else:
        parts.append(_hidden_parts(info))
    return Group(*parts)
