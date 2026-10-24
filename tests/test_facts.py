"""Compare every data file with the facts written down in ``tests/expected``."""

import numpy as np
import pytest

from pyml_datasets import load_dataset
from tests.expected import all_expected


def test_every_dataset_has_expected_facts(name: str) -> None:
    assert name in all_expected(), f"Add tests/expected/{name}.py"


def test_no_expected_facts_without_a_dataset() -> None:
    from pyml_datasets import list_datasets

    assert set(all_expected()) == set(list_datasets())


def test_shape_and_missing(name: str) -> None:
    expected, data = all_expected()[name], load_dataset(name)
    assert data.X.shape == expected.shape
    assert int(np.isnan(data.X).sum()) == expected.n_missing


def test_classes(name: str) -> None:
    expected, data = all_expected()[name], load_dataset(name)
    if expected.n_classes is None:
        assert data.info.task == "regression"
        return
    assert np.unique(data.y).size == expected.n_classes
    if expected.class_counts is not None:
        assert tuple(np.bincount(data.y).tolist()) == expected.class_counts


def test_first_row(name: str) -> None:
    expected, data = all_expected()[name], load_dataset(name)
    count = len(expected.first_row)
    np.testing.assert_allclose(data.X[0, :count], expected.first_row)


def test_published_means(name: str) -> None:
    expected, data = all_expected()[name], load_dataset(name)
    for column, mean in expected.column_means.items():
        assert float(np.nanmean(data.X[:, column])) == pytest.approx(
            mean, abs=expected.mean_tolerance
        )
