"""Validation of ``DatasetInfo``: it must be impossible to describe a dataset badly."""

from typing import Any

import pytest

from tests.conftest import make_info


def test_a_valid_info_is_accepted() -> None:
    assert make_info().name == "tiny"


def test_to_dict_is_plain() -> None:
    data = make_info(categorical={"a": ("x", "y")}).to_dict()
    assert data["creators"] == ["Someone"]
    assert data["categorical"] == {"a": ["x", "y"]}


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"name": "Bad Name"}, "not a valid dataset name"),
        ({"task": "clustering"}, "task must be one of"),
        ({"license": "MIT"}, "license must be one of"),
        ({"license_url": "http://example.org"}, "https URL"),
        ({"source_url": "ftp://example.org"}, "https URL"),
        ({"doi": "not-a-doi"}, "not a valid DOI"),
        ({"creators": ()}, "creator"),
        ({"citation": "  "}, "citation"),
        ({"changes": ()}, "changes"),
        ({"verified_on": "yesterday"}, "ISO date"),
        ({"categorical": {"a": ()}}, "no categories"),
    ],
)
def test_bad_values_are_rejected(changes: dict[str, Any], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        make_info(**changes)


def test_info_is_frozen() -> None:
    with pytest.raises(AttributeError):
        make_info().name = "other"  # type: ignore[misc]
