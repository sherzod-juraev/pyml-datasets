"""Tests of the ``pyml-datasets`` command line of the package."""

import argparse
import importlib
import io
import runpy
import subprocess
import sys
import zipfile
from importlib.resources import files
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from rich.console import Console

from pyml_datasets import DatasetInfo, get_info, list_datasets, load_dataset
from pyml_datasets._cli import _commands, _facts, _render, main
from pyml_datasets._cli._parser import build_parser

NAMES = list_datasets()


@pytest.fixture(autouse=True)
def wide_terminal(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make lines so long that rich never wraps a value in the captured output."""
    monkeypatch.setenv("COLUMNS", "1000")
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)


def _words(text: str) -> str:
    return " ".join(text.split())


def test_list_prints_every_dataset_and_the_totals(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list"]) == 0
    output = capsys.readouterr().out
    for name in NAMES:
        assert name in output
    classification = len(list_datasets("classification"))
    regression = len(list_datasets("regression"))
    expected = f"{len(NAMES)} datasets: classification {classification}, regression {regression}"
    assert expected in output


def _listed(capsys: pytest.CaptureFixture[str]) -> list[str]:
    """Return the dataset names of the ``list`` table in the order they are printed."""
    lines = capsys.readouterr().out.splitlines()
    return [line.split()[0] for line in lines if line.split()[:1] and line.split()[0] in NAMES]


def _shape(name: str) -> tuple[int, int]:
    n_samples, n_features = load_dataset(name).X.shape
    return n_samples, n_features


@pytest.mark.parametrize("task", ["classification", "regression"])
def test_list_task_shows_only_the_datasets_of_that_task(
    task: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["list", "--task", task]) == 0
    shown = _listed(capsys)
    assert set(shown) == set(list_datasets(task))  # type: ignore[arg-type]
    assert set(shown) < set(NAMES)


@pytest.mark.parametrize("task", ["classification", "regression"])
def test_the_footer_counts_only_the_shown_datasets(
    task: str, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["list", "--task", task])
    output = capsys.readouterr().out
    count = len(list_datasets(task))  # type: ignore[arg-type]
    assert f"{count} datasets: {task} {count}" in output
    other = "regression" if task == "classification" else "classification"
    assert other not in output


def test_the_default_order_is_by_name(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list"])
    assert _listed(capsys) == sorted(NAMES)


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("name", lambda name: name),
        ("samples", lambda n: _shape(n)[0]),
        ("features", lambda n: _shape(n)[1]),
    ],
)
def test_list_sort_orders_the_rows(
    key: str, value: Any, reverse: bool, capsys: pytest.CaptureFixture[str]
) -> None:
    argv = ["list", "--sort", key] + (["--reverse"] if reverse else [])
    assert main(argv) == 0
    shown = _listed(capsys)
    assert sorted(shown) == sorted(NAMES)
    values = [value(name) for name in shown]
    assert values == sorted(values, reverse=reverse)


@pytest.mark.parametrize("reverse", [False, True])
def test_equal_values_stay_in_the_order_of_their_names(
    reverse: bool, capsys: pytest.CaptureFixture[str]
) -> None:
    features = [_shape(name)[1] for name in NAMES]
    assert len(set(features)) < len(features), "the test needs two datasets with equal values"
    main(["list", "--sort", "features"] + (["--reverse"] if reverse else []))
    shown = _listed(capsys)
    for count in set(features):
        group = [name for name in shown if _shape(name)[1] == count]
        assert group == sorted(group)


def test_reverse_alone_reverses_the_names(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list", "--reverse"])
    assert _listed(capsys) == sorted(NAMES, reverse=True)


def test_task_sort_and_reverse_work_together(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list", "--task", "regression", "--sort", "samples", "--reverse"])
    shown = _listed(capsys)
    sizes = [_shape(name)[0] for name in shown]
    assert sizes == sorted(sizes, reverse=True)
    assert set(shown) == set(list_datasets("regression"))


@pytest.mark.parametrize(
    "argv", [["list", "--task", "clustering"], ["list", "--sort", "size"], ["list", "--sort"]]
)
def test_list_rejects_a_wrong_option(argv: list[str], capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as stop:
        main(argv)
    assert stop.value.code == 2
    assert "error:" in capsys.readouterr().err


def test_list_columns_are_aligned_as_designed() -> None:
    table = _render.list_table([], {})
    justify = {str(column.header): column.justify for column in table.columns}
    assert justify == {
        "Dataset": "left",
        "Task": "center",
        "License": "center",
        "Samples": "right",
        "Features": "right",
    }


def test_sort_rows_does_not_change_its_argument() -> None:
    rows = [
        _render.ListRow("b", "regression", "CC0-1.0", 5, 2),
        _render.ListRow("a", "regression", "CC0-1.0", 5, 3),
    ]
    ordered = _commands.sort_rows(rows, "samples", reverse=True)
    assert [row.name for row in ordered] == ["a", "b"]
    assert [row.name for row in rows] == ["b", "a"]


@pytest.mark.parametrize("name", NAMES)
def test_the_shape_is_read_from_the_header(name: str) -> None:
    data = load_dataset(name)
    assert _facts.read_shape(name) == data.X.shape


@pytest.mark.parametrize("name", NAMES)
def test_the_size_is_the_size_of_the_file(name: str) -> None:
    path = files("pyml_datasets") / "data" / f"{name}.npz"
    assert _facts.read_size(name) == len(path.read_bytes())


def test_list_has_the_shape_of_every_dataset(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list"])
    lines = capsys.readouterr().out.splitlines()
    for name in NAMES:
        (line,) = [line for line in lines if line.split()[:1] == [name]]
        n_samples, n_features = load_dataset(name).X.shape
        assert line.split()[-2:] == [str(n_samples), str(n_features)]


@pytest.mark.parametrize("name", NAMES)
def test_show_has_the_attribution_of_every_dataset(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["show", name, "--full"]) == 0
    output = _words(capsys.readouterr().out)
    info = get_info(name)
    for fact in (info.title, info.license, info.license_url, info.source_url, info.verified_on):
        assert fact in output
    for line in info.citation.split():
        assert line in output
    for change in info.changes:
        assert change.split()[0] in output
    for note in info.notes:
        assert note.split()[0] in output


def test_show_names_the_classes_or_the_targets(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "iris"])
    assert "Classes" in capsys.readouterr().out
    main(["show", "abalone"])
    output = capsys.readouterr().out
    assert "Classes" not in output
    assert "Targets" in output
    assert "Samples" in output


def test_show_marks_missing_values(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "adult"])
    assert "yes, stored as NaN" in capsys.readouterr().out
    main(["show", "iris"])
    assert "yes, stored as NaN" not in capsys.readouterr().out


def test_an_unknown_dataset_is_an_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["show", "no_such_dataset"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Unknown dataset 'no_such_dataset'" in captured.err
    assert "iris" in captured.err


def test_a_missing_data_file_is_an_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def missing(name: str) -> Any:
        raise FileNotFoundError(f"Dataset file '{name}.npz' is missing from the package.")

    monkeypatch.setattr(_facts, "read_shape", missing)
    assert main(["list"]) == 1
    assert "is missing from the package" in capsys.readouterr().err

    monkeypatch.setattr(_commands, "load_dataset", missing)
    assert main(["show", "iris"]) == 1
    assert "iris.npz" in capsys.readouterr().err


def test_a_command_is_required() -> None:
    with pytest.raises(SystemExit) as stop:
        main([])
    assert stop.value.code == 2


@pytest.mark.parametrize("argv", [["-h"], ["list", "-h"], ["show", "-h"]])
def test_help_is_plain_text_when_it_is_not_a_terminal(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as stop:
        main(argv)
    assert stop.value.code == 0
    output = capsys.readouterr().out
    assert "pyml-datasets" in output
    assert "\x1b" not in output


def test_the_output_has_no_color_when_it_is_not_a_terminal(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["list"])
    main(["show", "iris"])
    captured = capsys.readouterr()
    assert "\x1b" not in captured.out


def test_the_output_is_colored_when_the_color_is_forced(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("FORCE_COLOR", "1")
    main(["list"])
    assert "\x1b[" in capsys.readouterr().out


def test_no_color_is_respected(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.setenv("NO_COLOR", "1")
    main(["show", "iris"])
    output = capsys.readouterr().out
    assert "\x1b[3" not in output
    assert "\x1b[1;3" not in output


def test_text_of_a_dataset_is_never_taken_for_markup() -> None:
    odd = "[bold]odd[/bold] [/nothing] [red]"
    info = DatasetInfo(
        name="odd",
        title=f"Odd {odd}",
        task="classification",
        summary=odd,
        license="CC0-1.0",
        license_url="https://example.org/license",
        source=odd,
        source_url="https://example.org/data",
        doi=None,
        creators=(odd,),
        citation=odd,
        obtained_from=odd,
        changes=(odd,),
        verified_on="2026-11-17",
        notes=(odd,),
    )
    report = _render.show_report(
        info, shape=(2, 1), size=2048, feature_names=(odd,), target_names=(odd, "b"), full=True
    )
    console = Console(width=200, record=True, file=io.StringIO(), highlight=False)
    console.print(report)
    assert console.export_text().count(odd) >= 6


def test_no_name_of_a_feature_is_cut(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "superconductivity"])
    output = capsys.readouterr().out
    assert "more)" not in output
    for name in load_dataset("superconductivity").feature_names:
        assert name in output


def test_sizes_are_shown_in_kib_and_mib() -> None:
    assert _render.size_text(2048) == "2.0 KiB"
    assert _render.size_text(3 * 1024 * 1024) == "3.0 MiB"


def test_the_parser_stores_the_handler() -> None:
    args = build_parser().parse_args(["show", "iris"])
    assert isinstance(args, argparse.Namespace)
    assert args.name == "iris"
    assert args.handler is _commands.show_command


@pytest.mark.parametrize("argv", [["list"], ["show", "iris"], ["show", "german_credit", "--full"]])
def test_the_output_survives_a_console_that_is_not_utf8(
    argv: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    # A pipe on Windows uses cp1252, which has no box drawing characters.
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="cp1252", newline="")
    monkeypatch.setattr(sys, "stdout", stream)
    assert main(argv) == 0
    stream.flush()
    text = buffer.getvalue().decode("cp1252")
    assert "\u2500" not in text
    assert "-" * 10 in text


@pytest.mark.parametrize("name", NAMES)
def test_every_dataset_can_be_shown_on_a_console_that_is_not_utf8(
    name: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="cp1252", newline="")
    monkeypatch.setattr(sys, "stdout", stream)
    assert main(["show", name, "--full"]) == 0
    stream.flush()
    assert get_info(name).title.encode("cp1252", errors="replace").decode("cp1252") in (
        buffer.getvalue().decode("cp1252")
    )


def test_a_character_that_the_output_cannot_encode_becomes_a_question_mark(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="cp1252", newline="")
    monkeypatch.setattr(sys, "stdout", stream)
    assert main(["show", "combined_cycle_power_plant"]) == 0
    stream.flush()
    assert "P?nar T" in buffer.getvalue().decode("cp1252")


def test_a_stream_that_cannot_be_reconfigured_is_left_alone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Plain(io.StringIO):
        reconfigure = None

    monkeypatch.setattr(sys, "stderr", Plain())
    assert main(["list"]) == 0


def test_the_package_runs_as_a_module() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pyml_datasets", "show", "iris"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Iris" in result.stdout


def test_importing_the_package_does_not_load_rich() -> None:
    code = "import sys, pyml_datasets; assert 'rich' not in sys.modules, 'rich was imported'"
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr


def test_a_dataset_without_class_names_has_no_classes_line() -> None:
    info = DatasetInfo(
        name="plain",
        title="Plain",
        task="regression",
        summary="A summary.",
        license="CC-BY-4.0",
        license_url="https://example.org/license",
        source="Source",
        source_url="https://example.org/data",
        doi="10.1234/abc",
        creators=("Someone",),
        citation="Someone (2026). Plain.",
        obtained_from="Source",
        changes=("Converted.",),
        verified_on="2026-11-17",
        categorical={"colour": ("red", "blue")},
    )
    report = _render.show_report(
        info, shape=(3, 2), size=100, feature_names=("x", "colour"), target_names=None
    )
    console = Console(width=100, record=True, file=io.StringIO(), highlight=False)
    console.print(report)
    text = console.export_text()
    assert "Classes" not in text
    assert "Targets" not in text
    assert "Numeric (1)" in text
    assert "Categorical (1)" in text
    assert "2 (1 categorical, 1 numeric)" in text
    assert "10.1234/abc" in text


@pytest.mark.parametrize("name", NAMES)
def test_show_has_every_section_and_leaves_the_long_parts_out(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["show", name]) == 0
    output = capsys.readouterr().out
    for heading in ("Overview", "Provenance", "Features", "Citation"):
        assert heading in output
    assert "Changes made to the data" not in output
    assert "\nNotes " not in output
    assert "Run with --full" in output


@pytest.mark.parametrize("name", NAMES)
def test_show_full_adds_the_changes_and_the_notes(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["show", name, "--full"]) == 0
    output = capsys.readouterr().out
    assert "Changes made to the data" in output
    assert ("\nNotes " in output) == bool(get_info(name).notes)
    assert "Run with --full" not in output


def test_the_line_after_the_report_counts_what_is_left_out(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["show", "german_credit"])
    output = _words(capsys.readouterr().out)
    info = get_info("german_credit")
    expected = f"{len(info.changes)} changes and {len(info.notes)} notes are not shown."
    assert expected in output
    assert "Run with --full to read them." in output


def test_the_count_line_has_no_notes_when_there_are_none(
    capsys: pytest.CaptureFixture[str],
) -> None:
    (name,) = [name for name in NAMES if not get_info(name).notes][:1]
    main(["show", name])
    output = _words(capsys.readouterr().out)
    assert "note" not in output.split("Citation")[-1]
    assert "not shown" in output


def test_the_count_line_uses_the_singular() -> None:
    info = DatasetInfo(
        name="one",
        title="One",
        task="regression",
        summary="A summary.",
        license="CC0-1.0",
        license_url="https://example.org/license",
        source="Source",
        source_url="https://example.org/data",
        doi=None,
        creators=("Someone",),
        citation="Someone (2026). One.",
        obtained_from="Source",
        changes=("Converted.",),
        verified_on="2026-11-17",
    )
    text = _render._hidden_parts(info).plain
    assert text == "1 change is not shown. Run with --full to read it."


@pytest.mark.parametrize("name", NAMES)
def test_the_kinds_of_the_features_add_up(name: str, capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", name])
    output = _words(capsys.readouterr().out)
    data = load_dataset(name)
    categorical = len(data.categorical_features)
    n_features = data.X.shape[1]
    if categorical:
        assert (
            f"{n_features} ({categorical} categorical, {n_features - categorical} numeric)"
            in output
        )
        assert f"Categorical ({categorical})" in output
    else:
        assert f"{n_features} (all numeric)" in output
        assert "Categorical" not in output


def test_the_header_has_the_title_the_task_and_the_license(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["show", "german_credit"])
    first = capsys.readouterr().out.splitlines()[0]
    assert "German Credit" in first
    assert "classification" in first
    assert "CC-BY-4.0" in first


def test_the_name_is_not_repeated_as_a_fact(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "iris"])
    assert "german_credit" not in capsys.readouterr().out
    main(["show", "german_credit"])
    lines = capsys.readouterr().out.splitlines()
    assert not [line for line in lines if line.strip().startswith("Name ")]


def test_the_links_are_drawn_when_the_terminal_supports_them() -> None:
    # The console is built here and not by the command: a Windows console without escape
    # codes draws no links, so going through the command would depend on the platform.
    info = get_info("iris")
    data = load_dataset("iris")
    report = _render.show_report(
        info,
        shape=(data.X.shape[0], data.X.shape[1]),
        size=1,
        feature_names=data.feature_names,
        target_names=data.target_names,
    )
    console = Console(
        file=io.StringIO(),
        force_terminal=True,
        color_system="standard",
        legacy_windows=False,
        width=200,
        highlight=False,
    )
    console.print(report)
    output = console.file.getvalue()  # type: ignore[attr-defined]
    assert "\x1b]8;" in output
    assert info.source_url in output
    assert f"https://doi.org/{info.doi}" in output


def test_the_urls_are_plain_text_when_it_is_not_a_terminal(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["show", "iris"])
    output = capsys.readouterr().out
    info = get_info("iris")
    assert "\x1b" not in output
    assert info.source_url in output
    assert info.license_url in output


def test_the_parser_reads_full() -> None:
    assert build_parser().parse_args(["show", "iris"]).full is False
    assert build_parser().parse_args(["show", "iris", "--full"]).full is True


def test_a_missing_file_is_reported(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(_facts, "files", lambda package: tmp_path)
    with pytest.raises(FileNotFoundError, match="missing from the package"):
        _facts.read_shape("iris")


def test_x_must_be_a_matrix(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / "data").mkdir()
    np.savez(tmp_path / "data" / "vector.npz", X=np.zeros(3))
    monkeypatch.setattr(_facts, "files", lambda package: tmp_path)
    with pytest.raises(ValueError, match="expected a matrix"):
        _facts.read_shape("vector")


def test_an_array_format_that_is_not_read_is_reported(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    buffer = io.BytesIO()
    np.lib.format.write_array(buffer, np.zeros((2, 2)), version=(3, 0))
    (tmp_path / "data").mkdir()
    with zipfile.ZipFile(tmp_path / "data" / "odd.npz", "w") as archive:
        archive.writestr("X.npy", buffer.getvalue())
    monkeypatch.setattr(_facts, "files", lambda package: tmp_path)
    with pytest.raises(ValueError, match="unsupported array format"):
        _facts.read_shape("odd")


def test_the_main_module_exits_with_the_code_of_the_command(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["pyml-datasets", "show", "iris"])
    with pytest.raises(SystemExit) as stop:
        runpy.run_module("pyml_datasets", run_name="__main__")
    assert stop.value.code == 0
    assert "Iris" in capsys.readouterr().out


def test_importing_the_main_module_runs_nothing() -> None:
    assert importlib.import_module("pyml_datasets.__main__").main is main


def test_the_second_array_format_is_read(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    buffer = io.BytesIO()
    np.lib.format.write_array(buffer, np.zeros((5, 3)), version=(2, 0))
    (tmp_path / "data").mkdir()
    with zipfile.ZipFile(tmp_path / "data" / "second.npz", "w") as archive:
        archive.writestr("X.npy", buffer.getvalue())
    monkeypatch.setattr(_facts, "files", lambda package: tmp_path)
    assert _facts.read_shape("second") == (5, 3)
