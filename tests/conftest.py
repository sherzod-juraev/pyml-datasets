"""Shared fixtures."""

from pathlib import Path
from typing import Any

import numpy as np
import pytest

from pyml_datasets import DatasetInfo, list_datasets

FORMAT_VERSION = 2


@pytest.fixture(params=list_datasets())
def name(request: pytest.FixtureRequest) -> str:
    """Name of each bundled dataset, so a test runs once per dataset."""
    return str(request.param)


def make_info(**changes: Any) -> DatasetInfo:
    """Build a valid ``DatasetInfo``, with some fields replaced.

    Parameters
    ----------
    **changes
        Fields to replace.

    Returns
    -------
    DatasetInfo
        Information of a small imaginary dataset called ``tiny``.
    """
    values: dict[str, Any] = {
        "name": "tiny",
        "title": "Tiny",
        "task": "classification",
        "summary": "A tiny test dataset.",
        "license": "CC0-1.0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "source": "Nowhere",
        "source_url": "https://example.org/tiny",
        "doi": None,
        "creators": ("Someone",),
        "citation": "Someone (2000). Tiny.",
        "obtained_from": "A test.",
        "changes": ("None.",),
        "verified_on": "2026-10-17",
    }
    values.update(changes)
    return DatasetInfo(**values)


def write_npz(folder: Path, info: DatasetInfo, *, drop: tuple[str, ...] = (), **extra: Any) -> None:
    """Write a small valid data file for ``info`` into ``folder``.

    Parameters
    ----------
    folder : Path
        Folder that plays the role of ``pyml_datasets/data``.
    info : DatasetInfo
        Information of the dataset, its name gives the file name.
    drop : tuple of str, optional
        Arrays to leave out.
    **extra
        Arrays to add or replace.
    """
    arrays: dict[str, Any] = {
        "X": np.arange(6, dtype=np.float64).reshape(3, 2),
        "y": np.array([0, 1, 0], dtype=np.int64),
        "feature_names": np.array(["a", "b"]),
        "description": np.asarray("A tiny test dataset."),
        "format_version": np.asarray(FORMAT_VERSION),
        "meta": np.asarray("{}"),
        **extra,
    }
    for key in drop:
        del arrays[key]
    folder.mkdir(parents=True, exist_ok=True)
    np.savez(folder / f"{info.name}.npz", **arrays)
