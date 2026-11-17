"""Generate every file that is derived from the dataset information.

Run it from the repository root after adding or changing a dataset::

    python -m scripts gen           # write the files
    python -m scripts gen --check   # only report files that are out of date

The generated files are ``pyml_datasets/datasets/__init__.py``, the blocks between the
``<generated:...>`` markers of ``pyml_datasets/__init__.py``, ``NOTICE.md``, the table
between the markers of ``README.md``, ``pyml_datasets/data/MANIFEST.json`` and the
``docs/source/_generated`` includes. Each of them is a function of the ``INFO`` of the
datasets and of their data files, so no fact is written by hand in more than one place.
"""

import ast
import json
import re
from collections.abc import Mapping, Sequence
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Final

import numpy as np

from pyml_datasets import DatasetInfo
from scripts import ROOT

PACKAGE: Final = ROOT / "pyml_datasets"
_LINE_LENGTH: Final = 100
DATASETS_DIR: Final = PACKAGE / "datasets"
DATA_DIR: Final = PACKAGE / "data"
GENERATED_DOCS: Final = ROOT / "docs" / "source" / "_generated"
README_START: Final = "<!-- datasets:start -->"
README_END: Final = "<!-- datasets:end -->"


def dataset_names() -> tuple[str, ...]:
    """List the dataset modules found in ``pyml_datasets/datasets``.

    Returns
    -------
    tuple of str
        Module names in alphabetical order. Files that start with an underscore are not
        datasets. The modules are not imported.
    """
    return tuple(
        sorted(path.stem for path in DATASETS_DIR.glob("*.py") if not path.name.startswith("_"))
    )


def dataset_module(name: str) -> ModuleType:
    """Import the module of a dataset, whether or not the generated index lists it yet.

    The index (``datasets/__init__.py``) is one of the files this module writes, so it can be
    out of date when a new dataset is added. The package registry would then not know the
    dataset, and the module is imported by its name instead.

    Parameters
    ----------
    name : str
        Dataset module name.

    Returns
    -------
    types.ModuleType
        The module ``pyml_datasets.datasets.<name>``.
    """
    return import_module(f"pyml_datasets.datasets.{name}")


def info_of(name: str) -> DatasetInfo:
    """Return the ``INFO`` of a dataset module, see :func:`dataset_module`.

    Parameters
    ----------
    name : str
        Dataset module name.

    Returns
    -------
    DatasetInfo
        The ``INFO`` constant of the module.
    """
    info: DatasetInfo = dataset_module(name).INFO
    return info


def _task_of(path: Path) -> str:
    """Read the task from the source of a dataset module, without importing it.

    The index of the package must be written before the package can list a new dataset, so
    it cannot come from importing the package. The source is parsed instead: ``INFO`` must be
    a call that gives ``task`` as a string.

    Parameters
    ----------
    path : Path
        Source file of a dataset module.

    Returns
    -------
    str
        The value of the ``task`` argument of ``INFO``.

    Raises
    ------
    ValueError
        If the module has no ``INFO`` call with ``task`` given as a string.
    """
    for node in ast.parse(path.read_text("utf-8"), filename=str(path)).body:
        if (
            isinstance(node, ast.AnnAssign | ast.Assign)
            and isinstance(node.value, ast.Call)
            and any(
                isinstance(target, ast.Name) and target.id == "INFO" for target in _targets(node)
            )
        ):
            for keyword in node.value.keywords:
                value = keyword.value
                if (
                    keyword.arg == "task"
                    and isinstance(value, ast.Constant)
                    and isinstance(value.value, str)
                ):
                    return value.value
    raise ValueError(f"{path.name}: INFO must be a call that gives task as a string.")


def _targets(node: ast.AnnAssign | ast.Assign) -> list[ast.expr]:
    """List the targets of an assignment.

    Parameters
    ----------
    node : ast.AnnAssign or ast.Assign
        An assignment statement.

    Returns
    -------
    list of ast.expr
        The names, or other expressions, that the value is assigned to.
    """
    return [node.target] if isinstance(node, ast.AnnAssign) else list(node.targets)


def dataset_tasks() -> dict[str, str]:
    """Read the task of every dataset module found in ``pyml_datasets/datasets``.

    Returns
    -------
    dict of str to str
        Dataset name and task, in alphabetical order of the names.
    """
    return {name: _task_of(DATASETS_DIR / f"{name}.py") for name in dataset_names()}


