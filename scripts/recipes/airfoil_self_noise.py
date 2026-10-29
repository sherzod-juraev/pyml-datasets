"""Recipe for the Airfoil Self-Noise dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 291
_EXPECTED_SHAPE: Final = (1503, 5)
_SOURCE_TARGET: Final = "scaled-sound-pressure"
_TARGET_NAME: Final = "scaled_sound_pressure_level"

# Column names as UCI gives them (the variables table of the source), and the names stored in
# the file, in the order of the variables table. Columns are picked by name, so the order in
# which UCI returns them does not matter.
_COLUMNS: Final = (
    ("frequency", "frequency"),
    ("attack-angle", "angle_of_attack"),
    ("chord-length", "chord_length"),
    ("free-stream-velocity", "free_stream_velocity"),
    ("suction-side-displacement-thickness", "suction_side_displacement_thickness"),
)
# The source types the frequency (in Hz) as an integer.
_WHOLE_NUMBERS: Final = frozenset({"frequency"})
# The frequency, the chord length, the velocity and the thickness are physical quantities that
# cannot be negative. The angle of attack and the sound pressure level are only checked to be
# finite, the source documents no range for them.
_NOT_NEGATIVE: Final = frozenset(
    {"frequency", "chord-length", "free-stream-velocity", "suction-side-displacement-thickness"}
)


def build() -> Built:
    """Download Airfoil Self-Noise from UCI and return it as a ``Built`` object.

    The shape, the column names, the missing values and the kinds of values are checked, so a
    silent change of the data on the UCI side is noticed instead of being saved. The columns
    are renamed after their descriptions, written in lower case with underscores.

    Returns
    -------
    Built
        Features as a ``(1503, 5)`` matrix without missing values, and the scaled sound
        pressure level in decibels as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, if a value is
        missing or infinite, if the frequency is not a whole number, or if a frequency, chord
        length, velocity or thickness is negative.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("airfoil_self_noise: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"airfoil_self_noise: expected features of shape {_EXPECTED_SHAPE}, "
            f"got {features.shape}."
        )
    if set(features.columns) != {source for source, _ in _COLUMNS}:
        raise ValueError(f"airfoil_self_noise: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_SOURCE_TARGET] or len(targets) != len(features):
        raise ValueError(
            f"airfoil_self_noise: expected a single {_SOURCE_TARGET!r} target, one value per row."
        )

    columns: list[NDArray[np.float64]] = []
    for source, name in _COLUMNS:
        column = features[source].to_numpy(dtype=np.float64)
        if not np.isfinite(column).all():
            raise ValueError(f"airfoil_self_noise: {name} has missing or infinite values.")
        if source in _NOT_NEGATIVE and column.min() < 0:
            raise ValueError(f"airfoil_self_noise: {name} has negative values.")
        if source in _WHOLE_NUMBERS and not np.all(column == np.round(column)):
            raise ValueError(f"airfoil_self_noise: {name} must hold whole numbers only.")
        columns.append(column)

    y = targets[_SOURCE_TARGET].to_numpy(dtype=np.float64)
    if not np.isfinite(y).all():
        raise ValueError(f"airfoil_self_noise: {_TARGET_NAME} has missing or infinite values.")

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=tuple(name for _, name in _COLUMNS),
        target_names=(_TARGET_NAME,),
        extras={
            "source": "UCI Machine Learning Repository, dataset 291",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
