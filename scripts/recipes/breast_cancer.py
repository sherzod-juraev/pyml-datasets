"""Recipe for Breast Cancer Wisconsin (Diagnostic), taken from scikit-learn."""

from sklearn.datasets import load_breast_cancer

from scripts.recipes._common import Built
from scripts.recipes._sklearn import from_bunch


def build() -> Built:
    """Build the Breast Cancer Wisconsin (Diagnostic) dataset.

    Returns
    -------
    Built
        569 samples, 30 features and 2 classes.
    """
    return from_bunch(load_breast_cancer())
