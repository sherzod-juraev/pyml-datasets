"""Recipe for Iris, taken from scikit-learn."""

from sklearn.datasets import load_iris

from scripts.recipes._common import Built
from scripts.recipes._sklearn import from_bunch


def build() -> Built:
    """Build the Iris dataset.

    Returns
    -------
    Built
        150 samples, 4 features and 3 classes.
    """
    return from_bunch(load_iris())
