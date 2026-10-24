"""Recipe for the Auto MPG dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 9
_EXPECTED_SHAPE: Final = (398, 7)
# The data description of the source: "horsepower has 6 missing values".
_N_MISSING: Final = 6

# Features in the order they are stored in X: the order of the data description of the source.
# Columns are picked by name, so the order in which UCI returns them does not matter.
_FEATURE_NAMES: Final = (
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "acceleration",
    "model_year",
    "origin",
)
# Only this feature may hold missing values.
_MAY_BE_MISSING: Final = "horsepower"
# Multi-valued discrete features of the source, they hold whole numbers.
_WHOLE_NUMBERS: Final = frozenset({"cylinders", "model_year", "origin"})


def build() -> Built:
    """Download Auto MPG from the UCI repository and return it as a ``Built`` object.

    The shape, the column names, the missing values and the kinds of values are checked, so a
    silent change of the data on the UCI side is noticed instead of being saved. The identifier
    ``car_name`` is not a feature and is not stored. All features keep the numbers of the
    source, and the missing horsepower values stay ``NaN``.

    Returns
    -------
    Built
        Features as a ``(398, 7)`` matrix with 6 ``NaN`` in ``horsepower``, and the fuel
        consumption in miles per gallon as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, if a feature other
        than ``horsepower`` has missing values, if ``horsepower`` does not have exactly the 6
        missing values the source documents, if a discrete feature holds other than whole
        numbers, or if the target is missing or not positive.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("auto_mpg: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"auto_mpg: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if set(features.columns) != set(_FEATURE_NAMES):
        raise ValueError(f"auto_mpg: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != ["mpg"] or len(targets) != len(features):
        raise ValueError("auto_mpg: expected a single 'mpg' target, one value per row.")

    columns: list[NDArray[np.float64]] = []
    for name in _FEATURE_NAMES:
        column = features[name].to_numpy(dtype=np.float64)
        if np.isinf(column).any():
            raise ValueError(f"auto_mpg: {name} has infinite values.")
        n_missing = int(np.isnan(column).sum())
        if n_missing and name != _MAY_BE_MISSING:
            raise ValueError(f"auto_mpg: {name} has missing values.")
        if name == _MAY_BE_MISSING and n_missing != _N_MISSING:
            raise ValueError(
                f"auto_mpg: horsepower should have {_N_MISSING} missing values, got {n_missing}."
            )
        if name in _WHOLE_NUMBERS and not np.all(column == np.round(column)):
            raise ValueError(f"auto_mpg: {name} must hold whole numbers only.")
        columns.append(column)

    y = targets["mpg"].to_numpy(dtype=np.float64)
    if not (np.isfinite(y).all() and y.min() > 0):
        raise ValueError("auto_mpg: mpg must be positive and never missing.")

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=_FEATURE_NAMES,
        target_names=("mpg",),
        extras={
            "source": "UCI Machine Learning Repository, dataset 9",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
