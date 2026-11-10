"""Recipe for the Mushroom dataset from the UCI Machine Learning Repository."""

from collections.abc import Sequence
from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from pyml_datasets.datasets.mushroom import INFO
from scripts.recipes._common import Built

_UCI_ID: Final = 73
_EXPECTED_SHAPE: Final = (8124, 22)

# Column names as UCI gives them, in the order they are stored in X.
_SOURCE_COLUMNS: Final = (
    "cap-shape",
    "cap-surface",
    "cap-color",
    "bruises",
    "odor",
    "gill-attachment",
    "gill-spacing",
    "gill-size",
    "gill-color",
    "stalk-shape",
    "stalk-root",
    "stalk-surface-above-ring",
    "stalk-surface-below-ring",
    "stalk-color-above-ring",
    "stalk-color-below-ring",
    "veil-type",
    "veil-color",
    "ring-number",
    "ring-type",
    "spore-print-color",
    "population",
    "habitat",
)
# Names stored in the file: the hyphens become underscores, see INFO.changes.
_FEATURE_NAMES: Final = tuple(name.replace("-", "_") for name in _SOURCE_COLUMNS)
_SOURCE_TARGET: Final = "poisonous"
# The only feature where the source marks entries as missing. UCI delivers them as empty
# cells, the text "?" of the source file is accepted as well, both are stored as NaN.
_MISSING_FEATURES: Final = frozenset({"stalk_root"})
_MISSING_MARK: Final = "?"
# Target labels of the source, in the order of the class codes: edible=e, poisonous=p.
_TARGET_LABELS: Final = ("e", "p")
_TARGET_CLASSES: Final = ("edible", "poisonous")


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
                raise ValueError(f"mushroom: {name} has a missing value in row {row}.")
            codes[row] = np.nan
            continue
        if str(value) not in index:
            raise ValueError(
                f"mushroom: unknown {name} {value!r}, expected one of {tuple(categories)}."
            )
        codes[row] = index[str(value)]
    return codes


def _target_codes(values: Sequence[object]) -> NDArray[np.int64]:
    """Convert the labels ``e`` and ``p`` to the codes 0 (edible) and 1 (poisonous).

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
    index = {label: code for code, label in enumerate(_TARGET_LABELS)}
    codes = np.empty(len(values), dtype=np.int64)
    for row, value in enumerate(values):
        if _is_missing(value):
            raise ValueError(f"mushroom: poisonous has a missing value in row {row}.")
        if str(value) not in index:
            raise ValueError(
                f"mushroom: unknown poisonous {value!r}, expected one of {_TARGET_LABELS}."
            )
        codes[row] = index[str(value)]
    return codes


def build() -> Built:
    """Download Mushroom from the UCI repository and return it as a ``Built`` object.

    The shape, the column names and the categories of every feature are checked, so a silent
    change of the data on the UCI side is noticed instead of being saved. Categorical
    features become integer codes in the order of ``INFO.categorical``. Missing entries of
    ``stalk_root``, delivered as empty cells or as the text ``?``, are stored as ``NaN``.

    Returns
    -------
    Built
        Features as an ``(8124, 22)`` matrix with ``NaN`` for missing entries, and the class
        (0 for edible, 1 for poisonous) as the target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape, columns, categories or
        labels.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("mushroom: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"mushroom: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if list(features.columns) != list(_SOURCE_COLUMNS):
        raise ValueError(f"mushroom: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_SOURCE_TARGET] or len(targets) != len(features):
        raise ValueError("mushroom: expected a single 'poisonous' target, one value per row.")
    if set(INFO.categorical) != set(_FEATURE_NAMES):
        raise ValueError("mushroom: every feature must be listed in INFO.categorical.")

    columns = [
        _encode(
            features[source].tolist(),
            name,
            INFO.categorical[name],
            may_be_missing=name in _MISSING_FEATURES,
        )
        for source, name in zip(_SOURCE_COLUMNS, _FEATURE_NAMES, strict=True)
    ]

    y = _target_codes(targets[_SOURCE_TARGET].tolist())
    if np.unique(y).size != len(_TARGET_LABELS):
        raise ValueError("mushroom: both classes, edible and poisonous, must be present.")

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
            "source": "UCI Machine Learning Repository, dataset 73",
            "ucimlrepo_version": version("ucimlrepo"),
            "missing_stored_as_nan": ", ".join(f"{k}={v}" for k, v in missing.items()),
        },
    )
