"""The generated index must already be in the form that ruff produces."""

import ast

import pytest

from scripts.generate import render_datasets_init, render_package_stub

_MAX_LINE = 100


@pytest.mark.parametrize("count", [1, 3, 8, 30])
def test_generated_index_keeps_lines_short_and_one_entry_per_line(count: int) -> None:
    tasks = {f"dataset_{index:02d}": "classification" for index in range(count)}
    text = render_datasets_init(tasks)
    assert all(len(line) <= _MAX_LINE for line in text.splitlines())
    for name in tasks:
        assert f'\n    "{name}": "classification",\n' in text


def test_generated_index_is_valid_python_that_imports_no_dataset() -> None:
    text = render_datasets_init({"a_set": "regression", "b_set": "classification"})
    tree = ast.parse(text)
    imports = [node for node in tree.body if isinstance(node, ast.Import | ast.ImportFrom)]
    assert [node.module for node in imports if isinstance(node, ast.ImportFrom)] == [
        "collections.abc",
        "typing",
        "_types",
    ]


def test_generated_index_does_not_depend_on_the_number_of_datasets() -> None:
    few = render_datasets_init({"a_set": "regression"})
    many = render_datasets_init({"a_set": "regression", "b_set": "classification"})
    assert few.split("DATASET_TASKS")[0] == many.split("DATASET_TASKS")[0]


def test_stub_re_exports_every_loader_and_the_public_names() -> None:
    names = ["a_set", "b_set"]
    stub = render_package_stub(names)
    for name in names:
        assert f"from .datasets.{name} import load_{name} as load_{name}\n" in stub
    for public in ("get_info", "list_datasets", "load_dataset", "Dataset", "DatasetInfo"):
        assert f" import {public} as {public}\n" in stub
    assert all(len(line) <= _MAX_LINE for line in stub.splitlines())


def test_stub_wraps_an_import_that_passes_the_line_length() -> None:
    name = "a_dataset_with_a_long_name_" + "x" * 8
    stub = render_package_stub([name])
    assert f"from .datasets.{name} import (\n    load_{name} as load_{name},\n)\n" in stub
    assert all(len(line) <= _MAX_LINE for line in stub.splitlines())
