"""Build the bundled NPZ datasets.

Run it from the repository root with the ``build`` command and commit the resulting
files::

    python -m scripts build
    python -m scripts build iris wine --force

Every dataset has a recipe in ``scripts/recipes/`` that loads or downloads the raw data, and
an ``INFO`` in ``pyml_datasets/datasets/`` that says where the data comes from and under
which license. ``scripts/_npz.py`` combines both, validates the result and saves it. Existing
files are skipped unless ``--force`` is given, because NPZ files are not byte-for-byte
reproducible and every rebuild adds a new binary file to the git history. Some recipes
download data, so they need an internet connection.

After building, run ``python -m scripts gen`` to refresh the manifest, the notice and
the documentation.
"""

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Final

from pyml_datasets import DatasetInfo
from scripts import ROOT
from scripts._npz import save, to_arrays, validate
from scripts.recipes import get_recipe

OUTPUT_DIR: Final = ROOT / "pyml_datasets" / "data"


def _info_of(name: str) -> DatasetInfo:
    """Import the dataset module and return its ``INFO``.

    The module is imported directly and not through the registry, so a dataset that was
    just scaffolded can be built before ``python -m scripts gen`` has registered it.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    DatasetInfo
        The ``INFO`` constant of ``pyml_datasets/datasets/<name>.py``.
    """
    info: DatasetInfo = import_module(f"pyml_datasets.datasets.{name}").INFO
    return info


@dataclass(frozen=True)
class BuildResult:
    """What happened to one dataset in :func:`build_dataset`.

    Attributes
    ----------
    name : str
        Dataset name.
    built : bool
        ``True`` if the file was written, ``False`` if an existing file was kept.
    shape : tuple of int or None
        Shape of ``X`` of the new file, ``None`` if the file was kept.
    size_kib : float
        Size of the file in KiB.
    """

    name: str
    built: bool
    shape: tuple[int, ...] | None
    size_kib: float


def build_dataset(name: str, output_dir: Path, overwrite: bool = False) -> BuildResult:
    """Build one dataset and save it as ``<name>.npz``.

    Parameters
    ----------
    name : str
        Dataset name, one of ``recipe_names()``.
    output_dir : Path
        Directory where the file is written, created if missing.
    overwrite : bool, default=False
        Replace the file if it already exists, otherwise it is kept.

    Returns
    -------
    BuildResult
        Whether the file was written, and its shape and size.
    """
    path = output_dir / f"{name}.npz"
    if path.exists() and not overwrite:
        return BuildResult(name, False, None, path.stat().st_size / 1024)

    info = _info_of(name)
    arrays = to_arrays(get_recipe(name)(), info)
    validate(info, arrays)
    save(path, arrays)
    return BuildResult(name, True, tuple(arrays["X"].shape), path.stat().st_size / 1024)
