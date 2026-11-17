"""Registry of the bundled datasets: listing, lookup by name and loading by name.

The names and the tasks of the datasets come from ``datasets/__init__.py``, which is generated
and imports no dataset module. A dataset module is imported when that dataset is asked for,
so the cost of ``import pyml_datasets`` does not grow with the number of datasets.
"""

import importlib
from collections.abc import Callable
from types import ModuleType
from typing import Final

from ._types import Dataset, DatasetInfo, Task
from .datasets import DATASET_TASKS

_PACKAGE: Final = "pyml_datasets"


def _unknown(name: str) -> ValueError:
    """Build the error for a dataset name that is not bundled.

    Parameters
    ----------
    name : str
        The name that was asked for.

    Returns
    -------
    ValueError
        Error that lists the available names.
    """
    available = ", ".join(sorted(DATASET_TASKS))
    return ValueError(f"Unknown dataset {name!r}. Available datasets: {available}.")


def _module(name: str) -> ModuleType:
    """Import the module of a bundled dataset and check it against the generated index.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    types.ModuleType
        The module ``pyml_datasets.datasets.<name>``.

    Raises
    ------
    ValueError
        If no dataset has this name.
    RuntimeError
        If the name or the task in the ``INFO`` of the module differs from the generated
        index, which means ``python -m scripts gen`` was not run after a change.
    """
    if name not in DATASET_TASKS:
        raise _unknown(name)
    module = importlib.import_module(f".datasets.{name}", _PACKAGE)
    info: DatasetInfo = module.INFO
    if info.name != name or info.task != DATASET_TASKS[name]:
        raise RuntimeError(
            f"The index of datasets does not match the INFO of {name!r}. Run python -m scripts gen."
        )
    return module


def list_datasets(task: Task | None = None) -> tuple[str, ...]:
    """List the names of the bundled datasets.

    No dataset module is imported to answer this.

    Parameters
    ----------
    task : {"classification", "regression"}, optional
        Keep only the datasets of this task, all datasets if not given.

    Returns
    -------
    tuple of str
        Dataset names in alphabetical order. Each name works with ``load_dataset``.

    Examples
    --------
    >>> from pyml_datasets import list_datasets
    >>> "iris" in list_datasets()
    True
    >>> "iris" in list_datasets("regression")
    False
    """
    return tuple(
        sorted(name for name, kind in DATASET_TASKS.items() if task is None or kind == task)
    )


def get_info(name: str) -> DatasetInfo:
    """Return the provenance and license of a dataset without reading its data.

    Parameters
    ----------
    name : str
        Dataset name, one of ``list_datasets()``.

    Returns
    -------
    DatasetInfo
        License, source, citation and changes of the dataset.

    Raises
    ------
    ValueError
        If no dataset has this name.

    Examples
    --------
    >>> from pyml_datasets import get_info
    >>> get_info("iris").license
    'CC-BY-4.0'
    """
    info: DatasetInfo = _module(name).INFO
    return info


def load_dataset(name: str) -> Dataset:
    """Load a dataset by its name.

    This is the same as calling the ``load_<name>`` function of the dataset.

    Parameters
    ----------
    name : str
        Dataset name, one of ``list_datasets()``.

    Returns
    -------
    Dataset
        Freshly loaded dataset.

    Raises
    ------
    ValueError
        If no dataset has this name.

    Examples
    --------
    >>> from pyml_datasets import load_dataset
    >>> X, y = load_dataset("iris")
    >>> X.shape
    (150, 4)
    """
    loader: Callable[[], Dataset] = getattr(_module(name), f"load_{name}")
    return loader()
