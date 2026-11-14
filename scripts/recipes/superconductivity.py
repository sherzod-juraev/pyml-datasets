"""Recipe for the Superconductivity dataset from the UCI Machine Learning Repository."""

from importlib.metadata import version
from typing import Final

import numpy as np
from numpy.typing import NDArray
from ucimlrepo import fetch_ucirepo

from scripts.recipes._common import Built

_UCI_ID: Final = 464
_EXPECTED_SHAPE: Final = (21263, 81)

# Column names as UCI gives them, in the order of the file train.csv. They are stored
# unchanged, see INFO.changes.
_FEATURES: Final = (
    "number_of_elements",
    "mean_atomic_mass",
    "wtd_mean_atomic_mass",
    "gmean_atomic_mass",
    "wtd_gmean_atomic_mass",
    "entropy_atomic_mass",
    "wtd_entropy_atomic_mass",
    "range_atomic_mass",
    "wtd_range_atomic_mass",
    "std_atomic_mass",
    "wtd_std_atomic_mass",
    "mean_fie",
    "wtd_mean_fie",
    "gmean_fie",
    "wtd_gmean_fie",
    "entropy_fie",
    "wtd_entropy_fie",
    "range_fie",
    "wtd_range_fie",
    "std_fie",
    "wtd_std_fie",
    "mean_atomic_radius",
    "wtd_mean_atomic_radius",
    "gmean_atomic_radius",
    "wtd_gmean_atomic_radius",
    "entropy_atomic_radius",
    "wtd_entropy_atomic_radius",
    "range_atomic_radius",
    "wtd_range_atomic_radius",
    "std_atomic_radius",
    "wtd_std_atomic_radius",
    "mean_Density",
    "wtd_mean_Density",
    "gmean_Density",
    "wtd_gmean_Density",
    "entropy_Density",
    "wtd_entropy_Density",
    "range_Density",
    "wtd_range_Density",
    "std_Density",
    "wtd_std_Density",
    "mean_ElectronAffinity",
    "wtd_mean_ElectronAffinity",
    "gmean_ElectronAffinity",
    "wtd_gmean_ElectronAffinity",
    "entropy_ElectronAffinity",
    "wtd_entropy_ElectronAffinity",
    "range_ElectronAffinity",
    "wtd_range_ElectronAffinity",
    "std_ElectronAffinity",
    "wtd_std_ElectronAffinity",
    "mean_FusionHeat",
    "wtd_mean_FusionHeat",
    "gmean_FusionHeat",
    "wtd_gmean_FusionHeat",
    "entropy_FusionHeat",
    "wtd_entropy_FusionHeat",
    "range_FusionHeat",
    "wtd_range_FusionHeat",
    "std_FusionHeat",
    "wtd_std_FusionHeat",
    "mean_ThermalConductivity",
    "wtd_mean_ThermalConductivity",
    "gmean_ThermalConductivity",
    "wtd_gmean_ThermalConductivity",
    "entropy_ThermalConductivity",
    "wtd_entropy_ThermalConductivity",
    "range_ThermalConductivity",
    "wtd_range_ThermalConductivity",
    "std_ThermalConductivity",
    "wtd_std_ThermalConductivity",
    "mean_Valence",
    "wtd_mean_Valence",
    "gmean_Valence",
    "wtd_gmean_Valence",
    "entropy_Valence",
    "wtd_entropy_Valence",
    "range_Valence",
    "wtd_range_Valence",
    "std_Valence",
    "wtd_std_Valence",
)
_TARGET: Final = "critical_temp"
# Smallest and largest value of every column in the file train.csv of the UCI download,
# borders included, as the facts of the source file print them with six significant digits. A
# value outside of the ranges, widened by _RELATIVE_MARGIN, means that the data on the UCI
# side changed.
_RANGES: Final = {
    "number_of_elements": (1, 9),
    "mean_atomic_mass": (6.941, 208.98),
    "wtd_mean_atomic_mass": (6.42345, 208.98),
    "gmean_atomic_mass": (5.32057, 208.98),
    "wtd_gmean_atomic_mass": (1.96085, 208.98),
    "entropy_atomic_mass": (0, 1.9838),
    "wtd_entropy_atomic_mass": (0, 1.9582),
    "range_atomic_mass": (0, 207.972),
    "wtd_range_atomic_mass": (0, 205.59),
    "std_atomic_mass": (0, 101.02),
    "wtd_std_atomic_mass": (0, 101.02),
    "mean_fie": (375.5, 1313.1),
    "wtd_mean_fie": (375.5, 1348.03),
    "gmean_fie": (375.5, 1313.1),
    "wtd_gmean_fie": (375.5, 1327.59),
    "entropy_fie": (0, 2.15778),
    "wtd_entropy_fie": (0, 2.03856),
    "range_fie": (0, 1304.5),
    "wtd_range_fie": (0, 1251.86),
    "std_fie": (0, 499.672),
    "wtd_std_fie": (0, 479.162),
    "mean_atomic_radius": (48, 298),
    "wtd_mean_atomic_radius": (48, 298),
    "gmean_atomic_radius": (48, 298),
    "wtd_gmean_atomic_radius": (48, 298),
    "entropy_atomic_radius": (0, 2.14196),
    "wtd_entropy_atomic_radius": (0, 1.90375),
    "range_atomic_radius": (0, 256),
    "wtd_range_atomic_radius": (0, 240.164),
    "std_atomic_radius": (0, 115.5),
    "wtd_std_atomic_radius": (0, 97.1407),
    "mean_Density": (1.429, 22590),
    "wtd_mean_Density": (1.429, 22590),
    "gmean_Density": (1.429, 22590),
    "wtd_gmean_Density": (0.686245, 22590),
    "entropy_Density": (0, 1.9543),
    "wtd_entropy_Density": (0, 1.70342),
    "range_Density": (0, 22588.6),
    "wtd_range_Density": (0, 22434.2),
    "std_Density": (0, 10724.4),
    "wtd_std_Density": (0, 10410.9),
    "mean_ElectronAffinity": (1.5, 326.1),
    "wtd_mean_ElectronAffinity": (1.5, 326.1),
    "gmean_ElectronAffinity": (1.5, 326.1),
    "wtd_gmean_ElectronAffinity": (1.5, 326.1),
    "entropy_ElectronAffinity": (0, 1.76773),
    "wtd_entropy_ElectronAffinity": (0, 1.6754),
    "range_ElectronAffinity": (0, 349),
    "wtd_range_ElectronAffinity": (0, 218.697),
    "std_ElectronAffinity": (0, 162.895),
    "wtd_std_ElectronAffinity": (0, 169.076),
    "mean_FusionHeat": (0.222, 105),
    "wtd_mean_FusionHeat": (0.222, 105),
    "gmean_FusionHeat": (0.222, 105),
    "wtd_gmean_FusionHeat": (0.222, 105),
    "entropy_FusionHeat": (0, 2.03441),
    "wtd_entropy_FusionHeat": (0, 1.74716),
    "range_FusionHeat": (0, 104.778),
    "wtd_range_FusionHeat": (0, 102.675),
    "std_FusionHeat": (0, 51.635),
    "wtd_std_FusionHeat": (0, 51.6805),
    "mean_ThermalConductivity": (0.02658, 332.5),
    "wtd_mean_ThermalConductivity": (0.02658, 406.96),
    "gmean_ThermalConductivity": (0.02658, 317.884),
    "wtd_gmean_ThermalConductivity": (0.0229516, 376.033),
    "entropy_ThermalConductivity": (0, 1.63398),
    "wtd_entropy_ThermalConductivity": (0, 1.61299),
    "range_ThermalConductivity": (0, 429.974),
    "wtd_range_ThermalConductivity": (0, 401.44),
    "std_ThermalConductivity": (0, 214.986),
    "wtd_std_ThermalConductivity": (0, 213.3),
    "mean_Valence": (1, 7),
    "wtd_mean_Valence": (1, 7),
    "gmean_Valence": (1, 7),
    "wtd_gmean_Valence": (1, 7),
    "entropy_Valence": (0, 2.14196),
    "wtd_entropy_Valence": (0, 1.94974),
    "range_Valence": (0, 6),
    "wtd_range_Valence": (0, 6.9922),
    "std_Valence": (0, 3),
    "wtd_std_Valence": (0, 3),
    "critical_temp": (0.00021, 185),
}
_RELATIVE_MARGIN: Final = 1e-5
# The three columns that hold whole numbers only in the source file.
_WHOLE_NUMBERS: Final = frozenset({"number_of_elements", "range_atomic_radius", "range_Valence"})


