"""Recipe for the Palmer Penguins dataset, downloaded from the palmerpenguins repository."""

import csv
import io
from typing import Final

import numpy as np

from pyml_datasets.datasets.penguins import INFO
from scripts.recipes._common import Built
from scripts.recipes._sources import download

_URL: Final = (
    "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv"
)
_SHA256: Final = "f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93"
_COLUMNS: Final = (
    "species",
    "island",
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
    "sex",
    "year",
)
_SPECIES: Final = ("Adelie", "Chinstrap", "Gentoo")
_N_ROWS: Final = 344


def _number(text: str) -> float:
    """Convert a CSV cell to a number, ``NA`` becomes ``NaN``.

    Parameters
    ----------
    text : str
        Content of a numeric cell.

    Returns
    -------
    float
        The number, or ``NaN`` for a missing value.
    """
    return float("nan") if text == "NA" else float(text)


def _category(feature: str, text: str) -> float:
    """Convert a categorical cell to the integer code of its category.

    Parameters
    ----------
    feature : str
        Feature name, a key of ``INFO.categorical``.
    text : str
        Content of the cell.

    Returns
    -------
    float
        Index of the category in ``INFO.categorical[feature]``, or ``NaN`` for ``NA``.

    Raises
    ------
    ValueError
        If the text is not a known category.
    """
    if text == "NA":
        return float("nan")
    categories = INFO.categorical[feature]
    if text not in categories:
        raise ValueError(f"penguins: unknown {feature} {text!r}, expected one of {categories}.")
    return float(categories.index(text))


def build() -> Built:
    """Download the penguins file, check it and return it as a ``Built`` object.

    The file is accepted only if its SHA-256 digest is the pinned one. Its header, its
    number of rows and its species are checked as well.

    Returns
    -------
    Built
        344 samples, 7 features (two of them categorical codes, some values ``NaN``) and the
        species as the class.

    Raises
    ------
    ValueError
        If the file does not have the expected columns, rows or species.
    """
    text = download(_URL, _SHA256).decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    if tuple(reader.fieldnames or ()) != _COLUMNS:
        raise ValueError(f"penguins: unexpected columns {reader.fieldnames}.")
    rows = list(reader)
    if len(rows) != _N_ROWS:
        raise ValueError(f"penguins: expected {_N_ROWS} rows, got {len(rows)}.")

    species = [row["species"] for row in rows]
    if set(species) != set(_SPECIES):
        raise ValueError(f"penguins: unexpected species {sorted(set(species))}.")

    feature_names = _COLUMNS[1:]
    X = np.array(
        [
            [
                _category(name, row[name]) if name in INFO.categorical else _number(row[name])
                for name in feature_names
            ]
            for row in rows
        ],
        dtype=np.float64,
    )
    return Built(
        X=X,
        y=[_SPECIES.index(name) for name in species],
        feature_names=feature_names,
        target_names=_SPECIES,
        extras={"source_url": _URL, "source_sha256": _SHA256},
    )
