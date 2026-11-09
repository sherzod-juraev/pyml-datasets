"""Recipe for the Real Estate Valuation dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 477
_EXPECTED_SHAPE: Final = (414, 6)

# Column names as UCI gives them, in the order of the variables table. The identifier column
# "No" is not a feature, so it is not among them.
_SOURCE_COLUMNS: Final = (
    "X1 transaction date",
    "X2 house age",
    "X3 distance to the nearest MRT station",
    "X4 number of convenience stores",
    "X5 latitude",
    "X6 longitude",
)
_SOURCE_TARGET: Final = "Y house price of unit area"
# Names stored in the file, see INFO.changes.
_FEATURE_NAMES: Final = (
    "transaction_date",
    "house_age",
    "distance_to_nearest_mrt_station",
    "number_of_convenience_stores",
    "latitude",
    "longitude",
)
_TARGET: Final = "house_price_of_unit_area"
# Smallest and largest value of every column in the xlsx file of the UCI download, borders
# included. The transaction date is given rounded outward to three decimals, because
# ucimlrepo rounds the dates (2012.9166667 becomes 2012.917). A value outside of the ranges
# means that the data on the UCI side changed.
_RANGES: Final = {
    "transaction_date": (2012.666, 2013.584),
    "house_age": (0.0, 43.8),
    "distance_to_nearest_mrt_station": (23.38284, 6488.021),
    "number_of_convenience_stores": (0.0, 10.0),
    "latitude": (24.93207, 25.01459),
    "longitude": (121.47353, 121.56627),
    _TARGET: (7.6, 117.5),
}
# The source describes the number of convenience stores as an integer.
_WHOLE_NUMBERS: Final = frozenset({"number_of_convenience_stores"})
_TOLERANCE: Final = 1e-9


def _numeric(values: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    """Check that a numeric column is complete and inside the range of the source.

    Parameters
    ----------
    values : ndarray of shape (n_samples,)
        Column converted to ``float64``.
    name : str
        Name stored in the file, used in error messages and to find the range in ``_RANGES``.

    Returns
    -------
    ndarray of shape (n_samples,)
        The same column.

    Raises
    ------
    ValueError
        If the column has missing or infinite values, values outside of the range of the
        source, or, for a whole-number column, values that are not whole numbers.
    """
    if not np.isfinite(values).all():
        raise ValueError(f"real_estate_valuation: {name} has missing or infinite values.")
    low, high = _RANGES[name]
    if values.min() < low - _TOLERANCE or values.max() > high + _TOLERANCE:
        raise ValueError(f"real_estate_valuation: {name} must be between {low} and {high}.")
    if name in _WHOLE_NUMBERS and not np.all(values == np.round(values)):
        raise ValueError(f"real_estate_valuation: {name} must hold whole numbers only.")
    return values


def build() -> Built:
    """Download Real Estate Valuation from the UCI repository as a ``Built`` object.

    The shape, the column names, the ranges of all columns and the whole numbers of the
    number of convenience stores are checked, so a silent change of the data on the UCI side
    is noticed instead of being saved. The identifier column is not stored.

    Returns
    -------
    Built
        Features as a ``(414, 6)`` matrix without missing values, and the house price of unit
        area as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, or if a value is
        missing, infinite or outside of the range of the source.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("real_estate_valuation: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"real_estate_valuation: expected features of shape {_EXPECTED_SHAPE}, "
            f"got {features.shape}."
        )
    if list(features.columns) != list(_SOURCE_COLUMNS):
        raise ValueError(f"real_estate_valuation: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_SOURCE_TARGET] or len(targets) != len(features):
        raise ValueError(
            f"real_estate_valuation: expected a single {_SOURCE_TARGET!r} target, "
            "one value per row."
        )

    columns = [
        _numeric(features[source].to_numpy(dtype=np.float64), name)
        for source, name in zip(_SOURCE_COLUMNS, _FEATURE_NAMES, strict=True)
    ]
    y = _numeric(targets[_SOURCE_TARGET].to_numpy(dtype=np.float64), _TARGET)

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=_FEATURE_NAMES,
        target_names=(_TARGET,),
        extras={
            "source": "UCI Machine Learning Repository, dataset 477",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
