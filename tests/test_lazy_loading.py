"""Importing the package, listing the datasets and using one dataset import no other dataset."""

import json
import subprocess
import sys

import pytest

import pyml_datasets
from pyml_datasets import list_datasets

_PROBE = """
import json, sys
import pyml_datasets as package
{code}
loaded = sorted(
    name.rsplit(".", 1)[1] for name in sys.modules if name.startswith("pyml_datasets.datasets.")
)
print(json.dumps(loaded))
"""


def _loaded_after(code: str) -> list[str]:
    result = subprocess.run(
        [sys.executable, "-c", _PROBE.format(code=code)],
        capture_output=True,
        text=True,
        check=True,
    )
    loaded: list[str] = json.loads(result.stdout)
    return loaded


def test_import_loads_no_dataset_module() -> None:
    assert _loaded_after("") == []


def test_listing_loads_no_dataset_module() -> None:
    assert _loaded_after("package.list_datasets(); package.list_datasets('regression')") == []


def test_get_info_loads_only_that_dataset() -> None:
    assert _loaded_after("package.get_info('iris')") == ["iris"]


def test_loader_attribute_loads_only_that_dataset() -> None:
    assert _loaded_after("package.load_wine()") == ["wine"]


def test_load_dataset_loads_only_that_dataset() -> None:
    assert _loaded_after("package.load_dataset('iris')") == ["iris"]


def test_star_import_works() -> None:
    namespace: dict[str, object] = {}
    exec("from pyml_datasets import *", namespace)  # noqa: S102
    assert callable(namespace["load_iris"])


def test_loader_is_cached_in_the_module() -> None:
    loader = pyml_datasets.load_iris
    assert vars(pyml_datasets)["load_iris"] is loader


def test_misspelled_loader_raises_attribute_error() -> None:
    with pytest.raises(AttributeError, match="no attribute 'load_irsi'"):
        pyml_datasets.load_irsi  # type: ignore[attr-defined]  # noqa: B018
    with pytest.raises(AttributeError, match="no attribute 'iris'"):
        pyml_datasets.iris  # type: ignore[attr-defined]  # noqa: B018


def test_dir_lists_every_loader_before_it_is_imported() -> None:
    names = dir(pyml_datasets)
    assert names == sorted(pyml_datasets.__all__)
    assert {f"load_{name}" for name in list_datasets()} <= set(names)
