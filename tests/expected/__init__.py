"""Facts about each dataset, written down independently of the data files.

Every module in this package is named after a dataset and defines ``EXPECTED``. The values
come from the documentation of the source (shapes, class counts, published means), not from
the file under test, so a data file that was damaged or rebuilt wrongly is noticed.
"""

import importlib
import pkgutil
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Expected:
    """Independent facts about one dataset.

    Attributes
    ----------
    shape : tuple of int
        Shape of ``X``.
    n_classes : int or None
        Number of classes, ``None`` for regression.
    class_counts : tuple of int or None
        Number of samples per class, if the source states them.
    first_row : tuple of float
        The first values of the first sample. Only as many values as given are compared.
    column_means : dict of int to float
        Published mean of selected columns, ignoring missing values.
    mean_tolerance : float
        Largest allowed difference between a published mean and the mean of the data. It is
        small unless the source itself offers the data with two different precisions.
    n_missing : int
        Number of missing values in ``X``.
    n_targets : int
        Number of columns of ``y``, 1 if ``y`` is a vector.
    """

    shape: tuple[int, int]
    n_classes: int | None
    class_counts: tuple[int, ...] | None
    first_row: tuple[float, ...]
    column_means: dict[int, float] = field(default_factory=dict)
    mean_tolerance: float = 1e-4
    n_missing: int = 0
    n_targets: int = 1


def all_expected() -> dict[str, Expected]:
    """Collect ``EXPECTED`` from every module of this package.

    Returns
    -------
    dict of str to Expected
        Facts by dataset name.
    """
    found: dict[str, Expected] = {}
    for module in pkgutil.iter_modules(__path__):
        found[module.name] = importlib.import_module(f"{__name__}.{module.name}").EXPECTED
    return found
