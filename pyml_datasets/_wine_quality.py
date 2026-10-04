"""Loader for the Wine Quality dataset from the UCI Machine Learning Repository."""

from pyml_datasets._loader import Dataset, _load_npz


def load_wine_quality() -> Dataset:
    """Load the Wine Quality dataset.

    Returns
    -------
    Dataset
        Dataset with physicochemical features and the sensory quality score as target.
    """
    return _load_npz("wine_quality")
