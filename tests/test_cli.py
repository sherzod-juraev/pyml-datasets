"""Tests of the command line of the development scripts."""

import argparse
from collections.abc import Callable
from datetime import date
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from scripts import ROOT, build_datasets, check_legal, cli, generate, new_dataset


def _scaffold_folders(root: Path) -> None:
    for folder in (
        "pyml_datasets/datasets",
        "scripts/recipes",
        "tests/expected",
        "docs/source/datasets",
        "legal/evidence",
    ):
        (root / folder).mkdir(parents=True)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("cc0", "CC0-1.0"),
        ("CC0-1.0", "CC0-1.0"),
        ("by", "CC-BY-4.0"),
        ("BY", "CC-BY-4.0"),
        ("cc-by", "CC-BY-4.0"),
        ("cc-by-4.0", "CC-BY-4.0"),
    ],
)
def test_license_short_names(value: str, expected: str) -> None:
    assert cli.resolve_license(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("clf", "classification"),
        ("CLF", "classification"),
        ("classification", "classification"),
        ("reg", "regression"),
        ("Regression", "regression"),
    ],
)
def test_task_short_names(value: str, expected: str) -> None:
    assert cli.resolve_task(value) == expected


@pytest.mark.parametrize("resolve", [cli.resolve_license, cli.resolve_task])
def test_unknown_values_are_rejected(resolve: Callable[[str], str]) -> None:
    with pytest.raises(argparse.ArgumentTypeError, match="use one of"):
        resolve("mit")


def test_parser_turns_short_values_into_full_names() -> None:
    args = cli.build_parser().parse_args(["new", "seeds", "-l", "by", "-t", "clf"])
    assert (args.name, args.license_id, args.task) == ("seeds", "CC-BY-4.0", "classification")


def test_a_command_is_required() -> None:
    with pytest.raises(SystemExit) as stop:
        cli.main([])
    assert stop.value.code == 2


@pytest.mark.parametrize("module", [new_dataset, build_datasets, generate, check_legal])
def test_the_old_entry_points_are_gone(module: ModuleType) -> None:
    assert not hasattr(module, "main")


def test_new_refuses_to_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _scaffold_folders(tmp_path)
    monkeypatch.setattr(new_dataset, "ROOT", tmp_path)
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    argv = ["new", "seeds", "-l", "by", "-t", "reg"]
    assert cli.main(argv) == 0
    assert "legal/evidence/seeds.md" in capsys.readouterr().out
    assert cli.main(argv) == 1
    assert "Refusing to overwrite" in capsys.readouterr().err


def test_new_rejects_a_bad_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["new", "Not-Valid", "-l", "by", "-t", "clf"]) == 1
    assert "not a valid dataset name" in capsys.readouterr().err


