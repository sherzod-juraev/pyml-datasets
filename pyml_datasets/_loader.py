"""Reading of the datasets bundled with the package as NPZ files."""

from importlib.resources import files
from typing import Final

import numpy as np

from ._types import Dataset, DatasetInfo

_PACKAGE: Final = "pyml_datasets"
_DATA_DIR: Final = "data"
_FORMAT_VERSION: Final = 2
_REQUIRED_KEYS: Final = ("X", "y", "feature_names", "description", "format_version", "meta")


def load_npz(info: DatasetInfo) -> Dataset:
    """Read the bundled ``<info.name>.npz`` file and build a ``Dataset``.

    The file is opened with ``allow_pickle=False``, so it can never execute code.

    Parameters
    ----------
    info : DatasetInfo
        Provenance of the dataset. Its ``name`` selects the file.

    Returns
    -------
    Dataset
        Freshly loaded dataset, nothing is cached between calls.

    Raises
    ------
    FileNotFoundError
        If the file is not part of the installed package.
    ValueError
        If the file lacks required arrays, uses another data format version, or its arrays
        do not fit together.
    """
    name = info.name
    resource = files(_PACKAGE) / _DATA_DIR / f"{name}.npz"
    if not resource.is_file():
        raise FileNotFoundError(f"Dataset file '{name}.npz' is missing from the package.")

    with resource.open("rb") as file, np.load(file, allow_pickle=False) as npz:
        missing = [key for key in _REQUIRED_KEYS if key not in npz.files]
        if missing:
            raise ValueError(f"Dataset '{name}' is missing required arrays: {missing}.")

        version = int(npz["format_version"])
        if version != _FORMAT_VERSION:
            raise ValueError(
                f"Dataset '{name}' uses data format {version}, but this version of "
                f"pyml-datasets reads format {_FORMAT_VERSION}."
            )

        X, y = npz["X"], npz["y"]
        feature_names = tuple(str(item) for item in npz["feature_names"])
        if X.ndim != 2 or len(y) != len(X) or len(feature_names) != X.shape[1]:
            raise ValueError(
                f"Dataset '{name}' is inconsistent: X has shape {X.shape}, y has "
                f"{len(y)} rows and there are {len(feature_names)} feature names."
            )

        target_names: tuple[str, ...] | None = None
        if "target_names" in npz.files:
            target_names = tuple(str(item) for item in npz["target_names"])

        return Dataset(
            X=X,
            y=y,
            feature_names=feature_names,
            target_names=target_names,
            description=str(npz["description"].item()),
            info=info,
        )
