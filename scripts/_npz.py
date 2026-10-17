"""Conversion, validation and saving of the arrays stored in a dataset NPZ file."""

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Final, cast

import numpy as np
from numpy.typing import NDArray

from pyml_datasets import DatasetInfo
from scripts._render import info_json, render_description
from scripts.recipes._common import Built

FORMAT_VERSION: Final = 2
MANIFEST_KEYS: Final = ("X", "y", "feature_names", "target_names")


def to_arrays(built: Built, info: DatasetInfo) -> dict[str, NDArray[Any]]:
    """Convert a ``Built`` object and the dataset information into the stored arrays.

    Parameters
    ----------
    built : Built
        Result of a dataset recipe.
    info : DatasetInfo
        Provenance of the dataset. Its task decides the dtype of ``y``, and the description
        and the ``meta`` array are generated from it.

    Returns
    -------
    dict of str to ndarray
        The arrays ``X``, ``y``, ``feature_names``, ``description``, ``format_version``,
        ``meta`` and ``build``, plus ``target_names`` if the recipe provides them.

    Raises
    ------
    ValueError
        If a classification target is not made of whole numbers.
    """
    y = np.asarray(built.y)
    if info.task == "classification":
        if not np.all(y == np.round(y)):
            raise ValueError(f"{info.name}: classification labels must be whole numbers.")
        y = y.astype(np.int64)
    else:
        y = y.astype(np.float64)
    arrays: dict[str, NDArray[Any]] = {
        "X": np.asarray(built.X, dtype=np.float64),
        "y": y,
        "feature_names": np.asarray(built.feature_names),
        "description": np.asarray(render_description(info)),
        "format_version": np.asarray(FORMAT_VERSION, dtype=np.int64),
        "meta": np.asarray(info_json(info)),
        "build": np.asarray(json.dumps(dict(built.extras), sort_keys=True)),
    }
    if built.target_names is not None:
        arrays["target_names"] = np.asarray(built.target_names)
    return arrays


def validate(info: DatasetInfo, arrays: Mapping[str, NDArray[Any]]) -> None:
    """Check the arrays against the dataset information before they are saved.

    Parameters
    ----------
    info : DatasetInfo
        Information of the dataset. ``has_missing`` and ``categorical`` are checked here.
    arrays : mapping of str to ndarray
        Arrays produced by ``to_arrays``.

    Raises
    ------
    ValueError
        If ``X`` is not a 2D matrix without infinite values, if ``NaN`` appears although
        ``has_missing`` is false (or the other way round), if ``y`` is missing or does not fit
        ``X``, if the names do not fit, if class labels are not ``0 .. n_classes - 1``, or if
        a categorical column holds anything but valid codes.
    """
    name = info.name
    X, y = arrays["X"], arrays["y"]
    names = [str(item) for item in arrays["feature_names"]]
    if X.ndim != 2:
        raise ValueError(f"{name}: X must be 2D, got {X.ndim}D.")
    if np.isinf(X).any():
        raise ValueError(f"{name}: X contains infinite values.")
    n_missing = int(np.isnan(X).sum())
    if n_missing and not info.has_missing:
        raise ValueError(f"{name}: X has {n_missing} NaN but has_missing is False.")
    if info.has_missing and not n_missing:
        raise ValueError(f"{name}: has_missing is True but X has no NaN.")
    if len(y) != len(X):
        raise ValueError(f"{name}: y has {len(y)} rows but X has {len(X)}.")
    if not np.isfinite(y).all():
        raise ValueError(f"{name}: y must never contain missing or infinite values.")
    if len(names) != X.shape[1]:
        raise ValueError(f"{name}: feature_names does not match the columns of X.")

    if info.task == "classification":
        labels = np.unique(y)
        if y.ndim != 1 or not np.array_equal(labels, np.arange(labels.size)):
            raise ValueError(f"{name}: class labels must be 1D and 0 .. n_classes - 1.")
        if "target_names" in arrays and len(arrays["target_names"]) != labels.size:
            raise ValueError(f"{name}: target_names does not match the number of classes.")

    for feature, categories in info.categorical.items():
        if feature not in names:
            raise ValueError(f"{name}: categorical feature {feature!r} is not a feature name.")
        column = X[:, names.index(feature)]
        codes = column[~np.isnan(column)]
        if not np.array_equal(codes, np.round(codes)) or codes.min() < 0:
            raise ValueError(f"{name}: {feature!r} must hold whole-number codes.")
        if codes.max() >= len(categories):
            raise ValueError(f"{name}: {feature!r} has a code without a category name.")


def save(path: Path, arrays: Mapping[str, NDArray[Any]]) -> None:
    """Write the arrays to a compressed NPZ file, creating the folder if needed.

    Parameters
    ----------
    path : Path
        Target file, usually ``<output_dir>/<name>.npz``.
    arrays : mapping of str to ndarray
        Arrays to store.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **cast(dict[str, Any], dict(arrays)))


def array_digest(array: NDArray[Any]) -> str:
    """Compute a SHA-256 digest of an array that includes its dtype and shape.

    Parameters
    ----------
    array : ndarray
        Any array.

    Returns
    -------
    str
        Hexadecimal digest. Equal arrays give equal digests on every platform, unlike the
        bytes of an NPZ file, which are not reproducible.
    """
    digest = hashlib.sha256()
    digest.update(str(array.dtype.newbyteorder("<")).encode())
    digest.update(str(array.shape).encode())
    digest.update(np.ascontiguousarray(array).astype(array.dtype.newbyteorder("<")).tobytes())
    return digest.hexdigest()


def manifest_entry(arrays: Mapping[str, NDArray[Any]]) -> dict[str, str | None]:
    """Compute the manifest entry of a dataset: the digest of each data array.

    Parameters
    ----------
    arrays : mapping of str to ndarray
        Arrays of a data file.

    Returns
    -------
    dict of str to str or None
        Digest of ``X``, ``y``, ``feature_names`` and ``target_names``, ``None`` for an
        absent array.
    """
    return {key: array_digest(arrays[key]) if key in arrays else None for key in MANIFEST_KEYS}
