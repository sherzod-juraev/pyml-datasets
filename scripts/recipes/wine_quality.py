"""Recipe for the Wine Quality dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 186
_EXPECTED_SHAPE: Final = (6497, 11)


def build() -> Built:
    """Download Wine Quality from the UCI repository and return it as a ``Built`` object.

    The shape and the target values are checked, so a silent change of the data on the
    UCI side is noticed instead of being saved.

    Returns
    -------
    Built
        Features as a ``(6497, 11)`` matrix and the quality score as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape, columns or target values.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("wine_quality: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"wine_quality: expected features of shape {_EXPECTED_SHAPE}, got {features.shape}."
        )
    if list(targets.columns) != ["quality"] or len(targets) != len(features):
        raise ValueError("wine_quality: expected a single 'quality' target, one value per row.")

    y = targets["quality"].to_numpy(dtype=np.float64)
    if not (np.all(y == np.round(y)) and y.min() >= 0 and y.max() <= 10):
        raise ValueError("wine_quality: quality must be a whole score between 0 and 10.")

    return Built(
        X=features.to_numpy(dtype=np.float64),
        y=y,
        feature_names=[str(name) for name in features.columns],
        target_names=("quality",),
        extras={
            "source": "UCI Machine Learning Repository, dataset 186",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
