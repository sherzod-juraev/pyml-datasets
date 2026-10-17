import pytest

import pyml_datasets
from pyml_datasets import DatasetInfo, get_info, list_datasets, load_dataset
from pyml_datasets._registry import REGISTRY


def test_list_datasets_is_sorted_and_not_empty() -> None:
    names = list_datasets()
    assert names
    assert list(names) == sorted(names)


def test_list_by_task_partitions_the_datasets() -> None:
    classification = set(list_datasets("classification"))
    regression = set(list_datasets("regression"))
    assert classification | regression == set(list_datasets())
    assert not classification & regression


def test_registry_matches_list() -> None:
    assert tuple(sorted(REGISTRY)) == list_datasets()


def test_get_info_returns_the_info(name: str) -> None:
    info = get_info(name)
    assert isinstance(info, DatasetInfo)
    assert info.name == name


def test_load_dataset_equals_the_named_loader(name: str) -> None:
    by_name = load_dataset(name)
    by_loader = getattr(pyml_datasets, f"load_{name}")()
    assert by_name.info == by_loader.info
    assert by_name.X.shape == by_loader.X.shape


@pytest.mark.parametrize("function", [get_info, load_dataset])
def test_unknown_name_lists_the_available_datasets(function) -> None:
    with pytest.raises(ValueError, match="Unknown dataset 'nope'.*iris"):
        function("nope")
