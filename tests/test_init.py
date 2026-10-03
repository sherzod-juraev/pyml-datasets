import re

import pyml_datasets

EXPECTED_LOADERS = {
    "load_breast_cancer",
    "load_california_housing",
    "load_diabetes",
    "load_iris",
    "load_linnerud",
    "load_wine",
}


def test_version_is_a_semantic_version_string() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", pyml_datasets.__version__)


def test_all_names_exist() -> None:
    for name in pyml_datasets.__all__:
        assert hasattr(pyml_datasets, name), name


def test_all_has_no_duplicates() -> None:
    assert len(set(pyml_datasets.__all__)) == len(pyml_datasets.__all__)


def test_all_exports_dataset_and_version() -> None:
    assert "Dataset" in pyml_datasets.__all__
    assert "__version__" in pyml_datasets.__all__


def test_public_loaders() -> None:
    loaders = {name for name in pyml_datasets.__all__ if name.startswith("load_")}
    assert loaders == EXPECTED_LOADERS
