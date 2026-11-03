"""Recipe for the Statlog German Credit Data dataset from the UCI Machine Learning Repository."""

from collections.abc import Sequence
from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from pyml_datasets.datasets.german_credit import INFO
from scripts.recipes._common import Built

_UCI_ID: Final = 144
_EXPECTED_SHAPE: Final = (1000, 20)

# UCI calls the columns Attribute1 to Attribute20, in the order of the source description.
_SOURCE_COLUMNS: Final = tuple(f"Attribute{number}" for number in range(1, 21))
_FEATURE_NAMES: Final = (
    "checking_status",
    "duration",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings",
    "employment_since",
    "installment_rate",
    "personal_status_sex",
    "other_debtors",
    "residence_since",
    "property",
    "age",
    "other_installment_plans",
    "housing",
    "existing_credits",
    "job",
    "people_liable",
    "telephone",
    "foreign_worker",
)
# Numeric features that must be positive: a duration, an amount and an age cannot be zero.
_POSITIVE_FEATURES: Final = frozenset({"duration", "credit_amount", "age"})
_TARGET_COLUMN: Final = "class"
# The source codes the classes 1 and 2, the file stores 0 and 1 in the same order.
_TARGET_CODES: Final = {1: 0, 2: 1}
_TARGET_CLASSES: Final = ("good", "bad")


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
    """Convert the codes of the source (``A11``, ``A12``, ...) to the integer codes of the file.

    Every category name starts with the code of the source, up to the first colon, and the
    integer code of a cell is the index of its category in ``categories``.

    Parameters
    ----------
    values : sequence of object
        Cells of the column, the codes of the source.
    name : str
        Feature name, used in error messages.
    categories : sequence of str
        Category names of the feature, from ``INFO.categorical``.

    Returns
    -------
    ndarray of shape (n_samples,)
        Integer code of every cell.

    Raises
    ------
    ValueError
        If a cell is missing or is not one of the codes of the feature.
    """
    index = {category.split(":", 1)[0]: code for code, category in enumerate(categories)}
    codes = np.empty(len(values), dtype=np.int64)
    for row, value in enumerate(values):
        if _is_missing(value):
            raise ValueError(f"german_credit: {name} has a missing value in row {row}.")
        text = str(value).strip()
        if text not in index:
            raise ValueError(
                f"german_credit: unknown {name} {text!r}, expected one of {tuple(index)}."
            )
        codes[row] = index[text]
    return codes


def _numeric(values: NDArray[np.float64], name: str) -> NDArray[np.float64]:
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
        If the column has missing values, values that are not whole numbers, negative
        values, or zeros in a feature that must be positive.
    """
    if np.isnan(values).any():
        raise ValueError(f"german_credit: {name} has missing values.")
    if not np.all(values == np.round(values)):
        raise ValueError(f"german_credit: {name} must hold whole numbers only.")
    if values.min() < 0 or (name in _POSITIVE_FEATURES and values.min() == 0):
        raise ValueError(f"german_credit: {name} has values outside its range.")
    return values


def build() -> Built:
    """Download German Credit from the UCI repository and return it as a ``Built`` object.

    The shape, the column names, the codes of the categorical features, the whole numbers of
    the numeric features and the values of the target are checked, so a silent change of the
    data on the UCI side is noticed instead of being saved. Categorical features become
    integer codes in the order of ``INFO.categorical``. The class of the source, 1 for good
    and 2 for bad, is stored as 0 and 1.

    Returns
    -------
    Built
        Features as a ``(1000, 20)`` matrix without missing values, and the credit risk
        (0 for good, 1 for bad) as the class.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape, columns, codes or value
        ranges.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("german_credit: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"german_credit: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if list(features.columns) != list(_SOURCE_COLUMNS):
        raise ValueError(f"german_credit: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_TARGET_COLUMN] or len(targets) != len(features):
        raise ValueError(
            f"german_credit: expected a single {_TARGET_COLUMN!r} target, one value per row."
        )

    columns: list[NDArray[np.float64]] = []
    for source, name in zip(_SOURCE_COLUMNS, _FEATURE_NAMES, strict=True):
        if name in INFO.categorical:
            codes = _encode(features[source].tolist(), name, INFO.categorical[name])
            columns.append(codes.astype(np.float64))
        else:
            columns.append(_numeric(features[source].to_numpy(dtype=np.float64), name))

    raw = targets[_TARGET_COLUMN].to_numpy(dtype=np.float64)
    if np.isnan(raw).any() or not np.all(np.isin(raw, tuple(_TARGET_CODES))):
        raise ValueError(f"german_credit: the target must hold only {tuple(_TARGET_CODES)}.")
    y = np.array([_TARGET_CODES[int(value)] for value in raw], dtype=np.int64)
    if np.unique(y).size != len(_TARGET_CLASSES):
        raise ValueError("german_credit: both classes, good and bad, must be present.")

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=_FEATURE_NAMES,
        target_names=_TARGET_CLASSES,
        extras={
            "source": "UCI Machine Learning Repository, dataset 144",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
