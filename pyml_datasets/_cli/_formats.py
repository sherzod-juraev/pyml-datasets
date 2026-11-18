"""The Markdown and JSON output of the commands, as text for the terminal or for a file."""

import json
import re
from collections.abc import Mapping, Sequence

from .._types import DatasetInfo
from . import _render

# A bare address in the text of a dataset, which Markdown shows as plain text.
_BARE_ADDRESS = re.compile(r"(?<![<(\[/\w])https?://[^\s<>()\[\]]*[^\s<>()\[\].,;:!?]")
# The characters that Markdown reads as formatting.
_MARKDOWN_SPECIAL = re.compile(r"([\\`*_\[\]<>|])")


def escape(text: str) -> str:
    """Escape the characters that Markdown reads as formatting.

    Parameters
    ----------
    text : str
        A sentence of the program, for example a hint with a pattern in it.

    Returns
    -------
    str
        The text with a backslash before every such character.
    """
    return _MARKDOWN_SPECIAL.sub(r"\\\1", text)


def messages_markdown(lines: Sequence[str]) -> str:
    """Write sentences of the program, such as "No dataset matches", as Markdown paragraphs.

    Parameters
    ----------
    lines : sequence of str
        The sentences.

    Returns
    -------
    str
        One paragraph for every sentence.
    """
    return "\n\n".join(escape(line) for line in lines) + "\n"


def _link_addresses(text: str) -> str:
    """Put the bare addresses of a text in angle brackets, which Markdown shows as links.

    Parameters
    ----------
    text : str
        Text of a dataset, for example its citation.

    Returns
    -------
    str
        The text, with the same visible words.
    """
    return _BARE_ADDRESS.sub(lambda match: f"<{match[0]}>", text)


def _table(headers: Sequence[str], rows: Sequence[Sequence[str]], aligns: str) -> list[str]:
    """Build a Markdown table with aligned columns.

    Parameters
    ----------
    headers : sequence of str
        The names of the columns.
    rows : sequence of sequence of str
        The cells of every row.
    aligns : str
        One letter for each column: ``l`` for left, ``c`` for center and ``r`` for right.

    Returns
    -------
    list of str
        The lines of the table.
    """
    cells = [[cell.replace("|", "\\|") for cell in row] for row in rows]
    widths = [
        max(3, len(header), *(len(row[column]) for row in cells))
        for column, header in enumerate(headers)
    ]

    def line(row: Sequence[str]) -> str:
        """Write one line of the table, with the cells padded to the width of their column."""
        parts = []
        for column, cell in enumerate(row):
            if aligns[column] == "c":
                parts.append(cell.center(widths[column]))
            elif aligns[column] == "r":
                parts.append(cell.rjust(widths[column]))
            else:
                parts.append(cell.ljust(widths[column]))
        return "| " + " | ".join(parts) + " |"

    def mark(column: int) -> str:
        """Write the cell of the line below the header, which says how the column is aligned."""
        width = widths[column]
        if aligns[column] == "c":
            return ":" + "-" * width + ":"
        if aligns[column] == "r":
            return "-" * (width + 1) + ":"
        return ":" + "-" * (width + 1)

    rule = "|" + "|".join(mark(column) for column in range(len(headers))) + "|"
    return [line(headers), rule, *(line(row) for row in cells)]


def list_markdown(
    rows: Sequence[_render.ListRow], totals: Mapping[str, int], notes: Sequence[str]
) -> str:
    """Write the table of the datasets in Markdown.

    Parameters
    ----------
    rows : sequence of ListRow
        The rows of the table, in the order they are shown.
    totals : mapping of str to int
        Number of shown datasets of every task.
    notes : sequence of str
        Sentences for the lines below the table, for example which rows are shown.

    Returns
    -------
    str
        The table, a line that counts the datasets, and a paragraph for every note.
    """
    table = _table(
        ["Dataset", "Task", "License", "Samples", "Features"],
        [
            [f"`{row.name}`", row.task, row.license, str(row.n_samples), str(row.n_features)]
            for row in rows
        ],
        "lccrr",
    )
    paragraphs = [_render.counts_line(len(rows), totals), *(escape(note) for note in notes)]
    return "\n".join(table) + "\n\n" + "\n\n".join(paragraphs) + "\n"