def render_datasets_init(tasks: Mapping[str, str]) -> str:
    """Write ``pyml_datasets/datasets/__init__.py``, the index of the datasets.

    The index holds the name and the task of every dataset and imports no dataset module, so
    listing the datasets costs nothing. Every entry is on its own line with a trailing comma,
    the form that ``ruff format`` keeps for any number of datasets.

    Parameters
    ----------
    tasks : mapping of str to str
        Dataset name and task.

    Returns
    -------
    str
        Python source with the ``DATASET_TASKS`` mapping.
    """
    entries = "".join(f'    "{name}": "{task}",\n' for name, task in tasks.items())
    return (
        '"""Bundled datasets, one module per dataset.\n\n'
        "This file is generated by ``python -m scripts gen``, do not edit it by hand. It lists\n"
        "the datasets and does not import their modules: a module is imported when its dataset\n"
        "is used, see ``pyml_datasets.get_info`` and the ``__getattr__`` of ``pyml_datasets``.\n"
        '"""\n\n'
        "from collections.abc import Mapping\n"
        "from typing import Final\n\n"
        "from .._types import Task\n\n"
        f"DATASET_TASKS: Final[Mapping[str, Task]] = {{\n{entries}}}\n"
    )


def replace_block(text: str, tag: str, body: str) -> str:
    """Replace the lines between ``# <generated:tag>`` and ``# </generated:tag>``.

    Parameters
    ----------
    text : str
        Source text that contains both markers.
    tag : str
        Name of the block.
    body : str
        New lines of the block, each ending with a newline.

    Returns
    -------
    str
        The text with the block replaced.

    Raises
    ------
    ValueError
        If the markers are not found.
    """
    pattern = re.compile(
        rf"(?P<start>^[ \t]*# <generated:{tag}>\n)(?:.*?)(?P<end>^[ \t]*# </generated:{tag}>)",
        re.DOTALL | re.MULTILINE,
    )
    if not pattern.search(text):
        raise ValueError(f"Markers for the generated block {tag!r} not found.")
    return pattern.sub(lambda match: f"{match['start']}{body}{match['end']}", text, count=1)


def render_package_init(text: str, names: Sequence[str]) -> str:
    """Fill the generated block of ``pyml_datasets/__init__.py``.

    Parameters
    ----------
    text : str
        Current content of the file.
    names : sequence of str
        Dataset module names.

    Returns
    -------
    str
        Content with the ``__all__`` block filled.
    """
    exported = "".join(f'    "load_{name}",\n' for name in names)
    return replace_block(text, "all", exported)


def _stub_import(name: str) -> str:
    """Write the import of one loader the way ``ruff format`` keeps it.

    Parameters
    ----------
    name : str
        Dataset module name.

    Returns
    -------
    str
        One line, or the parenthesised form when the line would pass the line length.
    """
    line = f"from .datasets.{name} import load_{name} as load_{name}\n"
    if len(line) <= _LINE_LENGTH + 1:
        return line
    return f"from .datasets.{name} import (\n    load_{name} as load_{name},\n)\n"


def render_package_stub(names: Sequence[str]) -> str:
    """Write ``pyml_datasets/__init__.pyi``, the type information of the package.

    The loaders are imported by ``__getattr__`` at run time, which type checkers and IDEs
    cannot follow. They read this stub instead, so every loader has its real type and a
    misspelled name is reported.

    Parameters
    ----------
    names : sequence of str
        Dataset module names.

    Returns
    -------
    str
        Stub source, with every name re-exported in the ``name as name`` form.
    """
    loaders = "".join(_stub_import(name) for name in names)
    exported = "".join(f'    "load_{name}",\n' for name in names)
    return (
        "# This file is generated by ``python -m scripts gen``, do not edit it by hand.\n\n"
        "from ._registry import get_info as get_info\n"
        "from ._registry import list_datasets as list_datasets\n"
        "from ._registry import load_dataset as load_dataset\n"
        "from ._types import Dataset as Dataset\n"
        "from ._types import DatasetInfo as DatasetInfo\n"
        f"{loaders}\n"
        "__version__: str\n"
        "__author__: str\n\n"
        "__all__ = [\n"
        '    "Dataset",\n'
        '    "DatasetInfo",\n'
        '    "__version__",\n'
        '    "get_info",\n'
        '    "list_datasets",\n'
        '    "load_dataset",\n'
        f"{exported}]\n"
    )


