"""Recipe for the Forest Fires dataset from the UCI Machine Learning Repository."""

from collections.abc import Sequence
from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from pyml_datasets.datasets.forest_fires import INFO
from scripts.recipes._common import Built

_UCI_ID: Final = 162
_EXPECTED_SHAPE: Final = (517, 12)

# Column names as UCI gives them, in the order of the variables table. They are also the names
# stored in the file. Columns are picked by name, so the order in which UCI returns them does
# not matter.
_FEATURE_NAMES: Final = (
    "X",
    "Y",
    "month",
    "day",
    "FFMC",
    "DMC",
    "DC",
    "ISI",
    "temp",
    "RH",
    "wind",
    "rain",
)
_TARGET: Final = "area"
# The ranges that the variables table of the source gives for the numeric columns, borders
# included. A value outside of them means that the data on the UCI side changed.
_RANGES: Final = {
    "X": (1.0, 9.0),
    "Y": (2.0, 9.0),
    "FFMC": (18.7, 96.20),
    "DMC": (1.1, 291.3),
    "DC": (7.9, 860.6),
    "ISI": (0.0, 56.10),
    "temp": (2.2, 33.30),
    "RH": (15.0, 100.0),
    "wind": (0.40, 9.40),
    "rain": (0.0, 6.4),
    _TARGET: (0.0, 1090.84),
}
# The source describes the map coordinates as whole numbers.
_WHOLE_NUMBERS: Final = frozenset({"X", "Y"})
_TOLERANCE: Final = 1e-9


def _is_missing(value: object) -> bool:
    """Tell whether a cell of the UCI table is missing.

    Parameters
    ----------
    value : object
        One cell of a column read from the UCI table.

    Returns
    -------
    bool
        ``True`` for ``None`` and for ``NaN``.
    """
    return value is None or (isinstance(value, float) and value != value)


def _encode(
    values: Sequence[object],
    name: str,
    categories: Sequence[str],
) -> NDArray[np.int64]:
    """Convert the text cells of a column to the integer codes of their categories.

    Parameters
    ----------
    values : sequence of object
        Cells of the column.
    name : str
        Feature name, used in error messages.
    categories : sequence of str
        Category names, the code of a cell is the index of its text in this sequence.

    Returns
    -------
    ndarray of shape (n_samples,)
        Integer code of every cell.

    Raises
    ------
    ValueError
        If a cell is missing or is not one of the categories.
    """
    index = {category: code for code, category in enumerate(categories)}
    codes = np.empty(len(values), dtype=np.int64)
    for row, value in enumerate(values):
        if _is_missing(value):
            raise ValueError(f"forest_fires: {name} has a missing value in row {row}.")
        text = str(value).strip()
        if text not in index:
            raise ValueError(
                f"forest_fires: unknown {name} {text!r}, expected one of {tuple(categories)}."
            )
        codes[row] = index[text]
    return codes


def _numeric(values: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    """Check that a numeric column is finite and inside the range given by the source.

    Parameters
    ----------
    values : ndarray of shape (n_samples,)
        Column converted to ``float64``.
    name : str
        Column name, a key of ``_RANGES``.

    Returns
    -------
    ndarray of shape (n_samples,)
        The same column.

    Raises
    ------
    ValueError
        If the column has missing or infinite values, values outside of the range of the
        source, or, for a map coordinate, values that are not whole numbers.
    """
    if not np.isfinite(values).all():
        raise ValueError(f"forest_fires: {name} has missing or infinite values.")
    low, high = _RANGES[name]
    if values.min() < low - _TOLERANCE or values.max() > high + _TOLERANCE:
        raise ValueError(
            f"forest_fires: {name} is outside of the range {low} to {high} of the source."
        )
    if name in _WHOLE_NUMBERS and not np.all(values == np.round(values)):
        raise ValueError(f"forest_fires: {name} must hold whole numbers only.")
    return values


def build() -> Built:
    """Download Forest Fires from the UCI repository and return it as a ``Built`` object.

    The shape, the column names, the categories of the month and the day, and the ranges of
    the numeric columns and of the target are checked, so a silent change of the data on the
    UCI side is noticed instead of being saved. The month and the day become integer codes in
    the order of ``INFO.categorical``. The burned area is stored as released, without the
    logarithm transform that the source suggests.

    Returns
    -------
    Built
        Features as a ``(517, 12)`` matrix without missing values, and the burned area in
        hectares as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, or if a value is
        missing, infinite, outside of the range of the source or not a category of the source.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("forest_fires: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"forest_fires: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if set(features.columns) != set(_FEATURE_NAMES):
        raise ValueError(f"forest_fires: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_TARGET] or len(targets) != len(features):
        raise ValueError(f"forest_fires: expected a single {_TARGET!r} target, one value per row.")

    columns: list[NDArray[np.float64]] = []
    for name in _FEATURE_NAMES:
        if name in INFO.categorical:
            codes = _encode(features[name].tolist(), name, INFO.categorical[name])
            columns.append(codes.astype(np.float64))
        else:
            columns.append(_numeric(features[name].to_numpy(dtype=np.float64), name))
    y = _numeric(targets[_TARGET].to_numpy(dtype=np.float64), _TARGET)

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=_FEATURE_NAMES,
        target_names=(_TARGET,),
        extras={
            "source": "UCI Machine Learning Repository, dataset 162",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
