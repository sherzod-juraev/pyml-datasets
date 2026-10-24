"""Check that every bundled dataset is legally admissible and documented.

Run it from the repository root, locally and in CI::

    python -m scripts.check_legal

Errors make the command fail. A dataset is complete only when its evidence file has an
archived copy of the license page and the confirmation of the maintainer, so a missing or
malformed ``Archive`` or ``Maintainer check`` is an error. Warnings are printed but do not
fail the command: they are reminders, such as a license that was verified long ago.

The rules are the admission policy of ``CONTRIBUTING.md``: only the licenses in
``pyml_datasets._types.LICENSE_IDS`` are accepted, the license text must be in ``LICENSES/``,
and each dataset needs an evidence file in ``legal/evidence/`` that states the same license.
"""

import json
import re
import sys
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Final
from urllib.parse import unquote, urlsplit

from pyml_datasets import DatasetInfo
from pyml_datasets._types import LICENSE_IDS
from scripts import ROOT, utc_today
from scripts.generate import DATA_DIR, dataset_names

EVIDENCE_DIR: Final = ROOT / "legal" / "evidence"
LICENSES_DIR: Final = ROOT / "LICENSES"
DOCS_DIR: Final = ROOT / "docs" / "source" / "datasets"
REQUIRED_FIELDS: Final = ("License", "License page", "Checked")
MAX_AGE_DAYS: Final = 365
_FIELD: Final = re.compile(r"^- \*\*(?P<key>[^:*]+):\*\*[ \t]*(?P<value>.*)$", re.MULTILINE)
_PENDING: Final = ("", "none", "pending")
_ARCHIVE: Final = re.compile(
    r"https://web\.archive\.org/web/\d{14}[a-z_]*/(?P<original>https?://\S+)"
)
_ISO_DATE: Final = re.compile(r"\d{4}-\d{2}-\d{2}")


@dataclass
class Problems:
    """Errors and warnings found by the legal check.

    Attributes
    ----------
    errors : list of str
        Problems that must be fixed. The check fails if there is any.
    warnings : list of str
        Reminders. They do not fail the check.
    """

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def read_evidence(path: Path) -> dict[str, str]:
    """Read the fields of an evidence file.

    Parameters
    ----------
    path : Path
        Markdown file with lines like ``- **License:** CC0-1.0``.

    Returns
    -------
    dict of str to str
        Field name and value.
    """
    return {
        match["key"].strip(): match["value"].strip()
        for match in _FIELD.finditer(path.read_text("utf-8"))
    }


def license_expression_ids(expression: str) -> set[str]:
    """Split an SPDX expression such as ``MIT AND CC0-1.0`` into license identifiers.

    Parameters
    ----------
    expression : str
        SPDX license expression.

    Returns
    -------
    set of str
        The identifiers, without operators and parentheses.
    """
    tokens = re.split(r"[\s()]+", expression)
    return {token for token in tokens if token and token not in {"AND", "OR", "WITH"}}


def _page_key(url: str) -> tuple[str, str, str]:
    """Reduce an address to the parts that decide which page it is.

    Parameters
    ----------
    url : str
        An ``http`` or ``https`` address.

    Returns
    -------
    tuple of str
        Host without ``www.``, decoded path without a trailing slash, and query. The scheme
        and the fragment are ignored, so ``bank+marketing`` and ``bank%2Bmarketing`` match.
    """
    parts = urlsplit(url)
    host = parts.netloc.lower().removeprefix("www.")
    return host, unquote(parts.path).rstrip("/"), unquote(parts.query)


def check_archive(name: str, fields: Mapping[str, str], problems: Problems) -> None:
    """Check that the evidence links an archived copy of the license page.

    Parameters
    ----------
    name : str
        Dataset name.
    fields : mapping of str to str
        Fields of the evidence file.
    problems : Problems
        Collection that receives the errors.
    """
    value = fields.get("Archive", "")
    if value.lower() in _PENDING:
        problems.errors.append(f"{name}: no archived copy of the license page (Archive).")
        return
    match = _ARCHIVE.fullmatch(value)
    if match is None:
        problems.errors.append(
            f"{name}: Archive must be a link like "
            "https://web.archive.org/web/<14 digit timestamp>/<address of the license page>."
        )
        return
    page = fields.get("License page", "")
    if _page_key(match["original"]) != _page_key(page):
        problems.errors.append(
            f"{name}: Archive is a copy of {match['original']}, not of the license page {page}."
        )


def check_maintainer(name: str, fields: Mapping[str, str], problems: Problems, today: date) -> None:
    """Check that the maintainer has confirmed the license, with a name and a date.

    Parameters
    ----------
    name : str
        Dataset name.
    fields : mapping of str to str
        Fields of the evidence file.
    problems : Problems
        Collection that receives the errors.
    today : date
        Current date in UTC. A confirmation cannot be dated in the future.
    """
    value = fields.get("Maintainer check", "")
    if value.lower().startswith("pending") or not value:
        problems.errors.append(
            f"{name}: the maintainer has not confirmed the license yet (Maintainer check)."
        )
        return
    found = _ISO_DATE.search(value)
    who = value[: found.start()] if found else value
    try:
        confirmed = date.fromisoformat(found[0]) if found else None
    except ValueError:
        confirmed = None
    if confirmed is None or not any(char.isalpha() for char in who):
        problems.errors.append(
            f"{name}: Maintainer check must give a name and a date, "
            "for example 'Sherzod, 2026-10-20'."
        )
    elif confirmed > today:
        problems.errors.append(
            f"{name}: the date of the Maintainer check is in the future. Write dates in UTC."
        )


