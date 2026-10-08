# Contributing

> [!NOTE]
> This is a personal, educational project. I am not
> actively seeking contributors at this time.

However, this project is open-source, and you are **welcome to**:

- **Fork** this repository.
- **Copy** the code.
- **Modify** it for your own needs.
- **Develop** your own version independently.

The code is under the [MIT License](LICENSE), but the datasets are not: every dataset keeps the
terms of its original source (see [LICENSES](LICENSES) and the
[documentation](https://pyml-datasets.readthedocs.io/en/latest/license.html)). If you copy or
redistribute the data files, follow those terms.

If you build something interesting, I would love to hear about it.

The rest of this file is also a map of the project: where things are, how to check them, and
how a new dataset or a release is done.

## Quick start

```bash
git clone https://github.com/sherzod-juraev/pyml-datasets.git
cd pyml-datasets
pip install -e ".[nox]"
nox
```

`nox` runs every default session (see [Nox sessions](#nox-sessions)) in isolated virtual
environments, the same way as the CI.

## Project structure

```text
pyml-datasets/
├── .github/workflows/          # CI workflows
├── assets/                     # Branding
├── docs/                       # Sphinx documentation
├── LICENSES/                   # Licenses of the datasets
├── pyml_datasets/              # Source code
│   ├── data/                   # The .npz files
│   ├── _loader.py              # Dataset class and the file loader
│   ├── _sklearn.py             # Datasets that come from scikit-learn
│   └── _wine_quality.py        # Wine Quality (UCI)
├── scripts/                    # Scripts that generate the data files
├── tests/                      # Test suite
├── .gitignore                  # Git ignore rules
├── .readthedocs.yaml           # Read the Docs config
├── CONTRIBUTING.md             # This file
├── LICENSE                     # MIT License
├── noxfile.py                  # Nox sessions
├── pyproject.toml              # Project metadata and tool config
└── README.md                   # Project overview
```

## Development setup

### Requirements

- Python 3.12, 3.13 and 3.14. Install all three to run the whole Nox matrix, or run a single
  version, for example `nox -s tests-3.13`.

### Optional extras

The project defines the following extras in [pyproject.toml](pyproject.toml).

| Extra  |                         Purpose                          |
|:-------|:--------------------------------------------------------:|
| `nox`  |          Nox, which runs all the quality checks          |
| `dev`  | mypy, ruff, pytest, interrogate, scikit-learn, ucimlrepo |
| `docs` |              Sphinx and documentation tools              |
| `all`  |                     `dev` and `docs`                     |

`scikit-learn` and `ucimlrepo` are needed only to generate the data files and to compare them
with the originals in the tests. They are not runtime dependencies: the package itself needs
NumPy only.

### Setup

Install the extras you need:

- Nox (recommended, runs everything in isolated environments):

```bash
pip install -e ".[nox]"
```

- Development dependencies, to run a tool directly in your own environment:

```bash
pip install -e ".[dev]"
```

- Documentation tools:

```bash
pip install -e ".[docs]"
```

- Development and documentation together:

```bash
pip install -e ".[all]"
```

## Quality tooling

| Tool                        |                  Checks                   |
|:----------------------------|:-----------------------------------------:|
| mypy (strict)               |            Static type checking           |
| interrogate                 |         Docstring coverage (100%)         |
| ruff                        |           Linting and formatting          |
| pytest                      |      Test suite, also with oldest NumPy   |
| sphinx-lint, doc8, rstcheck |      Documentation style and syntax       |
| sphinx linkcheck            |    Validity of every link in the docs     |
| wheel check                 | Contents of the built wheel, smoke test   |

Each tool is configured in [pyproject.toml](pyproject.toml) and run by a Nox session, see
[Nox sessions](#nox-sessions) below.

## Nox sessions

This project uses [Nox](https://nox.thea.codes/) to run all quality checks in isolated
environments. Nox creates a separate virtual environment for each session, installs the
required dependencies, and runs the configured commands. This guarantees reproducibility
across machines and Python versions.

| Session      |      Python      |                           What it runs                            |
|:-------------|:----------------:|:-----------------------------------------------------------------:|
| `lint`       |       3.13       |                ruff check and ruff format --check                 |
| `types`      |       3.13       |        mypy (strict) on `pyml_datasets`, `scripts`, `tests`       |
| `docstrings` |       3.13       |           interrogate, docstring coverage must be 100%            |
| `tests`      | 3.12, 3.13, 3.14 |                              pytest                               |
| `tests-min`  |       3.12       |             pytest with the oldest NumPy that is supported        |
| `docs`       |       3.13       |  sphinx-lint, doc8, rstcheck, `sphinx-build -W`, Sphinx doctest   |
| `linkcheck`  |       3.13       |        Sphinx linkcheck, validity of every link in the docs       |
| `package`    |       3.13       | builds the wheel, checks its contents, loads every dataset from it |

`nox` without arguments runs every session except `linkcheck`, which needs the network and is
slow.

```bash
nox -l                          # list all sessions
nox -s lint                     # run one session
nox -s tests-3.13               # run one session on one Python version
nox -s tests -- -k wine         # arguments after -- are passed to pytest
nox -R                          # reuse the existing virtual environments, much faster
```

### What the `package` session guards

The session builds the wheel and then fails if:

- `py.typed` or `__init__.py` is missing,
- an `.npz` file from `pyml_datasets/data/` is not in the wheel,
- the license files are missing from the metadata,
- `tests/`, `docs/` or `scripts/` leaked into the wheel.

After that it installs the wheel into a clean environment, moves out of the repository, and
loads **every** `load_*` function listed in `__all__`. A dataset is therefore tested
automatically as soon as it is exported.

## Continuous integration

Every workflow calls Nox, so a failure in the CI can always be reproduced locally with the
same command.

| Workflow            |                Sessions                |                   When                   |
|:--------------------|:--------------------------------------:|:----------------------------------------:|
| `tests.yml`         | `tests-<version>`, `tests-min`         | push, pull request, every Monday         |
| `quality.yml`       | `lint`, `types`, `docstrings`, `package` | push, pull request                     |
| `docs.yml`          |                 `docs`                 | push, pull request                       |
| `docs-linkcheck.yml`|              `linkcheck`               | every week                               |

## Conventions

### Code

- Importing the package reads no data. Imports in `__init__.py` are eager on purpose (the
  package is tiny), and a data file is read only when a `load_*` function is called.
- Every loader returns a `Dataset` with a two-dimensional `X` and a `y` of the same length.
  The `package` session checks this for every exported loader.
- Public names are listed in `__all__` and imported from the package root:
  `from pyml_datasets import load_iris`.
- The runtime depends on NumPy only. Anything else (scikit-learn, ucimlrepo) belongs to the
  `dev` extra and to `scripts/`.
- Everything is checked by mypy in strict mode, ruff (line length 100) and interrogate
  (100% docstring coverage, private members included).

### Docstrings

- NumPy style.
- The module docstring is short prose.
- Every public loader documents what it returns, the shape of the data and the source.

### Tests

- `tests/` has one file per module (`test_loader.py`, `test_sklearn_datasets.py`, ...) plus
  `test_init.py` for the public API.
- Tests are grouped in classes by behavior. There is only a module docstring, no docstrings
  on the tests.
- Data files are compared with the originals (for example scikit-learn) where an original
  exists.

### Commits and versions

- Commits follow [Conventional Commits](https://www.conventionalcommits.org/): `feat`, `fix`,
  `docs`, `test`, `build`, `refactor` and `chore`, with a body that explains what changed and
  why.
- Work happens on `dev`. `main` receives a merge only when all checks pass.
- `__version__` in `pyml_datasets/__init__.py` is the single source of truth, `pyproject.toml`
  and the docs read it. It changes only when the public API changes (a new dataset or a
  breaking change is a MINOR bump while the version is 0.x). Housekeeping commits do not
  change it.

## Adding a dataset

1. Check the license of the source first. A dataset whose terms do not allow redistribution
   does not go into this repository.
2. Write a script in `scripts/` that generates the `.npz` file, so the file can always be
   reproduced.
3. Put the file into `pyml_datasets/data/`. The `data/*.npz` pattern in `pyproject.toml`
   includes it in the wheel automatically.
4. Add the `load_*` function (in a new module if the source is new), import it in
   `pyml_datasets/__init__.py` and add it to `__all__`.
5. Add the license text to `LICENSES/` if the source needs one.
6. Write the tests in `tests/`.
7. Add the documentation: the dataset page with its license, source and citation, and a row
   in the README table.
8. Run `nox` until every session passes.

## Releasing

1. Run `nox` on `dev`, and make sure the CI is green.
2. Bump `__version__` in `pyml_datasets/__init__.py` if the public API changed.
3. Merge `dev` into `main` and push.
4. Create the tag `vX.Y.Z` on `main` and a GitHub release titled `vX.Y.Z — <What Changed>`.
5. Check that the Read the Docs build is green.
