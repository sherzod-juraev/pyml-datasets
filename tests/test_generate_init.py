"""The generated registry must already be in the form that ruff produces."""

import pytest

from scripts.generate import render_datasets_init

_MAX_LINE = 100


@pytest.mark.parametrize("count", [1, 3, 8, 30])
def test_generated_init_keeps_lines_short_and_one_import_per_line(count: int) -> None:
    names = [f"dataset_{index:02d}" for index in range(count)]
    text = render_datasets_init(names)
    assert all(len(line) <= _MAX_LINE for line in text.splitlines())
    for name in names:
        assert f"\n    {name},\n" in text
        assert f"    ({name}.INFO, {name}.load_{name}),\n" in text


def test_generated_init_does_not_depend_on_the_number_of_datasets() -> None:
    few, many = render_datasets_init(["a_set"]), render_datasets_init(["a_set", "b_set"])
    assert few.startswith(many.split("from . import (")[0])
    assert "from . import (\n    a_set,\n)\n" in few
