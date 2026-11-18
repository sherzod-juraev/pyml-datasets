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
_MARKDOWN_LINKS_REPORT = "docs/build/markdown-links/report.md"

_DATA_DIR = Path(_PACKAGE) / "data"
_WHEEL_REQUIRED = [
    f"{_PACKAGE}/py.typed",
    f"{_PACKAGE}/__init__.pyi",
    f"{_PACKAGE}/__init__.py",
    f"{_PACKAGE}/__main__.py",
    f"{_PACKAGE}/_cli/__init__.py",
    f"{_PACKAGE}/data/MANIFEST.json",
]
# The command that the wheel installs, as ``entry_points.txt`` has to say it.
_WHEEL_ENTRY_POINTS = ".dist-info/entry_points.txt"
_WHEEL_COMMAND = "pyml-datasets = pyml_datasets._cli:main"
# The metadata of the wheel has to name the ``cli`` extra, which holds rich and rich-argparse.
_WHEEL_METADATA = ".dist-info/METADATA"
# The notice and the text of every license the data is under must travel with the wheel.
_WHEEL_LICENSES = [
    ".dist-info/licenses/LICENSE",
    ".dist-info/licenses/NOTICE.md",
    ".dist-info/licenses/LICENSES/CC-BY-4.0.txt",
    ".dist-info/licenses/LICENSES/CC0-1.0.txt",
]
_WHEEL_FORBIDDEN_PREFIXES = ("tests/", "docs/", "scripts/")

# Runs inside the session, from a folder outside the repository, against the installed wheel.
_SMOKE_TEST = """
from pathlib import Path

import pyml_datasets

location = Path(pyml_datasets.__file__).resolve()
assert "site-packages" in location.parts, f"not imported from site-packages: {location}"
assert isinstance(pyml_datasets.__version__, str)

names = pyml_datasets.list_datasets()
assert names, "the package bundles no datasets"
loaders = [f"load_{name}" for name in names]
for loader in loaders:
    assert loader in pyml_datasets.__all__, loader
for name in loaders:
    data = getattr(pyml_datasets, name)()
    assert data.X.ndim == 2 and len(data.X) == len(data.y), name
    assert data.info.license in {"CC0-1.0", "CC-BY-4.0"}, name
    assert data.info.citation in data.description.replace("\\n  ", " ").replace("\\n", " "), name
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

nox.options.sessions = [
    "lint",
    "types",
    "docstrings",
    "legal",
    "markdown",
    "tests",
    "tests-min",
    "docs",
    "package",
]
nox.options.default_venv_backend = "uv"
nox.options.error_on_external_run = True


def _sync(session: nox.Session, *flags: str) -> None:
    """Install the locked environment into the session's own virtual environment.

    The environment is installed from ``uv.lock`` without changing it, so the session
    fails if the lock file is out of date. No dependency group is installed unless it
    is passed in ``flags``.

    Parameters
    ----------
    session : nox.Session
        Session whose virtual environment receives the packages.
    *flags : str
        Extra arguments for ``uv sync``, for example ``"--group", "dev"`` or
        ``"--only-group", "dev-lint"``. The packages of the command line (``rich`` and
        ``rich-argparse``) are installed with ``"--extra", "cli"``.
    """
    session.run_install(
        "uv",
        "sync",
        "--locked",
        "--no-default-groups",
        *flags,
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
        external=True,
    )


def _pytest(session: nox.Session) -> None:
    """Run pytest and check the coverage of the package.

    The coverage is measured, with the settings of ``pyproject.toml``, only when no arguments
    follow ``--``. A single test or a selection of tests cannot reach the threshold of the
    whole package, so with arguments the session runs plain pytest.

    Parameters
    ----------
    session : nox.Session
        Session that runs pytest. Its arguments after ``--`` are passed to pytest.
    """
    coverage = [] if session.posargs else ["--cov"]
    session.run("pytest", *coverage, *session.posargs)


def _minimum_requirements() -> list[str]:
    """Return the runtime dependencies and the ``cli`` extra with every lower bound pinned.

    The dependencies are read from ``pyproject.toml``, so the lowest supported versions are
    written in one place only. Only simple ``name>=version`` requirements are supported.
    """
    with Path("pyproject.toml").open("rb") as file:
        project = tomllib.load(file)["project"]
    requirements: list[str] = [*project["dependencies"], *project["optional-dependencies"]["cli"]]
    return [requirement.replace(">=", "==") for requirement in requirements]


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
        entry_points = "".join(
            archive.read(name).decode("utf-8")
            for name in names
            if name.endswith(_WHEEL_ENTRY_POINTS)
        )
        metadata = "".join(
            archive.read(name).decode("utf-8") for name in names if name.endswith(_WHEEL_METADATA)
        )

    problems = [f"missing {name}" for name in _WHEEL_REQUIRED if name not in names]
    if "Provides-Extra: cli" not in metadata:
        problems.append("the metadata does not declare the extra 'cli'")
    if _WHEEL_COMMAND not in entry_points:
        problems.append(f"the metadata does not declare the command {_WHEEL_COMMAND!r}")

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
    _sync(session, "--only-group", "dev-lint")
    session.run("ruff", "check", *_SOURCE_PATHS)
    session.run("ruff", "format", "--check", *_SOURCE_PATHS)


@nox.session(python=DEFAULT_PYTHON)
def types(session: nox.Session) -> None:
    """Check the types with mypy in strict mode."""
    _sync(session, "--extra", "cli", "--group", "dev-types", "--group", "dev-test")
    session.run("mypy", _PACKAGE, "scripts")
    session.run("mypy", "tests")
    # The stub names every loader; stubtest fails when it differs from the real module.
    session.run("stubtest", "--allowlist", "tests/stubtest_allowlist.txt", _PACKAGE)


@nox.session(python=DEFAULT_PYTHON)
def docstrings(session: nox.Session) -> None:
    """Check that the docstring coverage is 100% and that the examples in them run."""
    _sync(session, "--extra", "cli", "--group", "dev-docstring", "--group", "dev-test")
    session.run("interrogate", _PACKAGE, "scripts")
    session.run("pytest", "--doctest-modules", _PACKAGE)


@nox.session(python=DEFAULT_PYTHON)
def legal(session: nox.Session) -> None:
    """Check licenses and evidence, and that the generated files are up to date."""
    _sync(session, "--group", "dev")
    session.run("python", "-m", "scripts", "check")


@nox.session(python=DEFAULT_PYTHON)
def markdown(session: nox.Session) -> None:
    """Check the syntax and the style of the Markdown files with rumdl (settings: .rumdl.toml)."""
    _sync(session, "--only-group", "md-lint")
    session.run("rumdl", "check", ".")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite on every supported Python version and check the coverage.

    Arguments after ``--`` are passed to pytest, for example ``nox -s tests -- -k wine``. The
    coverage is not measured then, see ``_pytest``.
    """
    _sync(session, "--extra", "cli", "--group", "dev-test")
    _pytest(session)


