"""An evidence file is complete only with an archived page and a maintainer confirmation."""

from datetime import date
from pathlib import Path

import pytest

from scripts import check_legal
from scripts.check_legal import Problems, check_info
from tests.conftest import make_info

TODAY = date(2026, 10, 23)
PAGE = "https://archive.ics.uci.edu/dataset/222/bank+marketing"
ARCHIVE = f"https://web.archive.org/web/20261023054004/{PAGE}"
CHECK = "Sherzod, 2026-10-23"


def run(
    folder: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    archive: str = ARCHIVE,
    check: str = CHECK,
) -> Problems:
    """Check a tiny dataset whose evidence file has the given ``Archive`` and check fields."""
    monkeypatch.setattr(check_legal, "EVIDENCE_DIR", folder)
    (folder / "tiny.md").write_text(
        "# Evidence: Tiny (`tiny`)\n\n"
        "- **License:** CC0-1.0\n"
        f"- **License page:** {PAGE}\n"
        "- **Checked:** 2026-10-17\n"
        "- **Checked by:** Someone\n"
        f"- **Archive:** {archive}\n"
        f"- **Maintainer check:** {check}\n",
        "utf-8",
    )
    problems = Problems()
    check_info(make_info(), problems, TODAY)
    return problems


def test_complete_evidence_has_no_problems(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    problems = run(tmp_path, monkeypatch)
    assert problems.errors == []
    assert problems.warnings == []


@pytest.mark.parametrize("archive", ["pending", "Pending", "none", ""])
def test_missing_archive_is_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, archive: str
) -> None:
    problems = run(tmp_path, monkeypatch, archive=archive)
    assert any("no archived copy" in error for error in problems.errors)


@pytest.mark.parametrize(
    "archive",
    [
        PAGE,
        "http://web.archive.org/web/20261023054004/" + PAGE,
        "https://web.archive.org/web/2026/" + PAGE,
        "https://example.org/web/20261023054004/" + PAGE,
    ],
)
def test_archive_must_be_a_wayback_link_with_a_timestamp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, archive: str
) -> None:
    problems = run(tmp_path, monkeypatch, archive=archive)
    assert any("Archive must be a link" in error for error in problems.errors)


def test_archive_of_another_page_is_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    other = "https://web.archive.org/web/20261023054004/https://archive.ics.uci.edu/dataset/53/iris"
    problems = run(tmp_path, monkeypatch, archive=other)
    assert any("not of the license page" in error for error in problems.errors)


@pytest.mark.parametrize(
    "original",
    [
        "https://archive.ics.uci.edu/dataset/222/bank%2Bmarketing",
        "https://archive.ics.uci.edu/dataset/222/bank+marketing/",
        "http://archive.ics.uci.edu/dataset/222/bank+marketing",
        "https://www.archive.ics.uci.edu/dataset/222/bank+marketing",
    ],
)
def test_spelling_of_the_same_address_is_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, original: str
) -> None:
    problems = run(
        tmp_path, monkeypatch, archive=f"https://web.archive.org/web/20261023054004/{original}"
    )
    assert problems.errors == []


@pytest.mark.parametrize("check", ["pending", "Pending since Monday", ""])
def test_unconfirmed_maintainer_check_is_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, check: str
) -> None:
    problems = run(tmp_path, monkeypatch, check=check)
    assert any("has not confirmed" in error for error in problems.errors)


@pytest.mark.parametrize(
    "check", ["Sherzod", "2026-10-23", "Sherzod, 2026-13-40", "ok, 23.10.2026"]
)
def test_maintainer_check_needs_a_name_and_a_real_date(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, check: str
) -> None:
    problems = run(tmp_path, monkeypatch, check=check)
    assert any("must give a name and a date" in error for error in problems.errors)


def test_maintainer_check_cannot_be_dated_in_the_future(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    problems = run(tmp_path, monkeypatch, check="Sherzod, 2026-10-24")
    assert any("in the future" in error for error in problems.errors)


def test_future_date_error_tells_to_write_utc(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    problems = run(tmp_path, monkeypatch, check="Sherzod, 2026-10-24")
    assert any("Write dates in UTC" in error for error in problems.errors)


def test_the_gate_takes_today_from_the_utc_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    days: list[date] = []
    monkeypatch.setattr(check_legal, "utc_today", lambda: date(2026, 10, 24))
    monkeypatch.setattr(check_legal, "check_info", lambda info, problems, today: days.append(today))
    check_legal.collect_problems()
    assert days
    assert set(days) == {date(2026, 10, 24)}