def _numeric(values: NDArray[np.float64], name: str) -> NDArray[np.float64]:
    """Check that a numeric column is complete and inside the range of the source.

    Parameters
    ----------
    values : ndarray of shape (n_samples,)
        Column converted to ``float64``.
    name : str
        Column name, used in error messages and to find the range in ``_RANGES``.

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
        raise ValueError(f"superconductivity: {name} has missing or infinite values.")
    low, high = _RANGES[name]
    margin = _RELATIVE_MARGIN * max(abs(low), abs(high))
    if values.min() < low - margin or values.max() > high + margin:
        raise ValueError(f"superconductivity: {name} must be between {low} and {high}.")
    if name in _WHOLE_NUMBERS and not np.all(values == np.round(values)):
        raise ValueError(f"superconductivity: {name} must hold whole numbers only.")
    return values


def build() -> Built:
    """Download Superconductivity from the UCI repository as a ``Built`` object.

    The shape, the column names, the ranges of all columns and the whole numbers of three
    columns are checked, so a silent change of the data on the UCI side is noticed instead of
    being saved.

    Returns
    -------
    Built
        Features as a ``(21263, 81)`` matrix without missing values, and the critical
        temperature as a regression target.

    Raises
    ------
    ValueError
        If the downloaded data does not have the expected shape or columns, or if a value is
        missing, infinite or outside of the range of the source.
    """
    dataset = fetch_ucirepo(id=_UCI_ID)
    features, targets = dataset.data.features, dataset.data.targets
    if features is None or targets is None:
        raise ValueError("superconductivity: UCI returned no features or no targets.")
    if features.shape != _EXPECTED_SHAPE:
        raise ValueError(
            f"superconductivity: expected features of shape {_EXPECTED_SHAPE}, "
            f"got {features.shape}."
        )
    if list(features.columns) != list(_FEATURES):
        raise ValueError(f"superconductivity: unexpected columns {list(features.columns)}.")
    if list(targets.columns) != [_TARGET] or len(targets) != len(features):
        raise ValueError(
            f"superconductivity: expected a single {_TARGET!r} target, one value per row."
        )

    columns = [_numeric(features[name].to_numpy(dtype=np.float64), name) for name in _FEATURES]
    y = _numeric(targets[_TARGET].to_numpy(dtype=np.float64), _TARGET)

    return Built(
        X=np.column_stack(columns),
        y=y,
        feature_names=_FEATURES,
        target_names=(_TARGET,),
        extras={
            "source": "UCI Machine Learning Repository, dataset 464",
            "ucimlrepo_version": version("ucimlrepo"),
        },
    )
