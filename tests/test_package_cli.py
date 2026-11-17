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
    assert main(["show", name]) == 0
    output = _words(capsys.readouterr().out)
    info = get_info(name)
    for fact in (info.title, info.license, info.license_url, info.source_url, info.verified_on):
        assert fact in output
    # The panel draws a border at the edge of every line, so compare piece by piece.
    for line in info.citation.split():
        assert line in output
    for change in info.changes:
        assert change.split()[0] in output


def test_show_names_the_classes_or_the_targets(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "iris"])
    assert "Classes" in capsys.readouterr().out
    main(["show", "abalone"])
    output = capsys.readouterr().out
    assert "Classes" not in output
    assert "Shape" in output


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
    panel = _render.show_panel(
        info, shape=(2, 1), size=2048, feature_names=(odd,), target_names=(odd, "b")
    )
    console = Console(width=200, record=True, file=io.StringIO(), highlight=False)
    console.print(panel)
    assert console.export_text().count(odd) >= 6


def test_long_lists_of_names_are_shortened(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "superconductivity"])
    output = capsys.readouterr().out
    assert "(71 more)" in output


def test_sizes_are_shown_in_kib_and_mib() -> None:
    assert _render._size(2048) == "2.0 KiB"
    assert _render._size(3 * 1024 * 1024) == "3.0 MiB"


def test_the_parser_stores_the_handler() -> None:
    args = build_parser().parse_args(["show", "iris"])
    assert isinstance(args, argparse.Namespace)
    assert args.name == "iris"
    assert args.handler is _commands.show_command


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
    panel = _render.show_panel(
        info, shape=(3, 1), size=100, feature_names=("x",), target_names=None
    )
    console = Console(width=100, record=True, file=io.StringIO(), highlight=False)
    console.print(panel)
    text = console.export_text()
    assert "Classes" not in text
    assert "Targets" not in text
    assert "colour" in text
    assert "10.1234/abc" in text


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
