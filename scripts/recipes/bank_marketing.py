"""Recipe for the Bank Marketing dataset from the UCI Machine Learning Repository."""

from collections.abc import Sequence
from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from pyml_datasets.datasets.bank_marketing import INFO
from scripts.recipes._common import Built

_UCI_ID: Final = 222
_EXPECTED_SHAPE: Final = (45211, 16)

# Column names as UCI gives them, in the order they are stored in X.
_SOURCE_COLUMNS: Final = (
    "age",
    "job",
    "marital",
    "education",
    "default",
    "balance",
    "housing",
    "loan",
    "contact",
    "day_of_week",
    "month",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
)
# Names stored in the file: UCI's day_of_week holds the day of the month, see INFO.changes.
_FEATURE_NAMES: Final = tuple("day" if name == "day_of_week" else name for name in _SOURCE_COLUMNS)
# Features where UCI marks entries as missing and the category "unknown" takes their place.
_UNKNOWN_FEATURES: Final = frozenset({"job", "education", "contact", "poutcome"})
_UNKNOWN: Final = "unknown"
_TARGET_CLASSES: Final = ("no", "yes")


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
    *,
    fill_unknown: bool = False,
) -> tuple[NDArray[np.int64], int]:
    """Convert the text cells of a column to the integer codes of their categories.

    Parameters
    ----------
    values : sequence of object
        Cells of the column.
    name : str
        Feature name, used in error messages.
    categories : sequence of str
        Category names, the code of a cell is the index of its text in this sequence.
    fill_unknown : bool, default=False
        Store missing cells as the category ``"unknown"`` instead of raising an error.

    Returns
    -------
    codes : ndarray of shape (n_samples,)
        Integer code of every cell.
    n_filled : int
        Number of missing cells that were stored as ``"unknown"``.

    Raises
    ------
    ValueError
        If a cell is missing and ``fill_unknown`` is false, or if a cell is not one of
        the categories.
    """
    index = {category: code for code, category in enumerate(categories)}
    codes = np.empty(len(values), dtype=np.int64)
    n_filled = 0
    for row, value in enumerate(values):
        if _is_missing(value):
            if not fill_unknown:
                raise ValueError(f"bank_marketing: {name} has a missing value in row {row}.")
            value = _UNKNOWN
            n_filled += 1
        if value not in index:
            raise ValueError(
                f"bank_marketing: unknown {name} {value!r}, expected one of {tuple(categories)}."
            )
        codes[row] = index[str(value)]
    return codes, n_filled


def _whole_numbers(values: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    """Check that a numeric column has no missing values and holds whole numbers only.

    Parameters
    ----------
    values : ndarray of shape (n_samples,)
        Column converted to ``float64``.
    name : str
        Feature name, used in error messages.

    Returns
    -------
    ndarray of shape (n_samples,)
        The same column.

    Raises
    ------
    ValueError
        If the column has missing values or values that are not whole numbers.
    """
    if np.isnan(values).any():
        raise ValueError(f"bank_marketing: {name} has missing values.")
    if not np.all(values == np.round(values)):
        raise ValueError(f"bank_marketing: {name} must hold whole numbers only.")
    return values


def build() -> Built:
    """Download Bank Marketing from the UCI repository and return it as a ``Built`` object.

    The shape, the column names, the categories and the ranges of the day and the target
    are checked, so a silent change of the data on the UCI side is noticed instead of being
    saved. Categorical features become integer codes in the order of ``INFO.categorical``.
    Entries of ``job``, ``education``, ``contact`` and ``poutcome`` that UCI marks as missing
    are stored as the category ``"unknown"``.

    Returns
    -------
    Built
        Features as a ``(45211, 16)`` matrix without missing values, and the answer of the
        client (0 for no, 1 for yes) as the class.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape, columns, categories or
        value ranges.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("bank_marketing: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"bank_marketing: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if set(features.columns) != set(_SOURCE_COLUMNS):
        raise ValueError(f"bank_marketing: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != ["y"] or len(targets) != len(features):
        raise ValueError("bank_marketing: expected a single 'y' target, one value per row.")

    columns: list[NDArray[np.float64]] = []
    filled: dict[str, int] = {}
    for source, name in zip(_SOURCE_COLUMNS, _FEATURE_NAMES, strict=True):
        if name in INFO.categorical:
            codes, n_filled = _encode(
                features[source].tolist(),
                name,
                INFO.categorical[name],
                fill_unknown=name in _UNKNOWN_FEATURES,
            )
            columns.append(codes.astype(np.float64))
            if n_filled:
                filled[name] = n_filled
        else:
            columns.append(
                _whole_numbers(features[source].to_numpy(dtype=np.float64), name),
            )

    day = columns[_FEATURE_NAMES.index("day")]
    if not (day.min() >= 1 and day.max() <= 31 and day.max() > 7):
        raise ValueError("bank_marketing: day must be the day of the month, between 1 and 31.")

    y, _ = _encode(targets["y"].tolist(), "y", _TARGET_CLASSES)
    if np.unique(y).size != len(_TARGET_CLASSES):
        raise ValueError("bank_marketing: both classes, no and yes, must be present.")

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=_FEATURE_NAMES,
        target_names=_TARGET_CLASSES,
        extras={
            "source": "UCI Machine Learning Repository, dataset 222",
            "ucimlrepo_version": version("ucimlrepo"),
            "missing_stored_as_unknown": ", ".join(f"{k}={v}" for k, v in filled.items()),
        },
    )
