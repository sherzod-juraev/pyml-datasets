"""Text generated from ``DatasetInfo``: descriptions, notices, tables and documentation includes.

Everything that states the origin or the license of a dataset is produced here from the
single ``DatasetInfo`` of the dataset, so the same fact is never written twice by hand.
"""

import json
import textwrap
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

import numpy as np

from pyml_datasets import Dataset, DatasetInfo

_LICENSE_NAMES: Final = {"CC-BY-4.0": "CC BY 4.0", "CC0-1.0": "CC0 1.0"}
_WIDTH: Final = 88


@dataclass(frozen=True)
class Facts:
    """Numbers that describe the stored data of a dataset.

    Attributes
    ----------
    n_samples : int
        Number of rows of ``X``.
    n_features : int
        Number of columns of ``X``.
    n_targets : int
        Number of target columns (1 for a one-dimensional ``y``).
    n_classes : int or None
        Number of classes for classification, ``None`` for regression.
    missing : int
        Number of ``NaN`` values in ``X``.
    missing_columns : int
        Number of columns of ``X`` that contain at least one ``NaN``.
    """

    n_samples: int
    n_features: int
    n_targets: int
    n_classes: int | None
    missing: int
    missing_columns: int


def facts_of(data: Dataset) -> Facts:
    """Compute the ``Facts`` of a loaded dataset.

    Parameters
    ----------
    data : Dataset
        A loaded dataset.

    Returns
    -------
    Facts
        Shape, class and missing value counts.
    """
    nan = np.isnan(data.X)
    n_classes = int(np.unique(data.y).size) if data.info.task == "classification" else None
    return Facts(
        n_samples=int(data.X.shape[0]),
        n_features=int(data.X.shape[1]),
        n_targets=1 if data.y.ndim == 1 else int(data.y.shape[1]),
        n_classes=n_classes,
        missing=int(nan.sum()),
        missing_columns=int(nan.any(axis=0).sum()),
    )


def license_name(license_id: str) -> str:
    """Return the readable name of a license identifier.

    Parameters
    ----------
    license_id : str
        SPDX identifier, for example ``"CC-BY-4.0"``.

    Returns
    -------
    str
        Readable name, for example ``"CC BY 4.0"``.
    """
    return _LICENSE_NAMES[license_id]


def info_json(info: DatasetInfo) -> str:
    """Serialize a ``DatasetInfo`` as the JSON text stored in the data file.

    Parameters
    ----------
    info : DatasetInfo
        Provenance of the dataset.

    Returns
    -------
    str
        JSON with sorted keys, so equal information always gives equal text.
    """
    return json.dumps(info.to_dict(), sort_keys=True, ensure_ascii=False)


def _wrap(text: str, *, first: str = "", rest: str = "") -> str:
    """Wrap a paragraph without splitting words, so long addresses stay intact.

    Parameters
    ----------
    text : str
        Paragraph to wrap.
    first : str, default=""
        Prefix of the first line.
    rest : str, default=""
        Prefix of the other lines.

    Returns
    -------
    str
        The wrapped paragraph.
    """
    return textwrap.fill(
        text,
        width=_WIDTH,
        initial_indent=first,
        subsequent_indent=rest,
        break_long_words=False,
        break_on_hyphens=False,
    )


def _bullets(items: Sequence[str], *, indent: str = "  ") -> list[str]:
    """Format items as a wrapped bullet list.

    Parameters
    ----------
    items : sequence of str
        The items.
    indent : str, default="  "
        Indentation of every line.

    Returns
    -------
    list of str
        Lines of the list.
    """
    return [_wrap(item, first=f"{indent}- ", rest=f"{indent}  ") for item in items]


