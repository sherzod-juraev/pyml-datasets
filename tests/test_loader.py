"""Tests for the NPZ loader: error paths and files built on the fly."""

import re
from pathlib import Path

import numpy as np
import pytest

from pyml_datasets import Dataset, _loader
from pyml_datasets._loader import load_npz
from tests.conftest import make_info, write_npz


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the loader at an empty ``data/`` folder inside ``tmp_path``."""
    monkeypatch.setattr(_loader, "files", lambda package: tmp_path)
    return tmp_path / "data"


def test_loads_file_without_target_names(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info)
    data = load_npz(info)
    assert isinstance(data, Dataset)
    assert data.X.shape == (3, 2)
    assert data.y.tolist() == [0, 1, 0]
    assert data.feature_names == ("a", "b")
    assert data.target_names is None
    assert data.description == "A tiny test dataset."
    assert data.info is info


def test_loads_target_names(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info, target_names=np.array(["no", "yes"]))
    assert load_npz(info).target_names == ("no", "yes")


def test_every_call_returns_a_fresh_dataset(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info)
    first, second = load_npz(info), load_npz(info)
    assert first is not second
    assert first.X is not second.X


def test_unpacks_into_x_and_y(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info)
    X, y = load_npz(info)
    assert X.shape == (3, 2)
    assert y.shape == (3,)


def test_missing_file_raises(data_dir: Path) -> None:
    data_dir.mkdir()
    with pytest.raises(FileNotFoundError, match="tiny.npz"):
        load_npz(make_info())


KEYS = ["X", "y", "feature_names", "description", "format_version", "meta"]


@pytest.mark.parametrize("key", KEYS)
def test_missing_required_array_raises(data_dir: Path, key: str) -> None:
    info = make_info()
    write_npz(data_dir, info, drop=(key,))
    with pytest.raises(ValueError, match=re.escape(f"['{key}']")):
        load_npz(info)


def test_other_format_version_raises(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info, format_version=np.asarray(1))
    with pytest.raises(ValueError, match="data format 1"):
        load_npz(info)


def test_inconsistent_shapes_raise(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info, y=np.array([0, 1]))
    with pytest.raises(ValueError, match="inconsistent"):
        load_npz(info)


def test_wrong_number_of_feature_names_raises(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info, feature_names=np.array(["only_one"]))
    with pytest.raises(ValueError, match="inconsistent"):
        load_npz(info)


def test_pickled_objects_are_refused(data_dir: Path) -> None:
    info = make_info()
    write_npz(data_dir, info, feature_names=np.array([object(), object()], dtype=object))
    with pytest.raises(ValueError, match="pickle"):
        load_npz(info)
