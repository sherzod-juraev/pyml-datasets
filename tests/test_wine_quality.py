import zipfile
from pathlib import Path

import numpy as np
import pytest

import pyml_datasets
from pyml_datasets import Dataset

# Reference values of the original UCI Wine Quality data (red and white wines combined).
# Adjust them if wine_quality.npz was built differently (deduplicated, extra columns, ...).
N_SAMPLES = 6497
FEATURE_NAMES = (
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
)
QUALITY_COUNTS = {3: 30, 4: 216, 5: 2138, 6: 2836, 7: 1079, 8: 193, 9: 5}

# Generous (min, max) bounds per feature, wide enough for the real data.
VALUE_RANGES = {
    "fixed_acidity": (3.0, 16.5),
    "volatile_acidity": (0.05, 1.7),
    "citric_acid": (0.0, 1.8),
    "residual_sugar": (0.5, 66.0),
    "chlorides": (0.005, 0.65),
    "free_sulfur_dioxide": (0.5, 300.0),
    "total_sulfur_dioxide": (5.0, 450.0),
    "density": (0.98, 1.04),
    "pH": (2.6, 4.1),
    "sulphates": (0.2, 2.1),
    "alcohol": (7.9, 15.5),
}

REQUIRED_KEYS = {"X", "y", "feature_names", "description"}
DATA_FILE = Path(pyml_datasets.__file__).parent / "data" / "wine_quality.npz"


@pytest.fixture(scope="module")
def dataset() -> Dataset:
    return pyml_datasets.load_wine_quality()


def test_archive_is_not_corrupted() -> None:
    with zipfile.ZipFile(DATA_FILE) as archive:
        assert archive.testzip() is None


def test_required_arrays_are_present_and_loadable() -> None:
    with np.load(DATA_FILE, allow_pickle=False) as npz:
        assert REQUIRED_KEYS <= set(npz.files)
        arrays = {key: npz[key] for key in npz.files}
    assert len(arrays) == len(set(arrays))


def test_loader_returns_the_stored_arrays(dataset: Dataset) -> None:
    with np.load(DATA_FILE, allow_pickle=False) as npz:
        np.testing.assert_array_equal(dataset.X, npz["X"])
        np.testing.assert_array_equal(dataset.y, npz["y"])


def test_shapes(dataset: Dataset) -> None:
    assert dataset.X.shape == (N_SAMPLES, len(FEATURE_NAMES))
    assert dataset.y.shape == (N_SAMPLES,)


def test_X_is_float64_and_finite(dataset: Dataset) -> None:
    assert dataset.X.dtype == np.float64
    assert np.isfinite(dataset.X).all()


def test_y_holds_integer_quality_scores(dataset: Dataset) -> None:
    assert dataset.y.dtype.kind in "if"
    np.testing.assert_array_equal(dataset.y, np.round(dataset.y))
    assert dataset.y.min() == 3
    assert dataset.y.max() == 9


def test_quality_counts(dataset: Dataset) -> None:
    values, counts = np.unique(dataset.y, return_counts=True)
    assert dict(zip(values.astype(int).tolist(), counts.tolist(), strict=True)) == QUALITY_COUNTS


def test_feature_names(dataset: Dataset) -> None:
    assert dataset.feature_names == FEATURE_NAMES


@pytest.mark.parametrize("name", sorted(VALUE_RANGES))
def test_feature_values_are_in_physical_range(dataset: Dataset, name: str) -> None:
    low, high = VALUE_RANGES[name]
    column = dataset.X[:, dataset.feature_names.index(name)]
    assert column.min() >= low
    assert column.max() <= high


def test_description_is_not_empty(dataset: Dataset) -> None:
    assert dataset.description.strip()