def render_description(info: DatasetInfo) -> str:
    """Write the plain text description that is stored inside the data file.

    Parameters
    ----------
    info : DatasetInfo
        Provenance of the dataset.

    Returns
    -------
    str
        Description with the source, the citation, the license and the changes.
    """
    lines = [info.title, "", _wrap(info.summary), ""]
    lines += [_wrap(f"Source: {info.source}, {info.source_url}", rest="  ")]
    lines += [_wrap(f"Obtained from: {info.obtained_from}", rest="  ")]
    lines += [_wrap(f"Creators: {', '.join(info.creators)}", rest="  "), ""]
    lines += ["Citation:", _wrap(info.citation, first="  ", rest="  "), ""]
    lines += [
        _wrap(
            f"License: {license_name(info.license)} ({info.license_url}). "
            f"Checked at the source on {info.verified_on}.",
            rest="  ",
        ),
        "",
        "Changes made to the data:",
        *_bullets(info.changes),
    ]
    if info.has_missing:
        lines += ["", "Missing values are stored as NaN in X."]
    if info.categorical:
        lines += ["", "Categorical features, stored as integer codes in X:"]
        for feature, categories in info.categorical.items():
            names = ", ".join(f"{code} = {name}" for code, name in enumerate(categories))
            lines.append(_wrap(f"{feature}: {names}", first="  ", rest="    "))
    if info.notes:
        lines += ["", "Notes:", *_bullets(info.notes)]
    if info.references:
        lines += ["", "References:", *_bullets(info.references)]
    return "\n".join(lines) + "\n"


def render_notice(infos: Sequence[DatasetInfo]) -> str:
    """Write ``NOTICE.md``, the attribution notice shipped in the wheel.

    Parameters
    ----------
    infos : sequence of DatasetInfo
        Information of every bundled dataset.

    Returns
    -------
    str
        Markdown text.
    """
    lines = [
        "# Notice: licenses and attribution of the bundled datasets",
        "",
        "<!-- Generated by `python -m scripts.generate` from the dataset information in "
        "pyml_datasets/datasets/. Do not edit it by hand. -->",
        "",
        "The code of pyml-datasets is released under the MIT license, see `LICENSE`. The "
        "datasets were created by other people. Each one is redistributed under the license it "
        "has at its source, and the changes made to it are listed here, as these licenses "
        "require. The license texts are in the `LICENSES` folder.",
    ]
    for info in sorted(infos, key=lambda item: item.name):
        lines += [
            "",
            f"## {info.title} (`{info.name}`)",
            "",
            f"- **License:** [{license_name(info.license)}]({info.license_url})",
            f"- **Creators:** {', '.join(info.creators)}",
            f"- **Source:** [{info.source}]({info.source_url})",
            f"- **Obtained from:** {info.obtained_from}",
            f"- **Citation:** {info.citation}",
            "- **Changes made:**",
            *[f"  - {change}" for change in info.changes],
        ]
        if info.notes:
            lines += ["- **Notes:**", *[f"  - {note}" for note in info.notes]]
    return "\n".join(lines) + "\n"


def render_readme_table(facts: dict[str, Facts], infos: Sequence[DatasetInfo]) -> str:
    """Write the table of datasets for the README.

    Parameters
    ----------
    facts : dict of str to Facts
        Facts of every dataset, by name.
    infos : sequence of DatasetInfo
        Information of every bundled dataset.

    Returns
    -------
    str
        Markdown table.
    """
    lines = [
        "| Function | Task | Samples × features | Missing values | License |",
        "|:---------|:-----|:------------------:|:--------------:|:-------:|",
    ]
    for info in sorted(infos, key=lambda item: item.name):
        fact = facts[info.name]
        missing = "yes" if info.has_missing else "no"
        lines.append(
            f"| `load_{info.name}` | {info.task.capitalize()} "
            f"| {fact.n_samples} × {fact.n_features} | {missing} "
            f"| {license_name(info.license)} |"
        )
    return "\n".join(lines) + "\n"


def _targets_cell(data: Dataset, fact: Facts) -> str:
    """Describe the targets of a dataset for the overview table.

    Parameters
    ----------
    data : Dataset
        A loaded dataset.
    fact : Facts
        Facts of the dataset.

    Returns
    -------
    str
        Text in reStructuredText.
    """
    names = data.target_names or ()
    if data.info.task == "classification":
        classes = ", ".join(f"``{name}`` ({code})" for code, name in enumerate(names))
        return f"{fact.n_classes} classes: {classes}"
    if fact.n_targets == 1:
        return "1 continuous target" + (f", ``{names[0]}``" if names else "")
    listed = ", ".join(f"``{name}``" for name in names)
    return f"{fact.n_targets} continuous targets" + (f": {listed}" if names else "")


