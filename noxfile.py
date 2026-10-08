"""Nox sessions: the quality checks that run locally and in the CI.

Run ``nox -l`` to list the sessions and ``nox`` to run the default ones.
"""

import shutil
import tomllib
import zipfile
from pathlib import Path

import nox

PYTHON_VERSIONS = ["3.12", "3.13", "3.14"]
DEFAULT_PYTHON = "3.13"

_PACKAGE = "pyml_datasets"
_SOURCE_PATHS = [_PACKAGE, "scripts", "tests", "noxfile.py"]
_DOCS_SOURCE = "docs/source"
_DOCS_HTML = "docs/build/html"
_DOCS_DOCTEST = "docs/build/doctest"
_DOCS_LINKCHECK = "docs/build/linkcheck"

_DATA_DIR = Path(_PACKAGE) / "data"
_WHEEL_REQUIRED = [f"{_PACKAGE}/py.typed", f"{_PACKAGE}/__init__.py"]
_WHEEL_LICENSES = [".dist-info/licenses/LICENSE", ".dist-info/licenses/LICENSES/CC-BY-4.0.txt"]
_WHEEL_FORBIDDEN_PREFIXES = ("tests/", "docs/", "scripts/")

# Runs inside the session, from a folder outside the repository, against the installed wheel.
_SMOKE_TEST = """
from pathlib import Path

import pyml_datasets

location = Path(pyml_datasets.__file__).resolve()
assert "site-packages" in location.parts, f"not imported from site-packages: {location}"
assert isinstance(pyml_datasets.__version__, str)

loaders = [name for name in pyml_datasets.__all__ if name.startswith("load_")]
assert loaders, "the package exports no loaders"
for name in loaders:
    data = getattr(pyml_datasets, name)()
    assert data.X.ndim == 2 and len(data.X) == len(data.y), name
print("pyml_datasets", pyml_datasets.__version__, "from", location.parent)
print("loaded", len(loaders), "datasets:", ", ".join(loaders))
"""

# Checks that the pinned minimum versions were not raised by the resolver.
_CHECK_VERSIONS = """
import sys
from importlib.metadata import version

from packaging.version import Version

for requirement in sys.argv[1:]:
    name, _, expected = requirement.partition("==")
    installed = version(name)
    message = f"{name} {installed} is installed, expected {expected}"
    assert Version(installed) == Version(expected), message
    print(name, installed)
"""

nox.options.sessions = ["lint", "types", "docstrings", "tests", "tests-min", "docs", "package"]
nox.options.error_on_external_run = True


def _minimum_requirements() -> list[str]:
    """Return the runtime dependencies with every lower bound pinned exactly.

    The dependencies are read from ``pyproject.toml``, so the lowest supported versions are
    written in one place only. Only simple ``name>=version`` requirements are supported.
    """
    with Path("pyproject.toml").open("rb") as file:
        dependencies: list[str] = tomllib.load(file)["project"]["dependencies"]
    return [requirement.replace(">=", "==") for requirement in dependencies]


def _check_wheel_contents(session: nox.Session, wheel: Path) -> None:
    """Fail the session if the wheel lacks files users need or ships files they do not.

    Every ``.npz`` file found in the source tree must be in the wheel, so a dataset that is
    left out of the package data is noticed without keeping a list of datasets here.

    Parameters
    ----------
    session : nox.Session
        Session that reports the error.
    wheel : Path
        Wheel file to inspect.
    """
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()

    problems = [f"missing {name}" for name in _WHEEL_REQUIRED if name not in names]

    data_files = sorted(path.name for path in _DATA_DIR.glob("*.npz"))
    if not data_files:
        problems.append(f"no .npz files found in {_DATA_DIR.as_posix()}")
    problems += [
        f"missing {_PACKAGE}/data/{name}"
        for name in data_files
        if f"{_PACKAGE}/data/{name}" not in names
    ]

    problems += [
        f"missing {suffix.removeprefix('.dist-info/')} in the metadata"
        for suffix in _WHEEL_LICENSES
        if not any(name.endswith(suffix) for name in names)
    ]
    problems += [
        f"unexpected {name}" for name in names if name.startswith(_WHEEL_FORBIDDEN_PREFIXES)
    ]

    if problems:
        session.error(f"{wheel.name}: " + "; ".join(problems))


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session) -> None:
    """Check the code style and the formatting with ruff."""
    session.install(".[dev]")
    session.run("ruff", "check", *_SOURCE_PATHS)
    session.run("ruff", "format", "--check", *_SOURCE_PATHS)


