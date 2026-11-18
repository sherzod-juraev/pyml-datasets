"""Tests of ``--format``, ``--output`` and ``--force`` of ``pyml-datasets list`` and ``show``."""

import io
import json
import sys
from pathlib import Path
from typing import Any

import pytest

from pyml_datasets import get_info, list_datasets, load_dataset
from pyml_datasets._cli import _commands, _formats, main
from pyml_datasets._cli._output import Destination, OutputError, choose_destination
from tests.conftest import make_info

NAMES = list_datasets()
CREATOR_NAME = "combined_cycle_power_plant"  # a creator has the letter "ı", not in cp1252


@pytest.fixture(autouse=True)
def plain_terminal(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the output the same on every machine."""
    monkeypatch.setenv("COLUMNS", "1000")
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("NO_COLOR", raising=False)


# --- the rules for the format and the file --------------------------------------------------


def test_the_terminal_is_the_default_and_the_format_is_text() -> None:
    assert choose_destination(None, None, False) == Destination("text", None)
    assert choose_destination("md", None, False) == Destination("md", None)
    assert choose_destination(None, "-", False) == Destination("text", None)
    assert choose_destination("json", "-", False) == Destination("json", None)


@pytest.mark.parametrize(
    ("name", "expected"),
    [("a.md", "md"), ("a.MD", "md"), ("a.txt", "text"), ("a.json", "json"), ("a.b.json", "json")],
)
def test_the_extension_chooses_the_format(
    name: str, expected: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    assert choose_destination(None, name, False) == Destination(expected, tmp_path.resolve() / name)


def test_a_known_extension_and_the_same_format_agree(tmp_path: Path) -> None:
    path = tmp_path / "a.json"
    assert choose_destination("json", str(path), False).format == "json"


def test_an_unknown_extension_needs_a_format(tmp_path: Path) -> None:
    path = str(tmp_path / "a.out")
    with pytest.raises(OutputError, match=r"cannot tell the format .* Use \.md, \.txt or \.json"):
        choose_destination(None, path, False)
    assert choose_destination("md", path, False).format == "md"


def test_a_format_that_disagrees_with_the_extension_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(OutputError, match="--format json does not fit the extension of 'a.md'"):
        choose_destination("json", str(tmp_path / "a.md"), False)


def test_a_name_only_means_the_current_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    destination = choose_destination(None, "iris.md", False)
    assert destination.path == tmp_path.resolve() / "iris.md"


def test_a_relative_path_is_taken_from_the_current_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "out").mkdir()
    (tmp_path / "work").mkdir()
    monkeypatch.chdir(tmp_path / "work")
    destination = choose_destination(None, str(Path("..") / "out" / "iris.md"), False)
    assert destination.path == tmp_path.resolve() / "out" / "iris.md"


def test_a_full_path_is_used_as_it_is(tmp_path: Path) -> None:
    destination = choose_destination(None, str(tmp_path / "iris.txt"), False)
    assert destination.path == tmp_path.resolve() / "iris.txt"


def test_the_home_directory_is_expanded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for variable in ("HOME", "USERPROFILE"):
        monkeypatch.setenv(variable, str(tmp_path))
    destination = choose_destination(None, str(Path("~") / "iris.md"), False)
    assert destination.path == tmp_path.resolve() / "iris.md"


def test_a_path_that_cannot_be_read_is_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(self: Path) -> Path:
        raise RuntimeError("no home directory")

    monkeypatch.setattr(Path, "expanduser", fail)
    with pytest.raises(OutputError, match="cannot read the path .*no home directory"):
        choose_destination(None, str(tmp_path / "a.md"), False)


def test_a_missing_directory_is_an_error_and_is_not_created(tmp_path: Path) -> None:
    path = tmp_path / "missing" / "a.md"
    with pytest.raises(OutputError, match="the directory .*missing.* does not exist"):
        choose_destination(None, str(path), False)
    assert not path.parent.exists()


def test_a_directory_is_not_a_file(tmp_path: Path) -> None:
    folder = tmp_path / "a.md"
    folder.mkdir()
    with pytest.raises(OutputError, match="is a directory"):
        choose_destination(None, str(folder), True)


def test_an_existing_file_needs_force(tmp_path: Path) -> None:
    path = tmp_path / "a.md"
    path.write_text("old", encoding="utf-8")
    with pytest.raises(OutputError, match="exists. Use --force to overwrite it"):
        choose_destination(None, str(path), False)
    assert choose_destination(None, str(path), True).path == path.resolve()


@pytest.mark.parametrize("output", [None, "-"])
def test_force_needs_a_file(output: str | None) -> None:
    with pytest.raises(OutputError, match="--force needs --output with a file"):
        choose_destination(None, output, True)


# --- the files ------------------------------------------------------------------------------


def _tree(path: Path) -> list[str]:
    return sorted(item.name for item in path.iterdir())


@pytest.mark.parametrize("command", [["list"], ["show", "iris"], ["show", CREATOR_NAME, "--full"]])
@pytest.mark.parametrize("name", ["out.md", "out.txt", "out.json"])
def test_a_file_is_utf8_with_line_feeds_and_no_byte_order_mark(
    command: list[str], name: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / name
    assert main([*command, "-o", str(path)]) == 0
    data = path.read_bytes()
    assert not data.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in data
    assert data.endswith(b"\n") and not data.endswith(b"\n\n")
    text = data.decode("utf-8")
    assert "\x1b" not in text
    assert all(line == line.rstrip() for line in text.splitlines())
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == f"wrote {path.resolve()}\n"


@pytest.mark.parametrize("name", ["out.md", "out.txt", "out.json"])
def test_a_character_outside_cp1252_is_written_as_it_is(name: str, tmp_path: Path) -> None:
    assert "ı" in "".join(get_info(CREATOR_NAME).creators)
    path = tmp_path / name
    assert main(["show", CREATOR_NAME, "-o", str(path)]) == 0
    text = path.read_bytes().decode("utf-8")
    assert "Pınar" in text
    assert "P?nar" not in text


def test_a_file_does_not_depend_on_the_width_of_the_terminal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    results = []
    for width in ("40", "300"):
        monkeypatch.setenv("COLUMNS", width)
        for command, name in ((["show", "german_credit", "--full"], "s.txt"), (["list"], "l.txt")):
            path = tmp_path / f"{width}-{name}"
            assert main([*command, "-o", str(path)]) == 0
        results.append([(tmp_path / f"{width}-{name}").read_bytes() for name in ("s.txt", "l.txt")])
    assert results[0] == results[1]


def test_a_text_file_has_the_facts_of_the_terminal_without_escape_codes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("FORCE_COLOR", "1")
    path = tmp_path / "iris.txt"
    assert main(["show", "iris", "--full", "-o", str(path)]) == 0
    capsys.readouterr()
    text = path.read_text("utf-8")
    assert "\x1b" not in text
    for fact in ("Iris", "classification", "CC-BY-4.0", "setosa", "Citation", "Changes made"):
        assert fact in text


def test_an_existing_file_is_kept_without_force_and_replaced_with_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "iris.md"
    path.write_text("old", encoding="utf-8")
    assert main(["show", "iris", "-o", str(path)]) == 2
    assert "error: " in capsys.readouterr().err
    assert path.read_text("utf-8") == "old"
    assert main(["show", "iris", "-o", str(path), "--force"]) == 0
    assert path.read_text("utf-8").startswith("# Iris")


def test_nothing_is_written_for_a_dataset_that_does_not_exist(tmp_path: Path) -> None:
    assert main(["show", "nothing", "-o", str(tmp_path / "a.md")]) == 2
    assert _tree(tmp_path) == []


def test_the_options_that_do_not_fit_stop_the_command(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    for argv in (
        ["list", "-o", str(tmp_path / "a.md"), "--format", "json"],
        ["show", "iris", "-o", str(tmp_path / "a.out")],
        ["list", "-o", str(tmp_path / "missing" / "a.md")],
        ["show", "iris", "--force"],
    ):
        assert main(argv) == 2, argv
        assert "error:" in capsys.readouterr().err
    assert _tree(tmp_path) == []


def test_a_file_that_cannot_be_written_is_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(self: Path, *args: Any, **kwargs: Any) -> int:
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "write_text", fail)
    assert main(["list", "-o", str(tmp_path / "a.md")]) == 1
    assert "error: denied" in capsys.readouterr().err


def test_a_wrong_format_is_a_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as stop:
        main(["list", "--format", "xml"])
    assert stop.value.code == 2
    assert "error:" in capsys.readouterr().err


def test_output_is_also_the_terminal_with_a_dash(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["show", "iris", "--format", "json", "-o", "-"]) == 0
    assert json.loads(capsys.readouterr().out)["name"] == "iris"


# --- list ----------------------------------------------------------------------------------


def _json(capsys: pytest.CaptureFixture[str]) -> Any:
    return json.loads(capsys.readouterr().out)


def test_list_json_is_an_array_of_objects(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list", "--format", "json"]) == 0
    data = _json(capsys)
    assert [row["name"] for row in data] == sorted(NAMES)
    for row in data:
        info = get_info(row["name"])
        loaded = load_dataset(row["name"])
        assert row == {
            "name": info.name,
            "task": info.task,
            "license": info.license,
            "samples": loaded.X.shape[0],
            "features": loaded.X.shape[1],
            "has_missing": info.has_missing,
        }


def test_the_default_limit_does_not_cut_json_but_cuts_the_other_formats(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(_commands, "DEFAULT_LIMIT", 5)
    main(["list", "--format", "json"])
    assert len(_json(capsys)) == len(NAMES)
    main(["list", "--format", "md"])
    assert f"Showing 1-5 of {len(NAMES)}." in capsys.readouterr().out
    main(["list", "--format", "json", "--limit", "3", "--offset", "2"])
    assert [row["name"] for row in _json(capsys)] == sorted(NAMES)[2:5]
    main(["list", "--format", "json", "--all", "--no-missing", "--name", "wine*"])
    assert [row["name"] for row in _json(capsys)] == ["wine", "wine_quality"]


@pytest.mark.parametrize("argv", [["--name", "nothing*"], ["--offset", "1000"]])
def test_list_json_is_an_empty_array_when_nothing_is_shown(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["list", "--format", "json", *argv]) == 0
    assert _json(capsys) == []


def test_list_markdown_is_an_aligned_table_with_the_counts(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["list", "--format", "md", "--limit", "3"]) == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("| Dataset ")
    assert lines[1].startswith("|:---") and lines[1].endswith("---:|")
    assert [line.split("|")[1].strip() for line in lines[2:5]] == [
        f"`{name}`" for name in sorted(NAMES)[:3]
    ]
    assert len({len(line) for line in lines[:5]}) == 1
    assert "3 datasets: classification 1, regression 2" in lines
    assert f"Showing 1-3 of {len(NAMES)}. Use --offset or --all to see more." in lines


def test_list_markdown_says_in_a_paragraph_that_nothing_matches(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["list", "--format", "md", "--name", "quality"]) == 0
    output = capsys.readouterr().out
    assert output.startswith("No dataset matches the filters.\n\nTip: ")
    assert r"\*quality\*" in output
    assert output.endswith(".\n")


def test_list_text_in_a_file_says_the_same_as_on_the_terminal(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    main(["list", "--name", "nothing*", "-o", str(tmp_path / "a.txt")])
    assert (tmp_path / "a.txt").read_text("utf-8") == "No dataset matches the filters.\n"
    main(["list", "--name", "wine", "-o", str(tmp_path / "b.txt")])
    text = (tmp_path / "b.txt").read_text("utf-8")
    assert "1 dataset: classification 1" in text and "Tip:" in text


def test_a_cut_list_in_a_markdown_file_names_the_rows(tmp_path: Path) -> None:
    path = tmp_path / "list.md"
    main(["list", "--offset", "2", "--limit", "2", "-o", str(path)])
    assert f"Showing 3-4 of {len(NAMES)}." in path.read_text("utf-8")


def test_a_pipe_character_in_a_cell_is_escaped() -> None:
    table = _formats._table(["a", "b"], [["x|y", "z"]], "lr")
    assert table[2] == "| x\\|y |   z |"


# --- show ----------------------------------------------------------------------------------


@pytest.mark.parametrize("name", NAMES)
def test_show_json_has_every_fact_of_every_dataset(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["show", name, "--format", "json"]) == 0
    output = capsys.readouterr().out
    assert output.isascii() and output.endswith("}\n")
    data = json.loads(output)
    info = get_info(name)
    loaded = load_dataset(name)
    assert {key: data[key] for key in info.to_dict()} == info.to_dict()
    assert data["n_samples"] == loaded.X.shape[0]
    assert data["n_features"] == loaded.X.shape[1]
    assert data["feature_names"] == list(loaded.feature_names)
    assert data["target_names"] == (
        None if loaded.target_names is None else list(loaded.target_names)
    )
    assert data["size_bytes"] > 0
    assert data["changes"] == list(info.changes) and data["notes"] == list(info.notes)


def test_show_json_does_not_depend_on_full(capsys: pytest.CaptureFixture[str]) -> None:
    main(["show", "german_credit", "--format", "json"])
    short = capsys.readouterr().out
    main(["show", "german_credit", "--format", "json", "--full"])
    assert capsys.readouterr().out == short


def test_json_on_a_console_that_is_not_utf8_is_ascii_and_keeps_the_letters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="cp1252", newline="")
    monkeypatch.setattr(sys, "stdout", stream)
    assert main(["show", CREATOR_NAME, "--format", "json"]) == 0
    stream.flush()
    data = json.loads(buffer.getvalue().decode("ascii"))
    assert data["creators"] == list(get_info(CREATOR_NAME).creators)


def test_a_json_file_keeps_the_letters_without_escapes(tmp_path: Path) -> None:
    path = tmp_path / "a.json"
    assert main(["show", CREATOR_NAME, "-o", str(path)]) == 0
    text = path.read_bytes().decode("utf-8")
    assert "Pınar" in text and "\\u" not in text
    assert json.loads(text)["creators"] == list(get_info(CREATOR_NAME).creators)


@pytest.mark.parametrize("name", NAMES)
def test_show_markdown_has_the_sections_and_the_notes_of_every_dataset(
    name: str, capsys: pytest.CaptureFixture[str]
) -> None:
    info = get_info(name)
    assert main(["show", name, "--format", "md", "--full"]) == 0
    text = capsys.readouterr().out
    assert text.startswith(f"# {info.title} (`{info.name}`)\n")
    for heading in ("## Overview", "## Provenance", "## Features", "## Citation"):
        assert heading in text
    assert ("## Notes" in text) is bool(info.notes)
    flat = text.replace("<", "").replace(">", "")
    assert all(f"- {change}".replace("<", "").replace(">", "") in flat for change in info.changes)
    assert all(line == line.rstrip() for line in text.splitlines())
    assert text.endswith("\n") and not text.endswith("\n\n")
    assert ("**DOI:**" in text) is bool(info.doi)


def test_show_markdown_without_full_counts_what_it_leaves_out(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["show", "german_credit", "--format", "md"])
    text = capsys.readouterr().out
    assert "4 changes and 5 notes are not shown. Run with --full to read them." in text
    assert "## Notes" not in text and "## Changes made" not in text


def test_show_markdown_puts_the_addresses_of_the_citation_in_angle_brackets(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["show", "iris", "--format", "md"])
    assert "<https://doi.org/" in capsys.readouterr().out


def test_show_markdown_names_classes_or_targets_and_feature_kinds(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["show", "german_credit", "--format", "md"])
    text = capsys.readouterr().out
    assert "- **Classes:** good, bad" in text
    assert "- **Features:** 20 (13 categorical, 7 numeric)" in text
    assert "- **Numeric (7):**" in text and "- **Categorical (13):**" in text
    main(["show", "abalone", "--format", "md"])
    text = capsys.readouterr().out
    assert "- **Features:** 8 (" in text


def test_show_markdown_of_a_dataset_with_only_categorical_features_and_no_names() -> None:
    info = make_info(doi=None, categorical={"colour": ("red", "blue")})
    text = _formats.show_markdown(
        info, shape=(3, 1), size=2048, feature_names=("colour",), target_names=None, full=True
    )
    assert "**Classes:**" not in text and "**Targets:**" not in text
    assert "**Numeric" not in text and "- **Categorical (1):** colour" in text
    assert "**DOI:**" not in text
    assert "- **Features:** 1 (1 categorical, 0 numeric)" in text
    assert "## Notes" not in text
    with_doi = make_info(doi="10.1234/abc")
    assert "- **DOI:** [10.1234/abc](https://doi.org/10.1234/abc)" in _formats.show_markdown(
        with_doi, shape=(3, 1), size=2048, feature_names=("x",), target_names=("a", "b"), full=False
    )