def test_build_reports_an_unknown_dataset(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def forbidden(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("nothing may be built")

    monkeypatch.setattr(build_datasets, "build_dataset", forbidden)
    assert cli.main(["build", "no_such_dataset"]) == 2
    assert "No recipe for: no_such_dataset" in capsys.readouterr().err


def test_build_passes_the_options_and_prints_a_summary(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    calls: list[tuple[str, Path, bool]] = []

    def fake(name: str, output_dir: Path, overwrite: bool = False) -> build_datasets.BuildResult:
        calls.append((name, output_dir, overwrite))
        return build_datasets.BuildResult(name, overwrite, (150, 4) if overwrite else None, 4.5)

    monkeypatch.setattr(build_datasets, "build_dataset", fake)
    assert cli.main(["build", "iris", "--output-dir", str(tmp_path), "-f"]) == 0
    assert calls == [("iris", tmp_path, True)]
    output = capsys.readouterr().out
    assert "iris" in output
    assert "built" in output
    assert "150 x 4" in output
    assert cli.main(["build", "iris", "--output-dir", str(tmp_path)]) == 0
    assert "use --force" in capsys.readouterr().out


@pytest.mark.parametrize("check", [True, False])
def test_gen_reports_stale_files(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], check: bool
) -> None:
    monkeypatch.setattr(generate, "run", lambda check: [ROOT / "NOTICE.md"])
    code = cli.main(["gen", "--check"] if check else ["gen"])
    captured = capsys.readouterr()
    assert "NOTICE.md" in captured.out
    assert code == (1 if check else 0)
    assert ("out of date" in captured.out) is check
    assert ("python -m scripts gen" in captured.err) is check


def test_gen_is_quiet_when_everything_is_up_to_date(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(generate, "run", lambda check: [])
    assert cli.main(["gen", "--check"]) == 0
    assert "up to date" in capsys.readouterr().out


def test_gen_reports_a_missing_data_file(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def missing(check: bool) -> list[Path]:
        raise FileNotFoundError("data/seeds.npz does not exist.")

    monkeypatch.setattr(generate, "run", missing)
    assert cli.main(["gen"]) == 1
    assert "data/seeds.npz does not exist" in capsys.readouterr().err


def _row(name: str = "iris") -> check_legal.DatasetRow:
    return check_legal.DatasetRow(name, "CC-BY-4.0", "2026-10-17", 31, True, True, False)


def test_legal_fails_on_errors_and_prints_them_to_stderr(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    problems = check_legal.Problems(errors=["iris: the evidence is bad."], warnings=[])
    monkeypatch.setattr(check_legal, "collect_problems", lambda: problems)
    monkeypatch.setattr(check_legal, "summarize", lambda: [_row()])
    assert cli.main(["legal"]) == 1
    captured = capsys.readouterr()
    assert "iris: the evidence is bad." in captured.err
    assert "1 error(s)" in captured.out
    assert "passed" not in captured.out


def test_legal_passes_with_warnings(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    problems = check_legal.Problems(errors=[], warnings=["iris: verified long ago."])
    monkeypatch.setattr(check_legal, "collect_problems", lambda: problems)
    monkeypatch.setattr(check_legal, "summarize", lambda: [_row()])
    assert cli.main(["legal"]) == 0
    captured = capsys.readouterr()
    assert "iris: verified long ago." in captured.out
    assert "1 warning(s)" in captured.out
    assert "Legal check passed." in captured.out


def test_text_from_outside_is_never_taken_for_markup(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    problems = check_legal.Problems(errors=["iris: [bold]odd[/bold] [/nothing]"], warnings=[])
    monkeypatch.setattr(check_legal, "collect_problems", lambda: problems)
    monkeypatch.setattr(check_legal, "summarize", lambda: [_row()])
    assert cli.main(["legal"]) == 1
    assert "[bold]odd[/bold] [/nothing]" in capsys.readouterr().err


def test_there_is_no_color_when_the_output_is_not_a_terminal(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    problems = check_legal.Problems(errors=["iris: bad."], warnings=["iris: old."])
    monkeypatch.setattr(check_legal, "collect_problems", lambda: problems)
    monkeypatch.setattr(check_legal, "summarize", lambda: [_row()])
    cli.main(["legal"])
    captured = capsys.readouterr()
    assert "\x1b" not in captured.out
    assert "\x1b" not in captured.err


def _fake_steps(ran: list[str], monkeypatch: pytest.MonkeyPatch, gen_code: int = 0) -> None:
    """Replace the steps of the commands by functions that only write down that they ran."""

    def legal() -> int:
        ran.append("legal")
        return 0

    def gen(check: bool) -> int:
        ran.append(f"gen {check}")
        return gen_code

    monkeypatch.setattr(cli, "_legal_check", legal)
    monkeypatch.setattr(cli, "_generate", gen)


def test_check_runs_both_checks(monkeypatch: pytest.MonkeyPatch) -> None:
    ran: list[str] = []
    _fake_steps(ran, monkeypatch, gen_code=1)
    assert cli.main(["check"]) == 1
    assert ran == ["legal", "gen True"]


def test_refresh_stops_when_the_build_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: Any, **kwargs: Any) -> int:
        raise AssertionError("must not run after a failed build")

    monkeypatch.setattr(cli, "_generate", forbidden)
    monkeypatch.setattr(cli, "_legal_check", forbidden)
    assert cli.main(["refresh", "no_such_dataset"]) == 2


def test_refresh_builds_then_generates_then_checks(monkeypatch: pytest.MonkeyPatch) -> None:
    ran: list[str] = []

    def build(names: list[str], output_dir: Path, force: bool) -> int:
        ran.append(f"build {names} {force}")
        return 0

    monkeypatch.setattr(cli, "_build_names", build)
    _fake_steps(ran, monkeypatch)
    assert cli.main(["refresh", "iris", "-f"]) == 0
    assert ran == ["build ['iris'] True", "gen False", "legal"]


def test_owner_of_a_message() -> None:
    assert check_legal.owner_of("iris: the evidence is missing.") == "iris"
    assert check_legal.owner_of("pyproject.toml: license expression lacks MIT.") == "pyproject.toml"


def test_the_summary_has_a_row_for_every_dataset() -> None:
    rows = check_legal.summarize(date(2026, 11, 17))
    assert [row.name for row in rows] == list(generate.dataset_names())
    assert all(row.has_evidence and row.has_archive and row.has_maintainer_check for row in rows)


@pytest.mark.parametrize("argv", [["-h"], ["new", "-h"], ["build", "-h"]])
def test_help_is_plain_text_when_it_is_not_a_terminal(
    capsys: pytest.CaptureFixture[str], argv: list[str]
) -> None:
    with pytest.raises(SystemExit) as stop:
        cli.main(argv)
    assert stop.value.code == 0
    output = capsys.readouterr().out
    assert "\x1b" not in output
    assert "python -m scripts" in output


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["list"], ["list", "--sort", "name"]),
        (
            ["list", "--task", "regression", "--sort", "samples", "--reverse"],
            ["list", "--sort", "samples", "--task", "regression", "--reverse"],
        ),
    ],
)
def test_list_passes_its_options_to_the_package_command(
    argv: list[str], expected: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[list[str]] = []

    def package_cli(arguments: list[str]) -> int:
        calls.append(arguments)
        return 0

    monkeypatch.setattr(cli, "package_cli", package_cli)
    assert cli.main(argv) == 0
    assert calls == [expected]


def test_list_rejects_a_wrong_option_like_the_package_command() -> None:
    with pytest.raises(SystemExit) as stop:
        cli.main(["list", "--sort", "size"])
    assert stop.value.code == 2


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["show", "iris"], ["show", "iris"]),
        (["show", "iris", "--full"], ["show", "iris", "--full"]),
    ],
)
def test_show_passes_its_arguments_to_the_package_command(
    argv: list[str], expected: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[list[str]] = []

    def package_cli(arguments: list[str]) -> int:
        calls.append(arguments)
        return 0

    monkeypatch.setattr(cli, "package_cli", package_cli)
    assert cli.main(argv) == 0
    assert calls == [expected]
