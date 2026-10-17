import re

import pyml_datasets
from pyml_datasets import list_datasets


def test_version_is_a_semantic_version_string() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", pyml_datasets.__version__)


def test_all_names_exist() -> None:
    for name in pyml_datasets.__all__:
        assert hasattr(pyml_datasets, name), name


def test_all_has_no_duplicates() -> None:
    assert len(set(pyml_datasets.__all__)) == len(pyml_datasets.__all__)


def test_public_api_is_exported() -> None:
    for name in ("Dataset", "DatasetInfo", "get_info", "list_datasets", "load_dataset"):
        assert name in pyml_datasets.__all__


def test_every_dataset_has_an_exported_loader() -> None:
    for name in list_datasets():
        assert f"load_{name}" in pyml_datasets.__all__
        assert callable(getattr(pyml_datasets, f"load_{name}"))


def test_removed_datasets_are_gone() -> None:
    for name in ("diabetes", "linnerud", "california_housing"):
        assert name not in list_datasets()
        assert not hasattr(pyml_datasets, f"load_{name}")
