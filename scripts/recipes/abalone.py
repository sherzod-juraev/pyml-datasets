"""Recipe for the Abalone dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from pyml_datasets.datasets.abalone import INFO
from scripts.recipes._common import Built

_UCI_ID: Final = 1
_EXPECTED_SHAPE: Final = (4177, 8)
_SOURCE_TARGET: Final = "Rings"

# Column names as UCI gives them and the names stored in the file, in the order of the variable
# table of the source. Columns are picked by name, so the order UCI returns them in does not
# matter.
_COLUMNS: Final = (
    ("Sex", "sex"),
    ("Length", "length"),
    ("Diameter", "diameter"),
    ("Height", "height"),
    ("Whole_weight", "whole_weight"),
    ("Shucked_weight", "shucked_weight"),
    ("Viscera_weight", "viscera_weight"),
    ("Shell_weight", "shell_weight"),
)


def _sex_codes(values: list[object]) -> NDArray[np.float64]:
    """Convert the sex of every abalone to the integer code of its category.

    Parameters
    ----------
    values : list of object
        Cells of the ``Sex`` column.

    Returns
    -------
    ndarray of shape (n_samples,)
        Index of each cell in ``INFO.categorical["sex"]``, as floats.

    Raises
    ------
    ValueError
        If a cell is not one of the categories, a missing cell included.
    """
    categories = INFO.categorical["sex"]
    unknown = sorted({str(value) for value in values if value not in categories})
    if unknown:
        raise ValueError(f"abalone: unknown sex {unknown}, expected one of {categories}.")
    return np.array([categories.index(str(value)) for value in values], dtype=np.float64)


def build() -> Built:
    """Download Abalone from the UCI repository and return it as a ``Built`` object.

    The shape, the column names, the categories and the kinds of values are checked, so a
    silent change of the data on the UCI side is noticed instead of being saved. The sex
    becomes integer codes in the order of ``INFO.categorical``. The continuous values are kept
    as UCI gives them, with the scaling that the source describes.

    Returns
    -------
    Built
        Features as a ``(4177, 8)`` matrix without missing values, and the number of rings as
        a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, if the sex is not
        one of the categories, if a measurement is missing, infinite or negative, or if the
        number of rings is not a whole number that is zero or more.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("abalone: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"abalone: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if set(features.columns) != {source for source, _ in _COLUMNS}:
        raise ValueError(f"abalone: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_SOURCE_TARGET] or len(targets) != len(features):
        raise ValueError(
            f"abalone: expected a single {_SOURCE_TARGET!r} target, one value per row."
        )

    columns: list[NDArray[np.float64]] = []
    for source, name in _COLUMNS:
        if name == "sex":
            columns.append(_sex_codes(features[source].tolist()))
            continue
        column = features[source].to_numpy(dtype=np.float64)
        if not np.isfinite(column).all():
            raise ValueError(f"abalone: {name} has missing or infinite values.")
        if column.min() < 0:
            raise ValueError(f"abalone: {name} has negative values.")
        columns.append(column)

    y = targets[_SOURCE_TARGET].to_numpy(dtype=np.float64)
    if not (np.isfinite(y).all() and np.all(y == np.round(y)) and y.min() >= 0):
        raise ValueError("abalone: the number of rings must be a whole number, zero or more.")

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=tuple(name for _, name in _COLUMNS),
        target_names=("rings",),
        extras={
            "source": "UCI Machine Learning Repository, dataset 1",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