def list_json(rows: Sequence[_render.ListRow], *, ascii_only: bool) -> str:
    """Write the datasets as a JSON array of objects.

    Parameters
    ----------
    rows : sequence of ListRow
        The rows, in the order they are shown.
    ascii_only : bool
        Write every character outside ASCII as an escape. This is for the terminal, whose
        code page may not have the character. A file is written in UTF-8 as it is.

    Returns
    -------
    str
        The JSON text with a newline at the end.
    """
    data = [
        {
            "name": row.name,
            "task": row.task,
            "license": row.license,
            "samples": row.n_samples,
            "features": row.n_features,
            "has_missing": row.has_missing,
        }
        for row in rows
    ]
    return json.dumps(data, indent=2, ensure_ascii=ascii_only) + "\n"


def show_json(
    info: DatasetInfo,
    *,
    shape: tuple[int, int],
    size: int,
    feature_names: Sequence[str],
    target_names: Sequence[str] | None,
    ascii_only: bool,
) -> str:
    """Write the facts about one dataset as a JSON object with all of them.

    Parameters
    ----------
    info : DatasetInfo
        Provenance and license of the dataset. Every field is written.
    shape : tuple of int
        Number of samples and number of features.
    size : int
        Size of the data file in bytes.
    feature_names : sequence of str
        Names of the columns of ``X``.
    target_names : sequence of str or None
        Class or target names, ``None`` if the dataset has none.
    ascii_only : bool
        Write every character outside ASCII as an escape, see :func:`list_json`.

    Returns
    -------
    str
        The JSON text with a newline at the end.
    """
    data = info.to_dict()
    data.update(
        n_samples=shape[0],
        n_features=shape[1],
        feature_names=list(feature_names),
        target_names=None if target_names is None else list(target_names),
        size_bytes=size,
    )
    return json.dumps(data, indent=2, ensure_ascii=ascii_only) + "\n"


def show_markdown(
    info: DatasetInfo,
    *,
    shape: tuple[int, int],
    size: int,
    feature_names: Sequence[str],
    target_names: Sequence[str] | None,
    full: bool,
) -> str:
    """Write the report about one dataset in Markdown, in the style of ``NOTICE.md``.

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
    full : bool
        Add the changes made to the data and the notes. Without it a sentence says how many
        there are.

    Returns
    -------
    str
        The report. Lines are not wrapped.
    """
    categorical = [name for name in feature_names if name in info.categorical]
    numeric = [name for name in feature_names if name not in info.categorical]
    kinds = (
        f"{shape[1]} ({len(categorical)} categorical, {len(numeric)} numeric)"
        if categorical
        else f"{shape[1]} (all numeric)"
    )
    lines = [
        f"# {info.title} (`{info.name}`)",
        "",
        info.summary,
        "",
        f"- **Task:** {info.task}",
        f"- **License:** [{info.license}]({info.license_url})",
        "",
        "## Overview",
        "",
        f"- **Samples:** {shape[0]}",
        f"- **Features:** {kinds}",
    ]
    if target_names is not None:
        label = "Classes" if info.task == "classification" else "Targets"
        lines.append(f"- **{label}:** {', '.join(target_names)}")
    lines += [
        f"- **Missing:** {'yes, stored as NaN' if info.has_missing else 'no'}",
        f"- **File size:** {_render.size_text(size)}",
        "",
        "## Provenance",
        "",
        f"- **Source:** [{info.source}]({info.source_url})",
        f"- **License checked:** {info.verified_on}",
    ]
    if info.doi:
        lines.append(f"- **DOI:** [{info.doi}](https://doi.org/{info.doi})")
    lines += [f"- **Creators:** {', '.join(info.creators)}", "", "## Features", ""]
    if numeric:
        lines.append(f"- **Numeric ({len(numeric)}):** {', '.join(numeric)}")
    if categorical:
        lines.append(f"- **Categorical ({len(categorical)}):** {', '.join(categorical)}")
    lines += ["", "## Citation", "", _link_addresses(info.citation), ""]
    if full:
        lines += ["## Changes made to the data", ""]
        lines += [f"- {_link_addresses(change)}" for change in info.changes]
        if info.notes:
            lines += ["", "## Notes", ""]
            lines += [f"- {_link_addresses(note)}" for note in info.notes]
    else:
        lines.append(escape(_render.hidden_message(info)))
    return "\n".join(lines) + "\n"