def check_info(info: DatasetInfo, problems: Problems, today: date) -> None:
    """Check the license, the citation and the evidence of one dataset.

    Parameters
    ----------
    info : DatasetInfo
        Provenance of the dataset.
    problems : Problems
        Collection that receives the errors and warnings.
    today : date
        Current date in UTC, used to find old verifications.
    """
    name = info.name
    if info.license not in LICENSE_IDS:
        problems.errors.append(f"{name}: license {info.license!r} is not allowed.")
    elif not (LICENSES_DIR / f"{info.license}.txt").exists():
        problems.errors.append(f"{name}: LICENSES/{info.license}.txt is missing.")
    if info.doi and info.doi not in info.citation:
        problems.errors.append(f"{name}: the DOI {info.doi} is not in the citation.")
    if "TODO" in json.dumps(info.to_dict()):
        problems.errors.append(f"{name}: the information still contains a TODO.")
    age = (today - date.fromisoformat(info.verified_on)).days
    if age > MAX_AGE_DAYS:
        problems.warnings.append(f"{name}: license verified {age} days ago, check it again.")

    path = EVIDENCE_DIR / f"{name}.md"
    if not path.exists():
        problems.errors.append(f"{name}: evidence file legal/evidence/{name}.md is missing.")
        return
    fields = read_evidence(path)
    for key in REQUIRED_FIELDS:
        if not fields.get(key):
            problems.errors.append(f"{name}: evidence has no '{key}' field.")
    if "TODO" in path.read_text("utf-8"):
        problems.errors.append(f"{name}: the evidence file still contains a TODO.")
    if fields.get("License") and fields["License"] != info.license:
        problems.errors.append(
            f"{name}: evidence says {fields['License']!r} but the dataset says {info.license!r}."
        )
    if fields.get("Checked") and fields["Checked"] != info.verified_on:
        problems.errors.append(f"{name}: evidence date differs from verified_on.")
    check_archive(name, fields, problems)
    check_maintainer(name, fields, problems, today)


def check_pyproject(infos: Sequence[DatasetInfo], problems: Problems) -> None:
    """Check that ``pyproject.toml`` declares the licenses of the bundled data.

    Parameters
    ----------
    infos : sequence of DatasetInfo
        Information of every bundled dataset.
    problems : Problems
        Collection that receives the errors.
    """
    project = tomllib.loads((ROOT / "pyproject.toml").read_text("utf-8"))["project"]
    declared = license_expression_ids(str(project.get("license", "")))
    needed = {"MIT"} | {info.license for info in infos}
    for missing in sorted(needed - declared):
        problems.errors.append(f"pyproject.toml: license expression lacks {missing}.")
    for extra in sorted(declared - needed):
        problems.errors.append(f"pyproject.toml: license expression lists unused {extra}.")
    files = project.get("license-files", [])
    for required in ("LICENSE", "LICENSES/*", "NOTICE.md"):
        if required not in files:
            problems.errors.append(f"pyproject.toml: license-files lacks {required}.")


def check_files(names: Sequence[str], problems: Problems) -> None:
    """Check that data files, dataset modules and evidence files match one to one.

    Parameters
    ----------
    names : sequence of str
        Names of the dataset modules.
    problems : Problems
        Collection that receives the errors.
    """
    data = {path.stem for path in DATA_DIR.glob("*.npz")}
    evidence = {path.stem for path in EVIDENCE_DIR.glob("*.md") if path.stem != "TEMPLATE"}
    known = set(names)
    for name in sorted(data - known):
        problems.errors.append(f"{name}: data file without a dataset module (no license info).")
    for name in sorted(known - data):
        problems.errors.append(f"{name}: dataset module without a data file.")
    for name in sorted(evidence - known):
        problems.errors.append(f"{name}: evidence file without a dataset.")
    for name in sorted(known):
        page = DOCS_DIR / f"{name}.rst"
        if not page.exists():
            problems.errors.append(f"{name}: documentation page {page.name} is missing.")
        elif "TODO" in page.read_text("utf-8"):
            problems.errors.append(f"{name}: the documentation page still contains a TODO.")


def collect_problems(today: date | None = None) -> Problems:
    """Run all legal checks.

    Parameters
    ----------
    today : date, optional
        Current date, today's date in UTC if not given.

    Returns
    -------
    Problems
        The errors and warnings of the whole repository.
    """
    from pyml_datasets import get_info

    problems = Problems()
    names = dataset_names()
    check_files(names, problems)
    infos = [get_info(name) for name in names]
    for info in infos:
        check_info(info, problems, today or utc_today())
    check_pyproject(infos, problems)
    return problems


def main() -> int:
    """Run the command line interface.

    Returns
    -------
    int
        1 if there are errors, 0 otherwise.
    """
    problems = collect_problems()
    for warning in problems.warnings:
        print(f"warning: {warning}")
    for error in problems.errors:
        print(f"error: {error}", file=sys.stderr)
    if problems.errors:
        print(f"{len(problems.errors)} legal problem(s).", file=sys.stderr)
        return 1
    print("Legal check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
