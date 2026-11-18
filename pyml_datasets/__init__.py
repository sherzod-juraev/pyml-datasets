"""Classic tabular datasets as NumPy ``.npz`` files.

The module of a dataset is imported when the dataset is first used, not when the package is
imported: ``import pyml_datasets`` and ``list_datasets`` import no dataset module, and a
``load_*`` function, ``get_info`` or ``load_dataset`` import only the one they need. No data
is read until a ``load_*`` function or ``load_dataset`` is called.

Every dataset carries its license, its source and its citation in ``Dataset.info``.

Type checkers and IDEs read ``__init__.pyi`` (generated), which names every loader, so the
``__getattr__`` below does not hide a misspelled name from them.
"""

__version__: str = "0.22.0"
__author__: str = "Sherzod Juraev"

import importlib
from typing import Any

from ._registry import get_info, list_datasets, load_dataset
from ._types import Dataset, DatasetInfo
from .datasets import DATASET_TASKS

__all__ = [
    "Dataset",
    "DatasetInfo",
    "__version__",
    "get_info",
    "list_datasets",
    "load_dataset",
    # <generated:all>
    "load_abalone",
    "load_adult",
    "load_airfoil_self_noise",
    "load_auto_mpg",
    "load_bank_marketing",
    "load_breast_cancer",
    "load_combined_cycle_power_plant",
    "load_concrete_strength",
    "load_credit_card_default",
    "load_digits",
    "load_energy_efficiency",
    "load_forest_fires",
    "load_german_credit",
    "load_iris",
    "load_mushroom",
    "load_penguins",
    "load_real_estate_valuation",
    "load_superconductivity",
    "load_wine",
    "load_wine_quality",
    # </generated:all>
]


def __dir__() -> list[str]:
    """List the public names, including the loaders that are not imported yet."""
    return sorted(__all__)


def __getattr__(name: str) -> Any:
    """Import a ``load_<dataset>`` function the first time it is used.

    The function is stored in the module afterwards, so later lookups do not come here.

    Parameters
    ----------
    name : str
        Attribute that was not found in the module.

    Returns
    -------
    Any
        The loader of the dataset.

    Raises
    ------
    AttributeError
        If ``name`` is not the loader of a bundled dataset.
    """
    dataset = name.removeprefix("load_")
    if name.startswith("load_") and dataset in DATASET_TASKS:
        loader = getattr(importlib.import_module(f".datasets.{dataset}", __name__), name)
        globals()[name] = loader
        return loader
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
