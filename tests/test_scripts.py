"""Tests of the development scripts: validation, scaffolding and generated blocks."""

from datetime import UTC, date, datetime, tzinfo
from pathlib import Path
from typing import Any, Self

import numpy as np
import pytest
from numpy.typing import NDArray

import scripts
from pyml_datasets import get_info, list_datasets
from scripts import new_dataset
from scripts._npz import array_digest, to_arrays, validate
from scripts._render import render_datasets_toctree
from scripts.generate import replace_block
from scripts.recipes import get_recipe, recipe_names
from scripts.recipes._common import Built
from tests.conftest import make_info


def _arrays(**changes: Any) -> dict[str, NDArray[Any]]:
    built = Built(
        X=changes.pop("X", [[1.0, 2.0], [3.0, 4.0]]),
        y=changes.pop("y", [0, 1]),
        feature_names=changes.pop("names", ["a", "b"]),
    )
    return to_arrays(built, make_info(**changes))


def test_valid_arrays_pass() -> None:
    validate(make_info(), _arrays())


def test_nan_requires_has_missing() -> None:
    arrays = _arrays(X=[[np.nan, 2.0], [3.0, 4.0]])
    with pytest.raises(ValueError, match="has_missing is False"):
        validate(make_info(), arrays)
    validate(make_info(has_missing=True), arrays)


def test_has_missing_without_nan_fails() -> None:
    with pytest.raises(ValueError, match="no NaN"):
        validate(make_info(has_missing=True), _arrays())


def test_target_must_not_be_missing() -> None:
    arrays = _arrays(task="regression", y=[1.0, np.nan])
    with pytest.raises(ValueError, match="y must never"):
        validate(make_info(task="regression"), arrays)


def test_labels_must_start_at_zero() -> None:
    with pytest.raises(ValueError, match="0 .. n_classes"):
        validate(make_info(), _arrays(y=[1, 2]))


def test_infinite_values_fail() -> None:
    with pytest.raises(ValueError, match="infinite"):
        validate(make_info(), _arrays(X=[[np.inf, 2.0], [3.0, 4.0]]))


def test_categorical_codes_are_checked() -> None:
    info = make_info(categorical={"a": ("x", "y")})
    validate(info, _arrays(categorical={"a": ("x", "y")}, X=[[0.0, 2.0], [1.0, 4.0]]))
    with pytest.raises(ValueError, match="without a category"):
        validate(info, _arrays(X=[[0.0, 2.0], [5.0, 4.0]]))


def test_digest_depends_on_dtype_shape_and_values() -> None:
    base = np.arange(6, dtype=np.float64)
    assert array_digest(base) == array_digest(base.copy())
    assert array_digest(base) != array_digest(base.astype(np.float32))
    assert array_digest(base) != array_digest(base.reshape(2, 3))
    assert array_digest(base) != array_digest(base + 1)


def test_replace_block() -> None:
    text = "a\n    # <generated:x>\n    old\n    # </generated:x>\nb\n"
    assert replace_block(text, "x", "    new\n") == (
        "a\n    # <generated:x>\n    new\n    # </generated:x>\nb\n"
    )
    with pytest.raises(ValueError, match="not found"):
        replace_block("nothing", "x", "")


def test_every_recipe_has_a_dataset(name: str) -> None:
    assert name in recipe_names()


def test_unknown_recipe_is_an_error() -> None:
    with pytest.raises(ValueError, match="No recipe"):
        get_recipe("nope")


def test_new_dataset_scaffold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for folder in (
        "pyml_datasets/datasets",
        "scripts/recipes",
        "tests/expected",
        "docs/source/datasets",
        "legal/evidence",
    ):
        (tmp_path / folder).mkdir(parents=True)
    monkeypatch.setattr(new_dataset, "ROOT", tmp_path)
    created = new_dataset.create("seeds", "CC-BY-4.0", "classification", "2026-10-17")
    assert len(created) == 5
    module = (tmp_path / "pyml_datasets/datasets/seeds.py").read_text("utf-8")
    assert "def load_seeds()" in module
    assert "TODO" in module
    compile(module, "seeds.py", "exec")
    with pytest.raises(FileExistsError):
        new_dataset.create("seeds", "CC-BY-4.0", "classification", "2026-10-17")


def test_new_dataset_writes_the_utc_date(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for folder in (
        "pyml_datasets/datasets",
        "scripts/recipes",
        "tests/expected",
        "docs/source/datasets",
        "legal/evidence",
    ):
        (tmp_path / folder).mkdir(parents=True)
    monkeypatch.setattr(new_dataset, "ROOT", tmp_path)
    monkeypatch.setattr(new_dataset, "utc_today", lambda: date(2026, 10, 24))
    argv = ["seeds", "--license", "CC0-1.0", "--task", "classification"]
    assert new_dataset.main(argv) == 0
    evidence = (tmp_path / "legal/evidence/seeds.md").read_text("utf-8")
    assert "**Checked:** 2026-10-24" in evidence


def test_utc_today_uses_the_utc_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    class Clock(datetime):
        """19:44 UTC on 2026-10-24, which is already the 25th in Tashkent (UTC+5)."""

        @classmethod
        def now(cls, tz: tzinfo | None = None) -> Self:
            return cls(2026, 10, 24, 19, 44, tzinfo=UTC).astimezone(tz)

    monkeypatch.setattr(scripts, "datetime", Clock)
    assert scripts.utc_today() == date(2026, 10, 24)


@pytest.mark.parametrize(("name", "license_id"), [("Bad", "CC0-1.0"), ("ok", "MIT")])
def test_new_dataset_rejects_bad_input(name: str, license_id: str) -> None:
    with pytest.raises(ValueError):
        new_dataset.create(name, license_id, "classification", "2026-10-17")


def test_datasets_toctree_is_hidden_and_ends_with_a_newline() -> None:
    text = render_datasets_toctree([get_info("iris")])
    assert text.splitlines()[:3] == [".. toctree::", "   :hidden:", ""]
    assert text.endswith("\n")


def test_datasets_toctree_lists_every_dataset_sorted_by_name() -> None:
    names = list_datasets()
    infos = [get_info(name) for name in reversed(names)]
    entries = [line.strip() for line in render_datasets_toctree(infos).splitlines()[3:]]
    assert entries == [f"{name}" for name in sorted(names)]
