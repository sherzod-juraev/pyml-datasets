"""Recipe for the Energy Efficiency dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 242
_EXPECTED_SHAPE: Final = (768, 8)

# Column names as UCI gives them (the variables table of the source), and the names stored in
# the file, in the order X1 to X8. Columns are picked by name, so the order in which UCI
# returns them does not matter.
_FEATURES: Final = (
    ("X1", "relative_compactness"),
    ("X2", "surface_area"),
    ("X3", "wall_area"),
    ("X4", "roof_area"),
    ("X5", "overall_height"),
    ("X6", "orientation"),
    ("X7", "glazing_area"),
    ("X8", "glazing_area_distribution"),
)
# The two responses: heating load first, cooling load second. They become the two columns of y.
_TARGETS: Final = (("Y1", "heating_load"), ("Y2", "cooling_load"))
# The source types these two features as integers.
_WHOLE_NUMBERS: Final = frozenset({"X6", "X8"})


def build() -> Built:
    """Download Energy Efficiency from UCI and return it as a ``Built`` object.

    The shape, the column names, the missing values and the kinds of values are checked, so a
    silent change of the data on the UCI side is noticed instead of being saved. The features
    are renamed after their descriptions, and the two responses are stacked into one matrix.

    Returns
    -------
    Built
        Features as a ``(768, 8)`` matrix without missing values, and the heating load and
        the cooling load as the two columns of a ``(768, 2)`` regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, if a value is
        missing, infinite or negative, if ``X6`` or ``X8`` hold other than whole numbers, or
        if a load is not positive.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("energy_efficiency: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"energy_efficiency: expected features of shape {_EXPECTED_SHAPE}, "
            f"got {features.shape}."
        )
    if set(features.columns) != {source for source, _ in _FEATURES}:
        raise ValueError(f"energy_efficiency: unexpected columns {list(features.columns)}.")
    if set(targets.columns) != {source for source, _ in _TARGETS} or len(targets) != len(features):
        raise ValueError(
            f"energy_efficiency: expected the targets Y1 and Y2, one value per row, "
            f"got {list(targets.columns)}."
        )

    columns: list[NDArray[np.float64]] = []
    for source, name in _FEATURES:
        column = features[source].to_numpy(dtype=np.float64)
        if not np.isfinite(column).all():
            raise ValueError(f"energy_efficiency: {name} has missing or infinite values.")
        if column.min() < 0:
            raise ValueError(f"energy_efficiency: {name} has negative values.")
        if source in _WHOLE_NUMBERS and not np.all(column == np.round(column)):
            raise ValueError(f"energy_efficiency: {name} must hold whole numbers only.")
        columns.append(column)

    responses: list[NDArray[np.float64]] = []
    for source, name in _TARGETS:
        response = targets[source].to_numpy(dtype=np.float64)
        if not (np.isfinite(response).all() and response.min() > 0):
            raise ValueError(f"energy_efficiency: {name} must be positive and never missing.")
        responses.append(response)

    return Built(
        X=np.column_stack(columns),
        y=np.column_stack(responses),
        feature_names=tuple(name for _, name in _FEATURES),
        target_names=tuple(name for _, name in _TARGETS),
        extras={
            "source": "UCI Machine Learning Repository, dataset 242",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
