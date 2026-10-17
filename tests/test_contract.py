"""Rules that every bundled dataset must follow, run once per dataset."""

import numpy as np

from pyml_datasets import Dataset, get_info, load_dataset


def test_returns_a_dataset_with_its_info(name: str) -> None:
    data = load_dataset(name)
    assert isinstance(data, Dataset)
    assert data.info == get_info(name)


def test_arrays_have_the_documented_types(name: str) -> None:
    data = load_dataset(name)
    assert data.X.dtype == np.float64
    assert data.X.ndim == 2
    assert data.y.dtype == (np.int64 if data.info.task == "classification" else np.float64)
    assert len(data.y) == len(data.X)
    assert len(data.feature_names) == data.X.shape[1]
    assert all(isinstance(item, str) for item in data.feature_names)


def test_nothing_is_infinite(name: str) -> None:
    data = load_dataset(name)
    assert not np.isinf(data.X).any()
    assert np.isfinite(data.y).all()


def test_classification_labels_are_consecutive_from_zero(name: str) -> None:
    data = load_dataset(name)
    if data.info.task != "classification":
        return
    labels = np.unique(data.y)
    assert labels.tolist() == list(range(labels.size))
    assert data.target_names is not None
    assert len(data.target_names) == labels.size


def test_description_states_license_and_source(name: str) -> None:
    data = load_dataset(name)
    assert data.info.citation in data.description.replace("\n  ", " ").replace("\n", " ") or (
        data.info.title in data.description
    )
    assert data.info.license_url in data.description
    assert data.info.source_url in data.description.replace("\n  ", "")


def test_info_is_complete(name: str) -> None:
    info = get_info(name)
    assert info.creators
    assert info.changes
    assert info.citation.strip()
    assert info.license in {"CC0-1.0", "CC-BY-4.0"}
    if info.doi:
        assert info.doi in info.citation


def test_loader_does_not_share_state_between_calls(name: str) -> None:
    first = load_dataset(name)
    first.X[0, 0] = -12345.0
    assert load_dataset(name).X[0, 0] != -12345.0