@nox.session(python=DEFAULT_PYTHON)
def types(session: nox.Session) -> None:
    """Check the types with mypy in strict mode."""
    session.install(".[dev]")
    session.run("mypy", _PACKAGE, "scripts")
    session.run("mypy", "tests")


@nox.session(python=DEFAULT_PYTHON)
def docstrings(session: nox.Session) -> None:
    """Check that the docstring coverage of the package and the scripts is 100%."""
    session.install(".[dev]")
    session.run("interrogate", _PACKAGE, "scripts")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite on every supported Python version.

    Arguments after ``--`` are passed to pytest, for example ``nox -s tests -- -k wine``.
    """
    session.install(".[dev]")
    session.run("pytest", *session.posargs)


@nox.session(name="tests-min", python=PYTHON_VERSIONS[0])
def tests_min(session: nox.Session) -> None:
    """Run the test suite with the oldest NumPy that pyml-datasets claims to support."""
    minimum = _minimum_requirements()
    # One install call on purpose: for pip an installed package is only a preference, so a
    # second call would raise NumPy to the version that the dev dependencies (scikit-learn,
    # SciPy) want and the test would no longer run on the minimum.
    session.install(".[dev]", *minimum)
    session.run("python", "-c", _CHECK_VERSIONS, *minimum)
    session.run("pytest", *session.posargs)


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session) -> None:
    """Check the documentation style, run its doctests and build it with warnings as errors."""
    session.install(".[docs]")
    session.run("sphinx-lint", _DOCS_SOURCE)
    session.run("doc8", _DOCS_SOURCE)
    session.run("rstcheck", "--recursive", _DOCS_SOURCE)
    session.run("sphinx-build", "-b", "html", "-W", "--keep-going", "-E", _DOCS_SOURCE, _DOCS_HTML)
    session.run(
        "sphinx-build",
        *("-b", "doctest", "-W", "--keep-going", "-E"),
        _DOCS_SOURCE,
        _DOCS_DOCTEST,
    )


@nox.session(python=DEFAULT_PYTHON)
def linkcheck(session: nox.Session) -> None:
    """Check that every link in the documentation is valid (needs the network, so it is slow)."""
    session.install(".[docs]")
    session.run("sphinx-build", "-b", "linkcheck", "-E", _DOCS_SOURCE, _DOCS_LINKCHECK)


@nox.session(python=DEFAULT_PYTHON)
def package(session: nox.Session) -> None:
    """Build the wheel, check its contents and load every dataset from an installed copy."""
    session.install("build")
    dist = Path(session.create_tmp()) / "dist"
    # Leftovers of an earlier build would be packed into the new wheel as they are.
    for leftover in (dist, Path("build"), *Path().glob("*.egg-info")):
        shutil.rmtree(leftover, ignore_errors=True)
    session.run("python", "-m", "build", "--wheel", "--outdir", str(dist))

    wheels = list(dist.glob("*.whl"))
    if len(wheels) != 1:
        session.error(f"expected exactly one wheel, found {len(wheels)}.")
    _check_wheel_contents(session, wheels[0])

    session.install(str(wheels[0]))
    session.chdir(session.create_tmp())
    session.run("python", "-c", _SMOKE_TEST)
