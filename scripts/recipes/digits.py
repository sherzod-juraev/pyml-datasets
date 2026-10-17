"""Recipe for the handwritten digits dataset, taken from scikit-learn."""

from sklearn.datasets import load_digits

from scripts.recipes._common import Built
from scripts.recipes._sklearn import from_bunch


def build() -> Built:
    """Build the handwritten digits dataset.

    scikit-learn ships the test set of the UCI dataset only, so this is 1797 of its 5620
    samples.

    Returns
    -------
    Built
        1797 samples, 64 features and 10 classes.
    """
    return from_bunch(load_digits())
