"""Tests of NOTICE.md: it is wrapped at the line length of the repository and loses no word."""

import re

import pytest

from pyml_datasets import get_info, list_datasets
from scripts._render import _wrap_markdown, render_notice

_LIMIT = 100
_ANGLE_ADDRESS = re.compile(r"<(https?://[^<>\s]+)>")
_BLOCK_START = re.compile(r"^\s*(?:[-+*>]|#+|\d+[.)])(?:\s|$)")


@pytest.fixture(scope="module")
def notice() -> str:
    return render_notice([get_info(name) for name in list_datasets()])


def _words(text: str) -> str:
    """Return the text on one line, without the angle brackets around addresses."""
    return " ".join(_ANGLE_ADDRESS.sub(r"\1", text).split())


def test_no_line_is_longer_than_the_limit(notice: str) -> None:
    assert [line for line in notice.splitlines() if len(line) > _LIMIT] == []


def test_wrapping_loses_no_word(notice: str) -> None:
    text = _words(notice)
    for name in list_datasets():
        info = get_info(name)
        for fact in (info.obtained_from, info.citation, *info.changes, *info.notes):
            assert _words(fact) in text, (name, fact)


def test_no_wrapped_line_starts_a_new_block(notice: str) -> None:
    """The bullets are the ones of the datasets, so no wrapped line was read as a new one."""
    infos = [get_info(name) for name in list_datasets()]
    nested = sum(len(info.changes) + len(info.notes) for info in infos)
    assert len(re.findall(r"^  - ", notice, flags=re.MULTILINE)) == nested
    assert len(re.findall(r"^- \*\*", notice, flags=re.MULTILINE)) == sum(
        6 + bool(info.notes) for info in infos
    )
    assert [
        line for line in notice.splitlines() if re.match(r"^\s*(?:\d+[.)]|[+*>])\s", line)
    ] == []


def test_wrap_markdown_keeps_a_marker_word_with_the_word_before_it() -> None:
    text = "alpha " * 15 + "- beta " + "gamma " * 3 + "1. delta"
    wrapped = _wrap_markdown(text, first="- ", rest="  ")
    assert all(len(line) <= _LIMIT for line in wrapped.splitlines())
    assert [line for line in wrapped.splitlines()[1:] if _BLOCK_START.match(line)] == []
    assert " ".join(wrapped.split())[2:] == text.strip()


def test_wrap_markdown_puts_a_bare_address_in_angle_brackets() -> None:
    wrapped = _wrap_markdown("See https://doi.org/10.1/x, and [a](https://b.org/c).")
    assert wrapped == "See <https://doi.org/10.1/x>, and [a](https://b.org/c)."
