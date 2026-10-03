"""Classic tabular datasets for pyml, bundled with the package as NPZ files."""

__version__: str = "0.1.0"
__author__: str = "Sherzod Juraev"

from pyml_datasets._loader import (
    Dataset,
    load_breast_cancer,
    load_california_housing,
    load_diabetes,
    load_iris,
    load_linnerud,
    load_wine,
)

__all__ = [
    "Dataset",
    "__version__",
    "load_breast_cancer",
    "load_california_housing",
    "load_diabetes",
    "load_iris",
    "load_linnerud",
    "load_wine",
]
