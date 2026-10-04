"""Conversion, validation and saving of the arrays stored in a dataset NPZ file."""

from pathlib import Path
from typing import Any, Final, cast

import numpy as np
from numpy.typing import NDArray

from scripts.recipes._common import Built

_RESERVED_KEYS: Final = ("X", "y", "feature_names", "description", "target_names")


def to_arrays(built: Built) -> dict[str, NDArray[Any]]:
    """Convert a ``Built`` object into the arrays stored in the NPZ file.

    Parameters
    ----------
    built : Built
        Result of a dataset recipe, its task decides the dtype of ``y``.

    Returns
    -------
    dict of str to ndarray
        Arrays ``X``, ``y``, ``feature_names`` and ``description``, the arrays of
        ``built.extras``, plus ``target_names`` if the recipe provides them.

    Raises
    ------
    ValueError
        If a key of ``built.extras`` clashes with a required key.
    """
    y_dtype = np.int64 if built.task == "classification" else np.float64
    arrays: dict[str, NDArray[Any]] = {
        "X": np.asarray(built.X, dtype=np.float64),
        "y": np.asarray(built.y, dtype=y_dtype),
        "feature_names": np.asarray(built.feature_names),
        "description": np.asarray(built.description),
    }
    for key, value in built.extras.items():
        if key in _RESERVED_KEYS:
            raise ValueError(f"extras key '{key}' clashes with a required key.")
        arrays[key] = np.asarray(value)
    if built.target_names is not None:
        arrays["target_names"] = np.asarray(built.target_names)
    return arrays


def validate(name: str, arrays: dict[str, NDArray[Any]]) -> None:
    """Check the basic structure of the arrays before they are saved.

    Parameters
    ----------
    name : str
        Dataset name, used in error messages.
    arrays : dict of str to ndarray
        Arrays produced by ``to_arrays``.

    Raises
    ------
    ValueError
        If ``X`` is not a finite 2D matrix, or if ``y`` or ``feature_names``
        do not match its shape.
    """
    X, y = arrays["X"], arrays["y"]
    if X.ndim != 2:
        raise ValueError(f"{name}: X must be 2D, got {X.ndim}D.")
    if not np.isfinite(X).all():
        raise ValueError(f"{name}: X contains NaN or infinite values.")
    if len(y) != len(X):
        raise ValueError(f"{name}: y has {len(y)} rows but X has {len(X)}.")
    if len(arrays["feature_names"]) != X.shape[1]:
        raise ValueError(f"{name}: feature_names does not match the columns of X.")


def save(path: Path, arrays: dict[str, NDArray[Any]]) -> None:
    """Write the arrays to a compressed NPZ file, creating the folder if needed.

    Parameters
    ----------
    path : Path
        Target file, usually ``<output_dir>/<name>.npz``.
    arrays : dict of str to ndarray
        Arrays to store.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **cast(dict[str, Any], arrays))
