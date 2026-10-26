"""Recipe for the Combined Cycle Power Plant dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 294
_EXPECTED_SHAPE: Final = (9568, 4)
_SOURCE_TARGET: Final = "PE"
_TARGET_NAME: Final = "net_hourly_electrical_energy_output"

# Column names as UCI gives them (the variables table of the source), the names stored in the
# file, and the range that the source documents for the column. Columns are picked by name, so
# the order in which UCI returns them does not matter.
_COLUMNS: Final = (
    ("AT", "temperature", (1.81, 37.11)),
    ("V", "exhaust_vacuum", (25.36, 81.56)),
    ("AP", "ambient_pressure", (992.89, 1033.30)),
    ("RH", "relative_humidity", (25.56, 100.16)),
)
_TARGET_RANGE: Final = (420.26, 495.76)
# The ranges are printed on the page with two decimals, a value may differ from them only by
# the rounding of the printed number.
_TOLERANCE: Final = 1e-6


def _check_range(name: str, values: NDArray[np.float64], bounds: tuple[float, float]) -> None:
    """Check that a column is finite and inside the range that the source documents.

    Parameters
    ----------
    name : str
        Name of the column, used in the error message.
    values : ndarray of shape (n_samples,)
        Values of the column.
    bounds : tuple of float
        Smallest and largest value documented by the source.

    Raises
    ------
    ValueError
        If a value is missing, infinite or outside the documented range.
    """
    low, high = bounds
    if not np.isfinite(values).all():
        raise ValueError(f"combined_cycle_power_plant: {name} has missing or infinite values.")
    if values.min() < low - _TOLERANCE or values.max() > high + _TOLERANCE:
        raise ValueError(
            f"combined_cycle_power_plant: {name} must be between {low} and {high}, "
            f"got {values.min()} to {values.max()}."
        )


def build() -> Built:
    """Download Combined Cycle Power Plant from UCI and return it as a ``Built`` object.

    The shape, the column names, the missing values and the ranges that the source documents
    are checked, so a silent change of the data on the UCI side is noticed instead of being
    saved. The columns are renamed after their descriptions.

    Returns
    -------
    Built
        Features as a ``(9568, 4)`` matrix without missing values, and the net hourly
        electrical energy output in MW as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, or if a value is
        missing, infinite or outside the range that the source documents.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("combined_cycle_power_plant: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"combined_cycle_power_plant: expected features of shape {_EXPECTED_SHAPE}, "
            f"got {features.shape}."
        )
    if set(features.columns) != {source for source, _, _ in _COLUMNS}:
        raise ValueError(
            f"combined_cycle_power_plant: unexpected columns {list(features.columns)}."
        )
    if list(targets.columns) != [_SOURCE_TARGET] or len(targets) != len(features):
        raise ValueError(
            f"combined_cycle_power_plant: expected a single {_SOURCE_TARGET!r} target, "
            "one value per row."
        )

    columns: list[NDArray[np.float64]] = []
    for source, name, bounds in _COLUMNS:
        column = features[source].to_numpy(dtype=np.float64)
        _check_range(name, column, bounds)
        columns.append(column)
    y = targets[_SOURCE_TARGET].to_numpy(dtype=np.float64)
    _check_range(_TARGET_NAME, y, _TARGET_RANGE)

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=tuple(name for _, name, _ in _COLUMNS),
        target_names=(_TARGET_NAME,),
        extras={
            "source": "UCI Machine Learning Repository, dataset 294",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
