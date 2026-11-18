"""Tests of the options of ``pyml-datasets list`` that filter and page the rows."""

import pytest

from pyml_datasets import get_info, list_datasets
from pyml_datasets._cli import _commands, main
from pyml_datasets._cli._commands import matches_name

NAMES = list_datasets()


@pytest.fixture(autouse=True)
def wide_terminal(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make lines so long that rich never wraps a value in the captured output."""
    monkeypatch.setenv("COLUMNS", "1000")
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)


def _listed(capsys: pytest.CaptureFixture[str]) -> list[str]:
    """Return the dataset names of the ``list`` table in the order they are printed."""
    lines = capsys.readouterr().out.splitlines()
    return [line.split()[0] for line in lines if line.split()[:1] and line.split()[0] in NAMES]


@pytest.mark.parametrize(
    ("name", "pattern", "expected"),
    [
        ("wine_quality", "wine*", True),
        ("wine_quality", "*quality", True),
        ("wine_quality", "*ine_q*", True),
        ("wine_quality", "WINE*", True),
        ("wine_quality", "wine", False),
        ("wine", "wine", True),
        ("iris", "ir?s", True),
        ("iris", "ir?", False),
        ("iris", "[hi]ris", True),
        ("iris", "[abc]ris", False),
        ("wine_quality", "wine%", True),
        ("wine_quality", "%quality", True),
        ("wine_quality", "%ine%", True),
        ("wine_quality", "wine_quality", True),
        ("wine_quality", "wine_q%", True),
        ("wineXquality", "wine_quality", False),
        ("wine_quality", "w_ne%", False),
    ],
)
def test_matches_name_works_like_like_in_sql(name: str, pattern: str, expected: bool) -> None:
    assert matches_name(name, pattern) is expected


@pytest.mark.parametrize(
    "pattern", ["wine*", "WINE*", "*wine*", "wine*y", "w?ne*", "wine%", "%wine%", "%quality"]
)
def test_name_keeps_the_datasets_that_match(
    pattern: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["list", "--name", pattern]) == 0
    expected = [name for name in NAMES if matches_name(name, pattern)]
    assert expected, "the test needs a pattern that matches"
    assert _listed(capsys) == expected


def test_a_name_without_a_wildcard_has_to_match_the_whole_name(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["list", "--name", "wine"])
    assert _listed(capsys) == ["wine"]


def test_a_name_without_a_wildcard_tells_how_to_match_more(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["list", "--name", "wine"])
    output = capsys.readouterr().out
    assert " ".join(output.split()).count("Tip:") == 1
    assert 'Use "wine*" for the names that start with it' in " ".join(output.split())
    assert '"*wine*" for the names that contain it' in " ".join(output.split())


@pytest.mark.parametrize("pattern", ["wine*", "wine%", "w?ne", "*wine", "iris", "abalone"])
def test_there_is_no_tip_when_it_would_not_help(
    pattern: str, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["list", "--name", pattern])
    assert "Tip:" not in capsys.readouterr().out


def test_the_tip_comes_with_the_message_when_nothing_matches(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["list", "--name", "quality"]) == 0
    output = " ".join(capsys.readouterr().out.split())
    assert output.startswith("No dataset matches the filters. Tip:")
    assert '"*quality*" for the names that contain it' in output


def test_the_tip_looks_at_the_datasets_of_the_task_only(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["list", "--name", "wine", "--task", "classification"])
    assert "Tip:" not in capsys.readouterr().out
    main(["list", "--name", "wine", "--task", "regression"])
    assert "Tip:" in capsys.readouterr().out


def test_an_underscore_is_an_ordinary_character(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list", "--name", "wine_quality"])
    assert _listed(capsys) == ["wine_quality"]
    main(["list", "--name", "w_ne*"])
    assert "No dataset matches the filters." in capsys.readouterr().out


def test_one_dataset_is_not_called_datasets(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list", "--name", "iris"])
    output = capsys.readouterr().out
    assert "1 dataset: classification 1" in output
    assert "1 datasets" not in output


def test_a_name_that_matches_nothing_says_so(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list", "--name", "nothing*"]) == 0
    output = capsys.readouterr().out
    assert "No dataset matches the filters." in output
    assert "datasets:" not in output


@pytest.mark.parametrize("wanted", [True, False])
def test_missing_keeps_the_datasets_with_or_without_missing_values(
    wanted: bool, capsys: pytest.CaptureFixture[str]
) -> None:
    flag = "--missing" if wanted else "--no-missing"
    assert main(["list", flag]) == 0
    expected = [name for name in NAMES if get_info(name).has_missing is wanted]
    assert expected, "the test needs datasets of both kinds"
    assert _listed(capsys) == expected


def test_the_filters_work_together(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list", "--task", "classification", "--name", "*e*", "--no-missing", "--sort", "samples"])
    shown = _listed(capsys)
    assert shown
    for name in shown:
        assert get_info(name).task == "classification"
        assert "e" in name
        assert not get_info(name).has_missing


def test_limit_shows_the_first_rows_and_says_how_many_there_are(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["list", "--limit", "3"]) == 0
    output = capsys.readouterr().out
    assert [
        line.split()[0]
        for line in output.splitlines()
        if line.split()[:1] and line.split()[0] in NAMES
    ] == sorted(NAMES)[:3]
    assert f"Showing 1-3 of {len(NAMES)}. Use --offset or --all to see more." in output
    assert "3 datasets:" in output


def test_offset_skips_rows_after_the_order_is_applied(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["list", "--sort", "samples", "--reverse"])
    everything = _listed(capsys)
    main(["list", "--sort", "samples", "--reverse", "--offset", "4", "--limit", "3"])
    output = capsys.readouterr().out
    assert f"Showing 5-7 of {len(NAMES)}." in output
    shown = [word for word in output.split() if word in NAMES]
    assert shown == everything[4:7]


def test_the_last_page_has_no_hint_to_see_more(capsys: pytest.CaptureFixture[str]) -> None:
    total = len(NAMES)
    main(["list", "--offset", str(total - 2)])
    output = capsys.readouterr().out
    assert f"Showing {total - 1}-{total} of {total}." in output
    assert "to see more" not in output


def test_the_default_limit_cuts_a_long_list(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(_commands, "DEFAULT_LIMIT", 5)
    assert main(["list"]) == 0
    output = capsys.readouterr().out
    assert [word for word in output.split() if word in NAMES] == sorted(NAMES)[:5]
    assert f"Showing 1-5 of {len(NAMES)}. Use --offset or --all to see more." in output


def test_all_shows_every_row_whatever_the_default_limit(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(_commands, "DEFAULT_LIMIT", 5)
    main(["list", "--all"])
    output = capsys.readouterr().out
    assert [word for word in output.split() if word in NAMES] == sorted(NAMES)
    assert "Showing" not in output


def test_all_with_an_offset_shows_the_rest(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list", "--all", "--offset", "2"])
    output = capsys.readouterr().out
    assert [word for word in output.split() if word in NAMES] == sorted(NAMES)[2:]
    assert f"Showing 3-{len(NAMES)} of {len(NAMES)}." in output


def test_the_table_shows_everything_when_nothing_is_cut(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["list", "--limit", str(len(NAMES))])
    output = capsys.readouterr().out
    assert "Showing" not in output
    assert f"{len(NAMES)} datasets:" in output


def test_an_offset_past_the_end_says_so(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list", "--offset", "1000"]) == 0
    output = capsys.readouterr().out
    assert f"The offset 1000 is past the end: {len(NAMES)} datasets match." in output


def test_an_offset_past_a_single_row_says_dataset_matches(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["list", "--name", "iris", "--offset", "1"])
    assert "The offset 1 is past the end: 1 dataset matches." in capsys.readouterr().out


@pytest.mark.parametrize(
    "argv",
    [
        ["list", "--limit", "0"],
        ["list", "--limit", "-1"],
        ["list", "--limit", "many"],
        ["list", "--limit"],
        ["list", "--offset", "-1"],
        ["list", "--offset", "1.5"],
        ["list", "--all", "--limit", "3"],
        ["list", "--limit", "3", "--all"],
        ["list", "--name"],
    ],
)
def test_wrong_values_are_an_error(argv: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as stop:
        main(argv)
    assert stop.value.code == 2
    assert "error:" in capsys.readouterr().err