@nox.session(name="tests-min", python=PYTHON_VERSIONS[0])
def tests_min(session: nox.Session) -> None:
    """Run the test suite with the oldest NumPy, rich and rich-argparse that are supported."""
    _sync(session, "--extra", "cli", "--group", "dev-test")
    minimum = _minimum_requirements()
    session.install(*minimum)
    session.run("python", "-c", _CHECK_VERSIONS, *minimum)
    _pytest(session)


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session) -> None:
    """Check the documentation style, run its doctests and build it with warnings as errors."""
    _sync(session, "--extra", "cli", "--group", "docs")
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
    _sync(session, "--extra", "cli", "--group", "docs-build")
    session.run("sphinx-build", "-b", "linkcheck", "-E", _DOCS_SOURCE, _DOCS_LINKCHECK)


@nox.session(name="markdown-links", python=DEFAULT_PYTHON)
def markdown_links(session: nox.Session) -> None:
    """Check the external links of the Markdown files with lychee (needs the network, slow).

    Only ``http`` and ``https`` addresses are checked. Links between the files and anchors are
    not. The report is written to ``docs/build/markdown-links/report.md``.
    """
    _sync(session, "--only-group", "md-links")
    listing = session.run("git", "ls-files", "*.md", external=True, silent=True)
    files = (listing or "").split()
    if not files:
        session.error("git lists no Markdown files.")
    Path(_MARKDOWN_LINKS_REPORT).parent.mkdir(parents=True, exist_ok=True)
    session.run(
        "lychee",
        *("--scheme", "https", "--scheme", "http"),
        *("--no-progress", "--format", "markdown"),
        *("--output", _MARKDOWN_LINKS_REPORT),
        *files,
    )


@nox.session(python=DEFAULT_PYTHON)
def package(session: nox.Session) -> None:
    """Build the wheel, check its contents, load every dataset and run the installed command."""
    _sync(session, "--group", "dev-package")
    dist = Path(session.create_tmp()) / "dist"
    # Leftovers of an earlier build would be packed into the new wheel as they are.
    for leftover in (dist, Path("build"), *Path().glob("*.egg-info")):
        shutil.rmtree(leftover, ignore_errors=True)
    session.run("python", "-m", "build", "--wheel", "--outdir", str(dist))

    wheels = list(dist.glob("*.whl"))
    if len(wheels) != 1:
        session.error(f"expected exactly one wheel, found {len(wheels)}.")
    # The session changes its directory below, so the path of the wheel must not depend on it.
    wheel = wheels[0].resolve()
    _check_wheel_contents(session, wheel)

    # First without the ``cli`` extra: the data needs NumPy alone, and the command must say what
    # is missing, with the exit code 3, and not fail with a traceback.
    session.install(str(wheel))
    session.chdir(session.create_tmp())
    session.run("python", "-c", _SMOKE_TEST)
    for command in (["pyml-datasets", "list"], ["python", "-m", "pyml_datasets", "list"]):
        refusal = session.run(*command, success_codes=[3], silent=True) or ""
        if "pip install rich rich-argparse" not in refusal or "Traceback" in refusal:
            session.error(f"{' '.join(command)} without the cli extra printed:\n{refusal}")
    # Then with the extra, the command of the wheel as a user starts it: by its name and as a
    # module.
    session.install(f"{wheel}[cli]")
    session.run("pyml-datasets", "list")
    session.run("pyml-datasets", "show", "iris")
    session.run("python", "-m", "pyml_datasets", "list")
