"""Loaders for the datasets originally taken from scikit-learn.

scikit-learn is not needed at runtime, the data are stored as NPZ files.
"""

from ._loader import Dataset, _load_npz


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
