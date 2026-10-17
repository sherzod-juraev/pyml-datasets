"""The legal gate: what may enter the repository and what must be written down."""

from datetime import date
from pathlib import Path

import pytest

from pyml_datasets import list_datasets
from scripts import check_legal
from scripts.check_legal import Problems, check_info, collect_problems, license_expression_ids
from tests.conftest import make_info

ROOT = Path(__file__).resolve().parents[1]


def test_repository_passes_the_legal_check() -> None:
    assert collect_problems().errors == []


def test_every_license_text_is_shipped(name: str) -> None:
    from pyml_datasets import get_info

    assert (ROOT / "LICENSES" / f"{get_info(name).license}.txt").is_file()


def test_every_dataset_has_evidence_and_a_notice_entry(name: str) -> None:
    assert (ROOT / "legal" / "evidence" / f"{name}.md").is_file()
    assert f"(`{name}`)" in (ROOT / "NOTICE.md").read_text("utf-8")


def test_removed_datasets_are_not_distributed() -> None:
    for removed in ("diabetes", "linnerud", "california_housing"):
        assert not (ROOT / "pyml_datasets" / "data" / f"{removed}.npz").exists()
        assert removed not in list_datasets()


@pytest.mark.parametrize("license_id", ["MIT", "GPL-3.0-only", "CC-BY-NC-4.0", "CC-BY-SA-4.0", ""])
def test_other_licenses_cannot_be_declared(license_id: str) -> None:
    with pytest.raises(ValueError, match="license must be one of"):
        make_info(license=license_id)


def test_license_expression_is_split() -> None:
    assert license_expression_ids("MIT AND (CC0-1.0 OR CC-BY-4.0)") == {
        "MIT",
        "CC0-1.0",
        "CC-BY-4.0",
    }


def test_doi_must_be_in_the_citation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_legal, "EVIDENCE_DIR", tmp_path)
    problems = Problems()
    check_info(make_info(doi="10.1234/abc"), problems, date(2026, 10, 17))
    assert any("DOI" in error for error in problems.errors)


def test_missing_evidence_is_an_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_legal, "EVIDENCE_DIR", tmp_path)
    problems = Problems()
    check_info(make_info(), problems, date(2026, 10, 17))
    assert any("evidence file" in error for error in problems.errors)


def test_evidence_must_name_the_same_license(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(check_legal, "EVIDENCE_DIR", tmp_path)
    (tmp_path / "tiny.md").write_text(
        "- **License:** CC-BY-4.0\n- **License page:** https://example.org\n"
        "- **Checked:** 2026-10-17\n",
        "utf-8",
    )
    problems = Problems()
    check_info(make_info(), problems, date(2026, 10, 17))
    assert any("evidence says" in error for error in problems.errors)


def test_todo_is_an_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_legal, "EVIDENCE_DIR", tmp_path)
    problems = Problems()
    check_info(make_info(summary="TODO write this"), problems, date(2026, 10, 17))
    assert any("TODO" in error for error in problems.errors)


def test_old_verification_is_only_a_warning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(check_legal, "EVIDENCE_DIR", tmp_path)
    problems = Problems()
    check_info(make_info(), problems, date(2028, 1, 1))
    assert any("days ago" in warning for warning in problems.warnings)
    assert not any("days ago" in error for error in problems.errors)
