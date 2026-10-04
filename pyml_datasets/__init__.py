"""Classic tabular datasets as NumPy ``.npz`` files.

Imports are eager on purpose (unlike pyml's lazy ``__getattr__``): the package is tiny,
and no data is read until a ``load_*`` function is called.
"""

__version__: str = "0.1.0"
__author__: str = "Sherzod Juraev"

from ._loader import Dataset
from ._sklearn import (
    load_breast_cancer,
    load_california_housing,
    load_diabetes,
    load_iris,
    load_linnerud,
    load_wine,
)
from ._wine_quality import load_wine_quality

__version__ = "0.1.0"

__all__ = [
    "Dataset",
    "__version__",
    "load_breast_cancer",
    "load_california_housing",
    "load_diabetes",
    "load_iris",
    "load_linnerud",
    "load_wine",
    "load_wine_quality",
]
