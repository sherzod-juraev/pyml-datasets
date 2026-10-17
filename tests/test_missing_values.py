"""Missing values and categorical features: what the format promises."""

import numpy as np

from pyml_datasets import load_dataset, load_penguins
from pyml_datasets.datasets import ENTRIES


def test_has_missing_in_info_matches_the_data(name: str) -> None:
    data = load_dataset(name)
    assert data.has_missing == data.info.has_missing == bool(np.isnan(data.X).any())


def test_targets_are_never_missing(name: str) -> None:
    assert not np.isnan(load_dataset(name).y.astype(float)).any()


def test_categorical_columns_hold_valid_codes(name: str) -> None:
    data = load_dataset(name)
    for feature, categories in data.info.categorical.items():
        column = data.X[:, data.feature_names.index(feature)]
        codes = column[~np.isnan(column)]
        assert np.array_equal(codes, np.round(codes))
        assert codes.min() >= 0
        assert codes.max() < len(categories)


def test_categorical_features_are_column_indices(name: str) -> None:
    data = load_dataset(name)
    names = [data.feature_names[index] for index in data.categorical_features]
    assert set(names) == set(data.info.categorical)


def test_penguins_example() -> None:
    data = load_penguins()
    assert data.has_missing
    assert [data.feature_names[i] for i in data.categorical_features] == ["island", "sex"]
    assert data.info.categorical["sex"] == ("female", "male")


def test_some_dataset_without_missing_values_exists() -> None:
    assert any(not info.has_missing for info, _ in ENTRIES)
