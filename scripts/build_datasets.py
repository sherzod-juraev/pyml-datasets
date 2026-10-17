"""Build the bundled NPZ datasets.

Run it from the repository root and commit the resulting files::

    python -m scripts.build_datasets
    python -m scripts.build_datasets iris wine --overwrite

Every dataset has a recipe in ``scripts/recipes/`` that loads or downloads the raw data, and
an ``INFO`` in ``pyml_datasets/datasets/`` that says where the data comes from and under
which license. ``scripts/_npz.py`` combines both, validates the result and saves it. Existing
files are skipped unless ``--overwrite`` is given, because NPZ files are not byte-for-byte
reproducible and every rebuild adds a new binary file to the git history. Some recipes
download data, so they need an internet connection.

After building, run ``python -m scripts.generate`` to refresh the manifest, the notice and
the documentation.
"""

import argparse
from collections.abc import Sequence
from importlib import import_module
from pathlib import Path
from typing import Final

from pyml_datasets import DatasetInfo
from scripts import ROOT
from scripts._npz import save, to_arrays, validate
from scripts.recipes import get_recipe, recipe_names

_OUTPUT_DIR: Final = ROOT / "pyml_datasets" / "data"


def _info_of(name: str) -> DatasetInfo:
    """Import the dataset module and return its ``INFO``.

    The module is imported directly and not through the registry, so a dataset that was
    just scaffolded can be built before ``scripts.generate`` has registered it.

    Parameters
    ----------
    name : str
        Dataset name.

    Returns
    -------
    DatasetInfo
        The ``INFO`` constant of ``pyml_datasets/datasets/<name>.py``.
    """
    info: DatasetInfo = import_module(f"pyml_datasets.datasets.{name}").INFO
    return info


def build_dataset(name: str, output_dir: Path, overwrite: bool = False) -> None:
    """Build one dataset and save it as ``<name>.npz``.

    Parameters
    ----------
    name : str
        Dataset name, one of ``recipe_names()``.
    output_dir : Path
        Directory where the file is written, created if missing.
    overwrite : bool, default=False
        Replace the file if it already exists, otherwise it is skipped.
    """
    path = output_dir / f"{name}.npz"
    if path.exists() and not overwrite:
        print(f"skip   {name}: {path.name} already exists (use --overwrite)")
        return

    info = _info_of(name)
    arrays = to_arrays(get_recipe(name)(), info)
    validate(info, arrays)
    save(path, arrays)

    size_kib = path.stat().st_size / 1024
    print(f"built  {name}: X{arrays['X'].shape} -> {path.name} ({size_kib:.1f} KiB)")


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
    available = recipe_names()
    parser = argparse.ArgumentParser(description="Build the bundled NPZ datasets.")
    parser.add_argument(
        "names",
        nargs="*",
        metavar="NAME",
        help=f"datasets to build, all by default: {', '.join(available)}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_OUTPUT_DIR,
        help="directory for the NPZ files (default: pyml_datasets/data)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace files that already exist",
    )
    args = parser.parse_args(argv)

    names: list[str] = args.names or list(available)
    unknown = [name for name in names if name not in available]
    if unknown:
        parser.error(f"unknown dataset(s): {', '.join(unknown)}")

    for name in names:
        build_dataset(name, args.output_dir, args.overwrite)
    print("Next: python -m scripts.generate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
