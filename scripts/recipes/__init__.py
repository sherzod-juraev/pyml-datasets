"""Recipes of the bundled datasets.

A recipe is a function without arguments that loads or downloads the raw data of one dataset
and returns it as a ``Built`` object. To add a dataset, write its recipe (a new module, or a
function in ``_sklearn.py`` if scikit-learn provides it) and add it to ``REGISTRY``.
"""

from collections.abc import Callable
from typing import Final

from scripts.recipes import _sklearn, wine_quality
from scripts.recipes._common import Built

REGISTRY: Final[dict[str, Callable[[], Built]]] = {
    "iris": _sklearn.iris,
    "wine": _sklearn.wine,
    "breast_cancer": _sklearn.breast_cancer,
    "diabetes": _sklearn.diabetes,
    "linnerud": _sklearn.linnerud,
    "california_housing": _sklearn.california_housing,
    "wine_quality": wine_quality.build,
}

__all__ = ["REGISTRY", "Built"]