def render_readme(text: str, table: str) -> str:
    """Put the table of datasets between the markers of the README.

    Parameters
    ----------
    text : str
        Current content of ``README.md``.
    table : str
        Markdown table.

    Returns
    -------
    str
        Content with the table replaced.

    Raises
    ------
    ValueError
        If the README does not contain both markers.
    """
    start, end = text.find(README_START), text.find(README_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"README.md must contain {README_START} and {README_END}.")
    return f"{text[: start + len(README_START)]}\n{table}{text[end:]}"


def load_arrays(name: str) -> dict[str, np.ndarray]:
    """Read all arrays of a data file without allowing pickles.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    dict of str to ndarray
        The arrays of ``data/<name>.npz``.

    Raises
    ------
    FileNotFoundError
        If the data file does not exist. Build it with ``python -m scripts build``.
    """
    path = DATA_DIR / f"{name}.npz"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} does not exist. Build it first: python -m scripts build {name}"
        )
    with np.load(path, allow_pickle=False) as archive:
        return {key: archive[key] for key in archive.files}


def render_manifest(names: Sequence[str]) -> str:
    """Write ``MANIFEST.json``, the digests of the data of every dataset.

    Parameters
    ----------
    names : sequence of str
        Dataset names.

    Returns
    -------
    str
        JSON text.
    """
    from scripts._npz import FORMAT_VERSION, manifest_entry

    datasets = {name: manifest_entry(load_arrays(name)) for name in names}
    manifest = {"format_version": FORMAT_VERSION, "datasets": datasets}
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def expected_files() -> dict[Path, str]:
    """Compute the content of every generated file.

    Returns
    -------
    dict of Path to str
        Path and content of each generated file.
    """
    names = dataset_names()
    files: dict[Path, str] = {DATASETS_DIR / "__init__.py": render_datasets_init(dataset_tasks())}
    # The registry of the package reads the index above, which can be out of date here, so
    # the modules are imported by name. The render module imports the package.
    from pyml_datasets import Dataset
    from scripts._render import (
        Facts,
        facts_of,
        render_api_loaders,
        render_datasets_table,
        render_datasets_toctree,
        render_license_table,
        render_notice,
        render_overview,
        render_provenance,
        render_readme_table,
    )

    infos = [info_of(name) for name in names]
    datas: list[Dataset] = [getattr(dataset_module(name), f"load_{name}")() for name in names]
    facts: dict[str, Facts] = {data.info.name: facts_of(data) for data in datas}

    package_init = PACKAGE / "__init__.py"
    files[package_init] = render_package_init(package_init.read_text("utf-8"), names)
    files[PACKAGE / "__init__.pyi"] = render_package_stub(names)
    files[ROOT / "NOTICE.md"] = render_notice(infos)
    readme = ROOT / "README.md"
    files[readme] = render_readme(readme.read_text("utf-8"), render_readme_table(facts, infos))
    files[DATA_DIR / "MANIFEST.json"] = render_manifest(names)

    files[GENERATED_DOCS / "datasets_table.inc"] = render_datasets_table(datas, facts)
    files[GENERATED_DOCS / "datasets_toctree.inc"] = render_datasets_toctree(infos)
    files[GENERATED_DOCS / "license_table.inc"] = render_license_table(infos)
    files[GENERATED_DOCS / "api_loaders.inc"] = render_api_loaders(infos)
    for data in datas:
        name = data.info.name
        files[GENERATED_DOCS / f"{name}_overview.inc"] = render_overview(data, facts[name])
        files[GENERATED_DOCS / f"{name}_provenance.inc"] = render_provenance(data.info)
    return files


def run(check: bool = False) -> list[Path]:
    """Write the generated files, or only find the ones that are out of date.

    Parameters
    ----------
    check : bool, default=False
        Do not write anything, only report the files whose content is not the expected one.

    Returns
    -------
    list of Path
        The files that were out of date: written if ``check`` is ``False``, left as they are
        otherwise. The list is empty when everything is up to date.
    """
    stale: list[Path] = []
    for path, content in expected_files().items():
        current = path.read_text("utf-8") if path.exists() else None
        if current == content:
            continue
        stale.append(path)
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, "utf-8")
    return stale
