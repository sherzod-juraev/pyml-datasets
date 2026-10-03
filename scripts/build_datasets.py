"""Build the bundled NPZ datasets from scikit-learn.

Run it manually from the repository root and commit the resulting files::

    python scripts/build_datasets.py
    python scripts/build_datasets.py iris wine --overwrite

Existing files are skipped unless ``--overwrite`` is given, because NPZ files
are not byte-for-byte reproducible and every rebuild adds a new binary blob to
the git history. ``california_housing`` is downloaded by scikit-learn on the
first run, so it needs an internet connection.
"""

import argparse
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, Final, Literal

import numpy as np
import sklearn
from numpy.typing import NDArray
from sklearn.datasets import (
    fetch_california_housing,
    load_breast_cancer,
    load_diabetes,
    load_iris,
    load_linnerud,
    load_wine,
)

_OUTPUT_DIR: Final = Path(__file__).resolve().parents[1] / "pyml_datasets" / "data"


@dataclass(frozen=True)
class _Spec:
    """Recipe for building one dataset file."""

    load: Callable[[], Any]
    task: Literal["classification", "regression"]


_SPECS: Final[dict[str, _Spec]] = {
    "iris": _Spec(load_iris, "classification"),
    "wine": _Spec(load_wine, "classification"),
    "breast_cancer": _Spec(load_breast_cancer, "classification"),
    "diabetes": _Spec(partial(load_diabetes, scaled=False), "regression"),
    "linnerud": _Spec(load_linnerud, "regression"),
    "california_housing": _Spec(fetch_california_housing, "regression"),
}


def _build_arrays(bunch: Any, spec: _Spec) -> dict[str, NDArray[Any]]:
    """Convert a scikit-learn ``Bunch`` into the arrays stored in the NPZ file.

    Parameters
    ----------
    bunch : Bunch
        Object returned by a scikit-learn dataset loader.
    spec : _Spec
        Recipe of the dataset, its task decides the dtype of ``y``.

    Returns
    -------
    dict of str to ndarray
        Arrays ``X``, ``y``, ``feature_names``, ``description`` and
        ``sklearn_version``, plus ``target_names`` if the source has them.
    """
    y_dtype = np.int64 if spec.task == "classification" else np.float64
    arrays: dict[str, NDArray[Any]] = {
        "X": np.asarray(bunch.data, dtype=np.float64),
        "y": np.asarray(bunch.target, dtype=y_dtype),
        "feature_names": np.asarray(bunch.feature_names),
        "description": np.asarray(bunch.DESCR),
        "sklearn_version": np.asarray(sklearn.__version__),
    }
    target_names = getattr(bunch, "target_names", None)
    if target_names is not None:
        arrays["target_names"] = np.asarray(target_names)
    return arrays


def _validate(name: str, arrays: dict[str, NDArray[Any]]) -> None:
    """Check the basic structure of the arrays before they are saved.

    Parameters
    ----------
    name : str
        Dataset name, used in error messages.
    arrays : dict of str to ndarray
        Arrays produced by ``_build_arrays``.

    Raises
    ------
    ValueError
        If ``X`` is not a finite 2D matrix, or if ``y`` or ``feature_names``
        do not match its shape.
    """
    X, y = arrays["X"], arrays["y"]
    if X.ndim != 2:
        raise ValueError(f"{name}: X must be 2D, got {X.ndim}D.")
    if not np.isfinite(X).all():
        raise ValueError(f"{name}: X contains NaN or infinite values.")
    if len(y) != len(X):
        raise ValueError(f"{name}: y has {len(y)} rows but X has {len(X)}.")
    if len(arrays["feature_names"]) != X.shape[1]:
        raise ValueError(f"{name}: feature_names does not match the columns of X.")


def build_dataset(name: str, output_dir: Path, overwrite: bool = False) -> None:
    """Build one dataset and save it as ``<name>.npz``.

    Parameters
    ----------
    name : str
        Dataset name, one of the keys of the dataset recipes.
    output_dir : Path
        Directory where the file is written, created if missing.
    overwrite : bool, default=False
        Replace the file if it already exists, otherwise it is skipped.
    """
    path = output_dir / f"{name}.npz"
    if path.exists() and not overwrite:
        print(f"skip   {name}: {path.name} already exists (use --overwrite)")
        return

    spec = _SPECS[name]
    arrays = _build_arrays(spec.load(), spec)
    _validate(name, arrays)

    output_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **arrays)
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
        help=f"datasets to build, all by default: {', '.join(_SPECS)}",
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

    names: list[str] = args.names or list(_SPECS)
    unknown = [name for name in names if name not in _SPECS]
    if unknown:
        parser.error(f"unknown dataset(s): {', '.join(unknown)}")

    for name in names:
        build_dataset(name, args.output_dir, args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
