"""Build the bundled NPZ datasets.

Run it manually from the repository root and commit the resulting files::

    python -m scripts.build_datasets
    python -m scripts.build_datasets iris wine --overwrite

Every dataset has a recipe in ``scripts/recipes/`` that loads or downloads the raw data.
``scripts/_npz.py`` validates and saves it. Existing files are skipped unless ``--overwrite``
is given, because NPZ files are not byte-for-byte reproducible and every rebuild adds a new
binary blob to the git history. ``california_housing`` is downloaded by scikit-learn on the
first run and ``wine_quality`` comes from the UCI repository, so both need an internet
connection.
"""

import argparse
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from scripts._npz import save, to_arrays, validate
from scripts.recipes import REGISTRY

_OUTPUT_DIR: Final = Path(__file__).resolve().parents[1] / "pyml_datasets" / "data"


def build_dataset(name: str, output_dir: Path, overwrite: bool = False) -> None:
    """Build one dataset and save it as ``<name>.npz``.

    Parameters
    ----------
    name : str
        Dataset name, one of the keys of the recipe registry.
    output_dir : Path
        Directory where the file is written, created if missing.
    overwrite : bool, default=False
        Replace the file if it already exists, otherwise it is skipped.
    """
    path = output_dir / f"{name}.npz"
    if path.exists() and not overwrite:
        print(f"skip   {name}: {path.name} already exists (use --overwrite)")
        return

    arrays = to_arrays(REGISTRY[name]())
    validate(name, arrays)
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
    parser = argparse.ArgumentParser(description="Build the bundled NPZ datasets.")
    parser.add_argument(
        "names",
        nargs="*",
        metavar="NAME",
        help=f"datasets to build, all by default: {', '.join(REGISTRY)}",
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

    names: list[str] = args.names or list(REGISTRY)
    unknown = [name for name in names if name not in REGISTRY]
    if unknown:
        parser.error(f"unknown dataset(s): {', '.join(unknown)}")

    for name in names:
        build_dataset(name, args.output_dir, args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
