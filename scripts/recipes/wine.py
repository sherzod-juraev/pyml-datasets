"""Recipe for Wine, taken from scikit-learn."""

from sklearn.datasets import load_wine

from scripts.recipes._common import Built
from scripts.recipes._sklearn import from_bunch


def build() -> Built:
    """Build the Wine dataset.

    Returns
    -------
    Built
        178 samples, 13 features and 3 classes.
    """
    return from_bunch(load_wine())
