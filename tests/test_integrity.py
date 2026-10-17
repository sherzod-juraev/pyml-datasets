"""Data files are what the manifest and the dataset information say they are."""

import json
from pathlib import Path

import numpy as np

from pyml_datasets import get_info, list_datasets
from scripts._npz import manifest_entry
from scripts._render import info_json, render_description

DATA = Path(__file__).resolve().parents[1] / "pyml_datasets" / "data"


def _arrays(name: str) -> dict[str, np.ndarray]:
    with np.load(DATA / f"{name}.npz", allow_pickle=False) as archive:
        return {key: archive[key] for key in archive.files}


def test_manifest_lists_exactly_the_datasets() -> None:
    manifest = json.loads((DATA / "MANIFEST.json").read_text("utf-8"))
    assert set(manifest["datasets"]) == set(list_datasets())


def test_manifest_digests_match_the_files(name: str) -> None:
    manifest = json.loads((DATA / "MANIFEST.json").read_text("utf-8"))
    assert manifest["datasets"][name] == manifest_entry(_arrays(name))


def test_stored_meta_equals_the_info(name: str) -> None:
    stored = json.loads(str(_arrays(name)["meta"]))
    assert stored == get_info(name).to_dict()
    assert str(_arrays(name)["meta"]) == info_json(get_info(name))


def test_stored_description_is_the_rendered_one(name: str) -> None:
    assert str(_arrays(name)["description"]) == render_description(get_info(name))


def test_files_hold_no_pickled_objects(name: str) -> None:
    for array in _arrays(name).values():
        assert array.dtype != object


def test_build_extras_are_json(name: str) -> None:
    assert isinstance(json.loads(str(_arrays(name)["build"])), dict)