def render_overview(data: Dataset, fact: Facts) -> str:
    """Write the overview table of a dataset page.

    Parameters
    ----------
    data : Dataset
        A loaded dataset.
    fact : Facts
        Facts of the dataset.

    Returns
    -------
    str
        reStructuredText that is included in the page of the dataset.
    """
    info = data.info
    if info.has_missing:
        missing = f"{fact.missing} values in {fact.missing_columns} columns, stored as ``NaN``"
    else:
        missing = "None"
    rows = [
        ("Loader", f"``load_{info.name}()``"),
        ("Task", info.task.capitalize()),
        ("Samples", str(fact.n_samples)),
        ("Features", str(fact.n_features)),
        ("Targets", _targets_cell(data, fact)),
        ("Missing values", missing),
        ("License", license_name(info.license)),
    ]
    lines = [".. list-table::", "   :widths: 25 75", ""]
    for label, value in rows:
        lines += [f"   * - {label}", f"     - {value}"]
    return "\n".join(lines) + "\n"


def render_provenance(info: DatasetInfo) -> str:
    """Write the source, citation, license and changes sections of a dataset page.

    Parameters
    ----------
    info : DatasetInfo
        Provenance of the dataset.

    Returns
    -------
    str
        reStructuredText that is included in the page of the dataset.
    """
    doi = f"https://doi.org/{info.doi}" if info.doi else None
    lines = [
        "Source and citation",
        "-------------------",
        "",
        f"* Source: `{info.source} <{info.source_url}>`__",
        f"* Obtained from: {info.obtained_from}",
        f"* Creators: {', '.join(info.creators)}",
    ]
    if doi:
        lines.append(f"* DOI: {doi}")
    lines += ["", "Please cite the dataset as:", "", f"   {info.citation}", ""]
    if info.references:
        lines += ["See also:", ""]
        lines += [f"* {reference}" for reference in info.references]
        lines.append("")
    lines += [
        "License",
        "-------",
        "",
        f"`{license_name(info.license)} <{info.license_url}>`__, as stated by the source. "
        f"The license was checked at the source on {info.verified_on}. See :doc:`/license`.",
        "",
        "Changes made",
        "~~~~~~~~~~~~",
        "",
    ]
    lines += [f"* {change}" for change in info.changes]
    for note in info.notes:
        lines += ["", ".. note::", "", f"   {note}"]
    return "\n".join(lines) + "\n"


def render_datasets_table(datas: Sequence[Dataset], facts: dict[str, Facts]) -> str:
    """Write the table of the datasets index page.

    Parameters
    ----------
    datas : sequence of Dataset
        Every bundled dataset.
    facts : dict of str to Facts
        Facts of every dataset, by name.

    Returns
    -------
    str
        reStructuredText that is included in the datasets index.
    """
    lines = [
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 30 17 10 10 15 18",
        "",
        "   * - Dataset",
        "     - Task",
        "     - Samples",
        "     - Features",
        "     - Missing values",
        "     - License",
    ]
    for data in sorted(datas, key=lambda item: item.info.name):
        info, fact = data.info, facts[data.info.name]
        lines += [
            f"   * - :doc:`{info.title} </datasets/{info.name}>`",
            f"     - {info.task.capitalize()}",
            f"     - {fact.n_samples}",
            f"     - {fact.n_features}",
            f"     - {'Yes' if info.has_missing else 'No'}",
            f"     - {license_name(info.license)}",
        ]
    return "\n".join(lines) + "\n"


def render_license_table(infos: Sequence[DatasetInfo]) -> str:
    """Write the table of licenses of the license page.

    Parameters
    ----------
    infos : sequence of DatasetInfo
        Information of every bundled dataset.

    Returns
    -------
    str
        reStructuredText that is included in the license page.
    """
    lines = [
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 28 14 58",
        "",
        "   * - Dataset",
        "     - License",
        "     - Original source",
    ]
    for info in sorted(infos, key=lambda item: item.name):
        lines += [
            f"   * - :doc:`{info.title} </datasets/{info.name}>`",
            f"     - {license_name(info.license)}",
            f"     - `{info.source} <{info.source_url}>`__",
        ]
    return "\n".join(lines) + "\n"


def render_api_loaders(infos: Sequence[DatasetInfo]) -> str:
    """Write the ``autofunction`` entries of the API reference.

    Parameters
    ----------
    infos : sequence of DatasetInfo
        Information of every bundled dataset.

    Returns
    -------
    str
        reStructuredText that is included in the API reference.
    """
    entries = [
        f".. autofunction:: pyml_datasets.load_{info.name}\n"
        for info in sorted(infos, key=lambda item: item.name)
    ]
    return "\n".join(entries)
