"""Create the files for a new dataset, with TODO markers where the facts must be written.

Run it from the repository root::

    python -m scripts.new_dataset my_dataset --license CC-BY-4.0 --task classification

It creates the dataset module, the build recipe, the expected facts for the tests, the
documentation page and the legal evidence file. It never overwrites an existing file. The
files contain ``TODO`` markers that ``python -m scripts.check_legal`` rejects, so a dataset
cannot be finished by accident. The steps that follow are in ``CONTRIBUTING.md``.
"""

import argparse
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from pyml_datasets._types import LICENSE_IDS, TASKS
from scripts import ROOT, utc_today

_NAME: Final = re.compile(r"[a-z][a-z0-9_]*")

_MODULE: Final = '''"""{title}: TODO one line that says what the dataset is."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="{name}",
    title="{title}",
    task="{task}",
    summary="TODO two sentences: what was measured, how many samples, what is predicted.",
    license="{license}",
    license_url="{license_url}",
    source="TODO name of the source, for example UCI Machine Learning Repository",
    source_url="https://example.org/TODO",
    doi=None,
    creators=("TODO",),
    citation="TODO the citation the source asks for, with its DOI if it has one",
    obtained_from="TODO the exact file or function the recipe reads",
    changes=("Converted to the NumPy NPZ format. TODO list every other change.",),
    verified_on="{today}",
)


def load_{name}() -> Dataset:
    """Load the {title} dataset (TODO task, TODO samples, TODO features).

    Returns
    -------
    Dataset
        TODO what the targets are. ``Dataset.info`` holds the license, the source and the
        citation.

    Examples
    --------
    >>> from pyml_datasets import load_{name}
    >>> X, y = load_{name}()
    >>> X.shape, y.shape
    ((0, 0), (0,))
    """
    return load_npz(INFO)
'''

_RECIPE: Final = '''"""Recipe for {title}."""

from scripts.recipes._common import Built
from scripts.recipes._sources import download


def build() -> Built:
    """Build the {title} dataset.

    Returns
    -------
    Built
        TODO shape and targets. Missing values must be ``NaN``, categories integer codes.
    """
    raw = download("https://example.org/TODO", "TODO sha256 of the file")
    raise NotImplementedError(f"TODO: turn {{len(raw)}} bytes into a Built object.")
'''

_EXPECTED: Final = '''"""Facts about {title}, written down independently of the data file."""

from tests.expected import Expected

EXPECTED = Expected(
    shape=(0, 0),  # TODO from the documentation of the source
    n_classes=None,  # TODO number of classes, None for regression
    class_counts=None,  # TODO samples per class if the source states them
    first_row=(),  # TODO the first values of the first sample, as printed in the source
    column_means={{}},  # TODO {{column index: mean}} if the source publishes them
    n_missing=0,  # TODO number of missing values the source reports
)
'''

_PAGE: Final = """{title}
{underline}

TODO a short paragraph for a student: what the data is and what it is good for.

Overview
--------

.. include:: /_generated/{name}_overview.inc

Features
--------

TODO describe the features and their units.

Target
------

TODO describe the target.

.. include:: /_generated/{name}_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_{name}
   >>> data = load_{name}()
   >>> data.X.shape
   (0, 0)
"""

_EVIDENCE: Final = """# Evidence: {title} (`{name}`)

- **License:** {license}
- **License page:** TODO https address of the page that states the license
- **Checked:** {today}
- **Checked by:** TODO who read the page, and how
- **Archive:** pending
- **Maintainer check:** pending

What the page says: TODO quote the exact sentence that gives the license.
"""


def create(name: str, license_id: str, task: str, today: str) -> list[Path]:
    """Write the scaffold files of a new dataset.

    Parameters
    ----------
    name : str
        Dataset name: lowercase letters, digits and underscores, starting with a letter.
    license_id : str
        One of the allowed license identifiers.
    task : str
        ``"classification"`` or ``"regression"``.
    today : str
        Date for ``verified_on`` and the evidence file, ``YYYY-MM-DD`` in UTC.

    Returns
    -------
    list of Path
        The files that were created.

    Raises
    ------
    ValueError
        If the name, the license or the task is not valid.
    FileExistsError
        If a dataset with this name already has one of the files.
    """
    if not _NAME.fullmatch(name):
        raise ValueError(f"{name!r} is not a valid dataset name.")
    if license_id not in LICENSE_IDS:
        raise ValueError(f"License must be one of {LICENSE_IDS}, got {license_id!r}.")
    if task not in TASKS:
        raise ValueError(f"Task must be one of {TASKS}, got {task!r}.")
    title = name.replace("_", " ").title()
    license_url = {
        "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
        "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
    }[license_id]
    values = {
        "name": name,
        "title": title,
        "underline": "=" * len(title),
        "task": task,
        "license": license_id,
        "license_url": license_url,
        "today": today,
    }
    plan = {
        ROOT / "pyml_datasets" / "datasets" / f"{name}.py": _MODULE,
        ROOT / "scripts" / "recipes" / f"{name}.py": _RECIPE,
        ROOT / "tests" / "expected" / f"{name}.py": _EXPECTED,
        ROOT / "docs" / "source" / "datasets" / f"{name}.rst": _PAGE,
        ROOT / "legal" / "evidence" / f"{name}.md": _EVIDENCE,
    }
    existing = [path for path in plan if path.exists()]
    if existing:
        raise FileExistsError(f"Refusing to overwrite: {', '.join(map(str, existing))}")
    for path, template in plan.items():
        path.write_text(template.format(**values), "utf-8")
    return list(plan)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line interface.

    Parameters
    ----------
    argv : sequence of str, optional
        Command line arguments, ``sys.argv[1:]`` if not given.

    Returns
    -------
    int
        Exit code, 0 on success.
    """
    parser = argparse.ArgumentParser(description="Scaffold a new dataset.")
    parser.add_argument("name", help="dataset name, for example 'seeds'")
    parser.add_argument("--license", required=True, choices=LICENSE_IDS, dest="license_id")
    parser.add_argument("--task", required=True, choices=TASKS)
    args = parser.parse_args(argv)

    created = create(args.name, args.license_id, args.task, utc_today().isoformat())
    for path in created:
        print(f"created {path.relative_to(ROOT)}")
    print("Now search for TODO, fill the files in, then see CONTRIBUTING.md, 'Adding a dataset'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
