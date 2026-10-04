"""Tests for the bundled datasets: shared contract plus per-dataset facts."""

from collections.abc import Callable
from typing import NamedTuple

import numpy as np
import pytest

from pyml_datasets import (
    load_breast_cancer,
    load_california_housing,
    load_diabetes,
    load_iris,
    load_linnerud,
    load_wine,
)
from pyml_datasets._loader import Dataset


class _Expected(NamedTuple):
    """What a dataset must look like, independent of how it was built."""

    loader: Callable[[], Dataset]
    n_samples: int
    n_features: int
    y_shape: tuple[int, ...]
    n_classes: int | None  # None for regression
    n_target_names: int | None  # None if the source has no target names


_CASES = [
    pytest.param(_Expected(load_iris, 150, 4, (150,), 3, 3), id="iris"),
    pytest.param(_Expected(load_wine, 178, 13, (178,), 3, 3), id="wine"),
    pytest.param(_Expected(load_breast_cancer, 569, 30, (569,), 2, 2), id="breast_cancer"),
    pytest.param(_Expected(load_diabetes, 442, 10, (442,), None, None), id="diabetes"),
    pytest.param(_Expected(load_linnerud, 20, 3, (20, 3), None, 3), id="linnerud"),
    pytest.param(
        _Expected(load_california_housing, 20640, 8, (20640,), None, 1),
        id="california_housing",
    ),
]


# ----------------------------- shared contract ----------------------------- #


@pytest.mark.parametrize("case", _CASES)
def test_returns_dataset(case: _Expected):
    assert isinstance(case.loader(), Dataset)


@pytest.mark.parametrize("case", _CASES)
def test_shapes(case: _Expected):
    data = case.loader()
    assert data.X.shape == (case.n_samples, case.n_features)
    assert data.y.shape == case.y_shape


@pytest.mark.parametrize("case", _CASES)
def test_X_is_finite_float64(case: _Expected):
    X = case.loader().X
    assert X.dtype == np.float64
    assert np.isfinite(X).all()


@pytest.mark.parametrize("case", _CASES)
def test_y_dtype_and_labels(case: _Expected):
    y = case.loader().y
    if case.n_classes is None:
        assert y.dtype == np.float64
        assert np.isfinite(y).all()
    else:
        assert y.dtype == np.int64
        assert set(np.unique(y)) == set(range(case.n_classes))


@pytest.mark.parametrize("case", _CASES)
def test_feature_names(case: _Expected):
    names = case.loader().feature_names
    assert isinstance(names, tuple)
    assert len(names) == case.n_features
    assert all(isinstance(name, str) and name for name in names)


@pytest.mark.parametrize("case", _CASES)
def test_target_names(case: _Expected):
    names = case.loader().target_names
    if case.n_target_names is None:
        assert names is None
    else:
        assert isinstance(names, tuple)
        assert len(names) == case.n_target_names
        assert all(isinstance(name, str) and name for name in names)


@pytest.mark.parametrize("case", _CASES)
def test_description_is_non_empty_text(case: _Expected):
    description = case.loader().description
    assert isinstance(description, str)
    assert description.strip()


@pytest.mark.parametrize("case", _CASES)
def test_unpacks_into_X_and_y(case: _Expected):
    data = case.loader()
    X, y = data
    assert X is data.X
    assert y is data.y


@pytest.mark.parametrize("case", _CASES)
def test_repeated_calls_return_equal_data(case: _Expected):
    first, second = case.loader(), case.loader()
    np.testing.assert_array_equal(first.X, second.X)
    np.testing.assert_array_equal(first.y, second.y)


@pytest.mark.parametrize("case", _CASES)
def test_repeated_calls_return_independent_arrays(case: _Expected):
    first, second = case.loader(), case.loader()
    assert first is not second
    assert not np.shares_memory(first.X, second.X)
    assert not np.shares_memory(first.y, second.y)


# --------------------------- dataset-specific facts --------------------------- #


def test_iris_classes_are_balanced():
    assert np.bincount(load_iris().y).tolist() == [50, 50, 50]


def test_iris_target_names_order():
    assert load_iris().target_names == ("setosa", "versicolor", "virginica")


def test_wine_class_counts():
    assert np.bincount(load_wine().y).tolist() == [59, 71, 48]


def test_breast_cancer_class_counts_and_label_order():
    data = load_breast_cancer()
    assert data.target_names == ("malignant", "benign")
    assert np.bincount(data.y).tolist() == [212, 357]


def test_diabetes_features_are_unscaled():
    # The scaled variant is mean-centered; the raw one keeps age in years.
    assert load_diabetes().X[:, 0].mean() > 40


def test_diabetes_target_is_positive():
    assert load_diabetes().y.min() > 0


def test_linnerud_is_multi_output_with_matching_target_names():
    data = load_linnerud()
    assert data.y.ndim == 2
    assert data.target_names is not None
    assert len(data.target_names) == data.y.shape[1]


def test_california_housing_target_is_positive():
    assert load_california_housing().y.min() > 0
