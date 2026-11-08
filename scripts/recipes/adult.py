"""Recipe for the Adult dataset from the UCI Machine Learning Repository."""

from collections.abc import Sequence
from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from pyml_datasets.datasets.adult import INFO
from scripts.recipes._common import Built

_UCI_ID: Final = 2
_EXPECTED_SHAPE: Final = (48842, 14)

# Column names as UCI gives them, in the order they are stored in X.
_SOURCE_COLUMNS: Final = (
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
)
# Names stored in the file: the hyphens become underscores, see INFO.changes.
_FEATURE_NAMES: Final = tuple(name.replace("-", "_") for name in _SOURCE_COLUMNS)
# Features where the source marks entries as missing. UCI delivers them as the text "?" in
# one part of the data and as empty cells in the other part, both are stored as NaN.
_MISSING_FEATURES: Final = frozenset({"workclass", "occupation", "native_country"})
_MISSING_MARK: Final = "?"
# Smallest and largest value of the whole-number features in the source files.
_RANGES: Final = {
    "age": (17, 90),
    "fnlwgt": (12285, 1_490_400),
    "education_num": (1, 16),
    "capital_gain": (0, 99_999),
    "capital_loss": (0, 4356),
    "hours_per_week": (1, 99),
}
_TARGET_CLASSES: Final = ("<=50K", ">50K")


def _is_missing(value: object) -> bool:
    """Tell whether a cell of the UCI table is an empty cell.

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
    may_be_missing: bool,
) -> NDArray[np.float64]:
    """Convert the text cells of a column to the integer codes of their categories.

    Parameters
    ----------
    values : sequence of object
        Cells of the column.
    name : str
        Feature name, used in error messages.
    categories : sequence of str
        Category names, the code of a cell is the index of its text in this sequence.
    may_be_missing : bool
        Store empty cells and the text ``"?"`` as ``NaN`` instead of raising an error.

    Returns
    -------
    ndarray of shape (n_samples,)
        Code of every cell as ``float64``, ``NaN`` for a missing cell.

    Raises
    ------
    ValueError
        If a cell is missing and ``may_be_missing`` is false, or if a cell is not one of
        the categories.
    """
    index = {category: code for code, category in enumerate(categories)}
    codes = np.empty(len(values), dtype=np.float64)
    for row, value in enumerate(values):
        if _is_missing(value) or value == _MISSING_MARK:
            if not may_be_missing:
                raise ValueError(f"adult: {name} has a missing value in row {row}.")
            codes[row] = np.nan
            continue
        if str(value) not in index:
            raise ValueError(
                f"adult: unknown {name} {value!r}, expected one of {tuple(categories)}."
            )
        codes[row] = index[str(value)]
    return codes


def _whole_numbers(values: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    """Check that a numeric column holds whole numbers inside its range, without gaps.

    Parameters
    ----------
    values : ndarray of shape (n_samples,)
        Column converted to ``float64``.
    name : str
        Feature name, used in error messages and to find the range in ``_RANGES``.

    Returns
    -------
    ndarray of shape (n_samples,)
        The same column.

    Raises
    ------
    ValueError
        If the column has missing values, values that are not whole numbers, or values
        outside the range of the source files.
    """
    if np.isnan(values).any():
        raise ValueError(f"adult: {name} has missing values.")
    if not np.all(values == np.round(values)):
        raise ValueError(f"adult: {name} must hold whole numbers only.")
    low, high = _RANGES[name]
    if values.min() < low or values.max() > high:
        raise ValueError(f"adult: {name} must be between {low} and {high}.")
    return values


def _target_codes(values: Sequence[object]) -> NDArray[np.int64]:
    """Convert the income labels to the codes 0 (``<=50K``) and 1 (``>50K``).

    The test part of the source writes the labels with a trailing dot, which is dropped.

    Parameters
    ----------
    values : sequence of object
        Cells of the target column.

    Returns
    -------
    ndarray of shape (n_samples,)
        Class code of every sample.

    Raises
    ------
    ValueError
        If a label is missing or is not one of the two classes.
    """
    index = {label: code for code, label in enumerate(_TARGET_CLASSES)}
    codes = np.empty(len(values), dtype=np.int64)
    for row, value in enumerate(values):
        if _is_missing(value):
            raise ValueError(f"adult: income has a missing value in row {row}.")
        label = str(value).removesuffix(".")
        if label not in index:
            raise ValueError(f"adult: unknown income {value!r}, expected one of {_TARGET_CLASSES}.")
        codes[row] = index[label]
    return codes


def build() -> Built:
    """Download Adult from the UCI repository and return it as a ``Built`` object.

    The shape, the column names, the categories and the ranges of the whole-number features
    are checked, and so is the link between ``education`` and ``education_num``, so a silent
    change of the data on the UCI side is noticed instead of being saved. Categorical
    features become integer codes in the order of ``INFO.categorical``. Missing entries of
    ``workclass``, ``occupation`` and ``native_country``, delivered as the text ``?`` or as
    empty cells, are stored as ``NaN``. The trailing dot of the test labels is dropped.

    Returns
    -------
    Built
        Features as a ``(48842, 14)`` matrix with ``NaN`` for missing entries, and the
        income class (0 for ``<=50K``, 1 for ``>50K``) as the class.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape, columns, categories, value
        ranges or labels.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("adult: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"adult: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if list(features.columns) != list(_SOURCE_COLUMNS):
        raise ValueError(f"adult: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != ["income"] or len(targets) != len(features):
        raise ValueError("adult: expected a single 'income' target, one value per row.")

    columns: list[NDArray[np.float64]] = []
    for source, name in zip(_SOURCE_COLUMNS, _FEATURE_NAMES, strict=True):
        if name in INFO.categorical:
            columns.append(
                _encode(
                    features[source].tolist(),
                    name,
                    INFO.categorical[name],
                    may_be_missing=name in _MISSING_FEATURES,
                )
            )
        else:
            columns.append(_whole_numbers(features[source].to_numpy(dtype=np.float64), name))

    education = columns[_FEATURE_NAMES.index("education")]
    education_num = columns[_FEATURE_NAMES.index("education_num")]
    if not np.array_equal(education + 1, education_num):
        raise ValueError("adult: education_num must be the code of education plus one.")

    y = _target_codes(targets["income"].tolist())
    if np.unique(y).size != len(_TARGET_CLASSES):
        raise ValueError("adult: both classes, <=50K and >50K, must be present.")

    X = np.column_stack(columns)
    missing = {
        name: int(np.isnan(X[:, column]).sum())
        for column, name in enumerate(_FEATURE_NAMES)
        if name in _MISSING_FEATURES
    }
    return Built(
        X=X,
        y=y,
        feature_names=_FEATURE_NAMES,
        target_names=_TARGET_CLASSES,
        extras={
            "source": "UCI Machine Learning Repository, dataset 2",
            "ucimlrepo_version": version("ucimlrepo"),
            "missing_stored_as_nan": ", ".join(f"{k}={v}" for k, v in missing.items()),
        },
    )
