"""Loading of the datasets bundled with the package as NPZ files."""

from collections.abc import Iterator
from dataclasses import dataclass
from importlib.resources import files
from typing import Any, Final

import numpy as np
from numpy.typing import NDArray

_PACKAGE: Final = "pyml_datasets"
_DATA_DIR: Final = "data"
_REQUIRED_KEYS: Final = ("X", "y", "feature_names", "description")


@dataclass(frozen=True, eq=False)
class Dataset:
    """Dataset with its data matrix, targets and metadata.

    Iterating over a ``Dataset`` yields ``X`` and ``y``, so
    ``X, y = load_iris()`` works as well as ``data = load_iris()``.

    Attributes
    ----------
    X : ndarray of shape (n_samples, n_features)
        Data matrix.
    y : ndarray of shape (n_samples,) or (n_samples, n_targets)
        Target values.
    feature_names : tuple of str
        Names of the columns of ``X``.
    target_names : tuple of str or None
        Class names for classification or target names for multi-output
        regression, ``None`` if the source does not provide them.
    description : str
        Description of the dataset, including its source.
    """

    X: NDArray[np.float64]
    y: NDArray[Any]
    feature_names: tuple[str, ...]
    target_names: tuple[str, ...] | None
    description: str

    def __iter__(self) -> Iterator[NDArray[Any]]:
        """Yield ``X`` and ``y`` in this order."""
        yield self.X
        yield self.y


def _load_npz(name: str) -> Dataset:
    """Read the bundled ``<name>.npz`` file and build a ``Dataset``.

    Parameters
    ----------
    name : str
        File name of the dataset without the ``.npz`` extension.

    Returns
    -------
    Dataset
        Freshly loaded dataset, nothing is cached between calls.

    Raises
    ------
    FileNotFoundError
        If the file is not part of the installed package.
    ValueError
        If the file does not contain all required arrays.
    """
    resource = files(_PACKAGE) / _DATA_DIR / f"{name}.npz"
    if not resource.is_file():
        raise FileNotFoundError(f"Dataset file '{name}.npz' is missing from the package.")

    with resource.open("rb") as file, np.load(file, allow_pickle=False) as npz:
        missing = [key for key in _REQUIRED_KEYS if key not in npz.files]
        if missing:
            raise ValueError(f"Dataset '{name}' is missing required arrays: {missing}.")

        target_names: tuple[str, ...] | None = None
        if "target_names" in npz.files:
            target_names = tuple(str(item) for item in npz["target_names"])

        return Dataset(
            X=npz["X"],
            y=npz["y"],
            feature_names=tuple(str(item) for item in npz["feature_names"]),
            target_names=target_names,
            description=str(npz["description"].item()),
        )


def load_iris() -> Dataset:
    """Load the Iris dataset (classification, 150 samples, 4 features).

    Returns
    -------
    Dataset
        Dataset with 3 classes of iris plants.
    """
    return _load_npz("iris")


def load_wine() -> Dataset:
    """Load the Wine dataset (classification, 178 samples, 13 features).

    Returns
    -------
    Dataset
        Dataset with 3 classes of wine cultivars.
    """
    return _load_npz("wine")


def load_breast_cancer() -> Dataset:
    """Load the Breast Cancer Wisconsin (Diagnostic) dataset.

    Binary classification with 569 samples and 30 features.

    Returns
    -------
    Dataset
        Dataset with malignant and benign classes.
    """
    return _load_npz("breast_cancer")


def load_diabetes() -> Dataset:
    """Load the Diabetes dataset (regression, 442 samples, 10 features).

    Returns
    -------
    Dataset
        Dataset with unscaled features and a disease progression target.
    """
    return _load_npz("diabetes")


def load_linnerud() -> Dataset:
    """Load the Linnerud dataset (multi-output regression, 20 samples).

    Returns
    -------
    Dataset
        Dataset with 3 exercise features and 3 physiological targets,
        so ``y`` has shape ``(20, 3)``.
    """
    return _load_npz("linnerud")


def load_california_housing() -> Dataset:
    """Load the California Housing dataset (regression, 20640 samples, 8 features).

    Returns
    -------
    Dataset
        Dataset with the median house value as target.
    """
    return _load_npz("california_housing")
