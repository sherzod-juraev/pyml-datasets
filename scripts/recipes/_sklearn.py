"""Recipes for the datasets that scikit-learn provides."""

from typing import Any, Literal

import sklearn
from sklearn.datasets import (
    fetch_california_housing,
    load_breast_cancer,
    load_diabetes,
    load_iris,
    load_linnerud,
    load_wine,
)

from scripts.recipes._common import Built


def _from_bunch(bunch: Any, task: Literal["classification", "regression"]) -> Built:
    """Convert a scikit-learn ``Bunch`` into a ``Built`` object.

    Parameters
    ----------
    bunch : Bunch
        Object returned by a scikit-learn dataset loader.
    task : {"classification", "regression"}
        Task of the dataset.

    Returns
    -------
    Built
        The same data, with the scikit-learn version recorded in ``extras``.
    """
    return Built(
        X=bunch.data,
        y=bunch.target,
        feature_names=bunch.feature_names,
        target_names=getattr(bunch, "target_names", None),
        description=bunch.DESCR,
        task=task,
        extras={"sklearn_version": sklearn.__version__},
    )


def iris() -> Built:
    """Build the Iris dataset (classification)."""
    return _from_bunch(load_iris(), "classification")


def wine() -> Built:
    """Build the Wine dataset (classification)."""
    return _from_bunch(load_wine(), "classification")


def breast_cancer() -> Built:
    """Build the Breast Cancer Wisconsin (Diagnostic) dataset (classification)."""
    return _from_bunch(load_breast_cancer(), "classification")


def diabetes() -> Built:
    """Build the Diabetes dataset (regression), with the original unscaled features."""
    return _from_bunch(load_diabetes(scaled=False), "regression")


def linnerud() -> Built:
    """Build the Linnerud dataset (multi-output regression)."""
    return _from_bunch(load_linnerud(), "regression")


def california_housing() -> Built:
    """Build the California Housing dataset (regression), downloaded on the first run."""
    return _from_bunch(fetch_california_housing(), "regression")
