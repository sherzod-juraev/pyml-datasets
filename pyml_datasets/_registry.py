"""Registry of the bundled datasets: listing, lookup by name and loading by name."""

from collections.abc import Callable, Mapping
from typing import Final

from ._types import Dataset, DatasetInfo, Task
from .datasets import ENTRIES

REGISTRY: Final[Mapping[str, DatasetInfo]] = {info.name: info for info, _ in ENTRIES}
_LOADERS: Final[Mapping[str, Callable[[], Dataset]]] = {info.name: load for info, load in ENTRIES}

if len(REGISTRY) != len(ENTRIES):
    raise RuntimeError("Two bundled datasets share the same name.")


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
    available = ", ".join(REGISTRY)
    return ValueError(f"Unknown dataset {name!r}. Available datasets: {available}.")


def list_datasets(task: Task | None = None) -> tuple[str, ...]:
    """List the names of the bundled datasets.

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
        sorted(name for name, info in REGISTRY.items() if task is None or info.task == task)
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
    try:
        return REGISTRY[name]
    except KeyError:
        raise _unknown(name) from None


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
    try:
        loader = _LOADERS[name]
    except KeyError:
        raise _unknown(name) from None
    return loader()
