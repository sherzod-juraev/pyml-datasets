"""Shared code of the recipes whose data comes from scikit-learn."""

from typing import Any

import sklearn

from scripts.recipes._common import Built


def from_bunch(bunch: Any) -> Built:
    """Convert a scikit-learn ``Bunch`` into a ``Built`` object.

    Parameters
    ----------
    bunch : Bunch
        Object returned by a scikit-learn dataset loader.

    Returns
    -------
    Built
        The same data, with the scikit-learn version recorded in ``extras``. Class names
        are converted to strings, because some loaders return integers.
    """
    target_names = getattr(bunch, "target_names", None)
    return Built(
        X=bunch.data,
        y=bunch.target,
        feature_names=[str(name) for name in bunch.feature_names],
        target_names=None if target_names is None else [str(name) for name in target_names],
        extras={"sklearn_version": sklearn.__version__},
    )
