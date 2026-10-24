"""Recipe for the Concrete Compressive Strength dataset from the UCI repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 165
_EXPECTED_SHAPE: Final = (1030, 8)
_SOURCE_TARGET: Final = "Concrete compressive strength"
_TARGET_NAME: Final = "concrete_compressive_strength"

# Column names as UCI gives them, in the order of the data description of the source, and the
# names stored in the file. Columns are picked by name, so the order UCI returns them in does
# not matter.
_COLUMNS: Final = (
    ("Cement", "cement"),
    ("Blast Furnace Slag", "blast_furnace_slag"),
    ("Fly Ash", "fly_ash"),
    ("Water", "water"),
    ("Superplasticizer", "superplasticizer"),
    ("Coarse Aggregate", "coarse_aggregate"),
    ("Fine Aggregate", "fine_aggregate"),
    ("Age", "age"),
)
# The source gives the age in days, from 1 to 365.
_AGE_RANGE: Final = (1, 365)


def build() -> Built:
    """Download Concrete Compressive Strength from UCI and return it as a ``Built`` object.

    The shape, the column names, the missing values and the range of the age are checked, so a
    silent change of the data on the UCI side is noticed instead of being saved. The columns
    are renamed to lower case with underscores.

    Returns
    -------
    Built
        Features as a ``(1030, 8)`` matrix without missing values, and the compressive strength
        in MPa as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, if a value is
        missing, infinite or negative, if the age is not a whole number of days between 1 and
        365, or if the strength is not positive.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("concrete_strength: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"concrete_strength: expected features of shape {_EXPECTED_SHAPE}, "
            f"got {features.shape}."
        )
    if set(features.columns) != {source for source, _ in _COLUMNS}:
        raise ValueError(f"concrete_strength: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_SOURCE_TARGET] or len(targets) != len(features):
        raise ValueError(
            f"concrete_strength: expected a single {_SOURCE_TARGET!r} target, one value per row."
        )

    columns: list[NDArray[np.float64]] = []
    for source, name in _COLUMNS:
        column = features[source].to_numpy(dtype=np.float64)
        if not np.isfinite(column).all():
            raise ValueError(f"concrete_strength: {name} has missing or infinite values.")
        if column.min() < 0:
            raise ValueError(f"concrete_strength: {name} has negative values.")
        columns.append(column)

    age = columns[-1]
    low, high = _AGE_RANGE
    if not (np.all(age == np.round(age)) and age.min() >= low and age.max() <= high):
        raise ValueError(
            f"concrete_strength: age must be a whole number of days between {low} and {high}."
        )

    y = targets[_SOURCE_TARGET].to_numpy(dtype=np.float64)
    if not (np.isfinite(y).all() and y.min() > 0):
        raise ValueError("concrete_strength: the strength must be positive and never missing.")

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=tuple(name for _, name in _COLUMNS),
        target_names=(_TARGET_NAME,),
        extras={
            "source": "UCI Machine Learning Repository, dataset 165",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
