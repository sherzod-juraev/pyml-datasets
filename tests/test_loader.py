"""Tests for the NPZ loader: error paths and files built on the fly."""

import re
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from pyml_datasets import _loader
from pyml_datasets._loader import _REQUIRED_KEYS, Dataset, _load_npz


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the loader at an empty ``data/`` folder inside ``tmp_path``."""
    monkeypatch.setattr(_loader, "files", lambda package: tmp_path)
    folder = tmp_path / "data"
    folder.mkdir()
    return folder


def _save(folder: Path, name: str, *, drop: tuple[str, ...] = (), **extra: Any) -> None:
    """Write a small valid ``<name>.npz``; ``drop`` removes keys, ``extra`` adds/overrides."""
    arrays: dict[str, Any] = {
        "X": np.arange(6, dtype=np.float64).reshape(3, 2),
        "y": np.array([0, 1, 0], dtype=np.int64),
        "feature_names": np.array(["a", "b"]),
        "description": np.asarray("A tiny test dataset."),
        **extra,
    }
    for key in drop:
        del arrays[key]
    np.savez(folder / f"{name}.npz", **arrays)


# ------------------------------- happy path -------------------------------- #


def test_loads_file_without_target_names(data_dir: Path):
    _save(data_dir, "tiny")
    data = _load_npz("tiny")
    assert isinstance(data, Dataset)
    assert data.X.shape == (3, 2)
    assert data.y.tolist() == [0, 1, 0]
    assert data.feature_names == ("a", "b")
    assert data.target_names is None
    assert data.description == "A tiny test dataset."


def test_loads_file_with_target_names(data_dir: Path):
    _save(data_dir, "tiny", target_names=np.array(["neg", "pos"]))
    assert _load_npz("tiny").target_names == ("neg", "pos")


# -------------------------------- error paths ------------------------------- #


def test_missing_file_raises_file_not_found(data_dir: Path):
    with pytest.raises(FileNotFoundError, match=re.escape("ghost.npz")):
        _load_npz("ghost")


@pytest.mark.parametrize("key", _REQUIRED_KEYS)
def test_missing_required_key_raises_value_error(data_dir: Path, key: str):
    _save(data_dir, "broken", drop=(key,))
    with pytest.raises(ValueError, match=re.escape(f"['{key}']")):
        _load_npz("broken")


def test_all_missing_keys_are_reported_together(data_dir: Path):
    _save(data_dir, "broken", drop=("y", "description"))
    with pytest.raises(ValueError, match=re.escape("['y', 'description']")):
        _load_npz("broken")


def test_error_message_names_the_dataset(data_dir: Path):
    _save(data_dir, "broken", drop=("X",))
    with pytest.raises(ValueError, match="broken"):
        _load_npz("broken")


def test_pickled_object_arrays_are_rejected(data_dir: Path):
    _save(data_dir, "unsafe", feature_names=np.array(["a", None], dtype=object))
    with pytest.raises(ValueError, match="allow_pickle"):
        _load_npz("unsafe")
