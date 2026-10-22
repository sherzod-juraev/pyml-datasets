# Contributing

> [!NOTE]
> This is a personal, educational project. I am **not** looking for contributors or
> collaborators, and I may be slow to answer, or not answer, issues and pull requests. I would
> rather say this honestly than let you wait for a reply.

This project is open-source under the [MIT License](LICENSE), and you are **welcome to**:

- **Fork** this repository.
- **Copy** the code.
- **Modify** it for your own needs.
- **Develop** your own version independently.

If you build something interesting, I would love to hear about it. The datasets keep their own
licenses, see [Admission policy](#dataset-admission-policy) before you copy any of them.

The rest of this file is a map of the project, written mostly for myself and for anyone who
forks it: where things are, how to check them, and how to add a dataset or make a release.

## Quick start

The project uses [uv](https://docs.astral.sh/uv/) to manage Python versions, dependencies and
virtual environments. Install it first, see the
[uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone https://github.com/sherzod-juraev/pyml-datasets.git
cd pyml-datasets
uv run --locked --only-group nox nox
```

The last command installs only Nox, at the version pinned in `uv.lock`, and runs every default
session (see [Nox sessions](#nox-sessions)) in isolated virtual environments, the same way as
the CI.

To work on the code, create the project environment (`.venv`) with the development tools:

```bash
uv sync --locked    # the default group, dev: tests, lint, types, docstrings, packaging
uv run pytest       # run a command inside .venv, no activation needed
```

## Project structure

```text
pyml-datasets/
├── .github/workflows/          # CI workflows, each one calls Nox through uv
├── assets/branding/            # Logos
├── docs/source/                # Sphinx documentation
│   ├── _generated/             # Generated includes (do not edit)
│   ├── datasets/               # One page per dataset
│   └── design/                 # Design notes
├── legal/evidence/             # One evidence file per dataset: where the license was read
├── LICENSES/                   # Full text of every license the data is under
├── pyml_datasets/              # Source code
│   ├── data/                   # <name>.npz files and MANIFEST.json (generated)
│   ├── datasets/               # One module per dataset: INFO + load_<name>()
│   │   └── __init__.py         # ENTRIES, the registry input (generated)
│   ├── _loader.py              # Reads an npz file into a Dataset
│   ├── _registry.py            # list_datasets, get_info, load_dataset
│   └── _types.py               # DatasetInfo and Dataset
├── scripts/                    # Development tools, not shipped in the wheel
│   ├── recipes/                # One recipe per dataset: how to get the arrays
│   ├── build_datasets.py       # recipe + INFO -> data/<name>.npz
│   ├── generate.py             # INFO -> registry, NOTICE, README table, docs, manifest
│   ├── check_legal.py          # The legal gate
│   └── new_dataset.py          # Scaffolds the files of a new dataset
├── tests/                      # Test suite, organised by concern
│   └── expected/               # One module per dataset: independent facts
├── CONTRIBUTING.md             # This file
├── LICENSE                     # MIT License (the code)
├── NOTICE.md                   # Creators, sources, citations, changes (generated)
├── noxfile.py                  # Nox sessions
├── pyproject.toml              # Project metadata, dependency groups and tool config
├── README.md                   # Project overview
└── uv.lock                     # Exact version of every locked dependency (committed)
```

The idea behind the layout: **a dataset is described once**, in `pyml_datasets/datasets/<name>.py`
(its `INFO`). Everything that says where a dataset comes from or under which license it is
distributed is generated from that. See `docs/source/design/single_source.rst`.

## Development setup

### Requirements

- [uv](https://docs.astral.sh/uv/). It also installs the Python versions that are missing, so
  you do not have to install Python 3.12, 3.13 and 3.14 yourself to run the whole Nox matrix.
  Run a single version if you prefer, for example `nox -s tests-3.13`.

### Dependency groups

The development tools are **dependency groups** ([PEP 735](https://peps.python.org/pep-0735/))
in `pyproject.toml`, not extras. They are not part of the published package: `pip install
pyml-datasets` installs NumPy and nothing else. `uv.lock` pins the exact version of every
package of every group.

| Group           |                      Purpose                       |
|:----------------|:--------------------------------------------------:|
| `dev-test`      |           pytest, pytest-sugar, pytest-cov         |
| `dev-lint`      |                        ruff                        |
| `dev-types`     |                        mypy                        |
| `dev-docstring` |                     interrogate                    |
| `dev-package`   |                  build (the wheel)                 |
| `dev`           | all `dev-*` groups, scikit-learn and ucimlrepo     |
| `docs-lint`     |            doc8, rstcheck, sphinx-lint             |
| `docs-build`    |           Sphinx, its theme and extensions         |
| `docs`          |             `docs-lint` and `docs-build`           |
| `docs-live`     |       `docs-build` and sphinx-autobuild            |
| `nox`           |                  Nox, to run sessions              |

scikit-learn and ucimlrepo are needed only to rebuild data files, never to use the package.

`uv sync` installs the `dev` group by default. Add or replace groups with flags:

```bash
uv sync --locked                      # the project and the dev group
uv sync --locked --group docs         # add one more group
uv sync --locked --all-groups         # every group
uv sync --locked --only-group nox     # only one group, without the project
```

`uv sync` makes `.venv` match the groups you ask for exactly, so it also **removes** the
packages of the groups you did not name. `--locked` makes uv fail instead of changing
`uv.lock` when it is out of date. Without it, `uv sync` and `uv run` update the lock file
silently.

### Dependencies and the lock file

`uv.lock` is committed, so everyone, and the CI, installs the same versions. `pyproject.toml`
holds the lower bounds (`pytest>=8.0`), `uv.lock` holds the exact versions.

```bash
uv add --group dev-test pytest-xdist   # add a tool to a group and update the lock
uv remove --group dev-test pytest-xdist
uv lock                                # re-resolve after editing pyproject.toml by hand
uv lock --check                        # is uv.lock up to date? (writes nothing)
uv lock --upgrade                      # move every package to the newest allowed version
uv lock --upgrade-package ruff         # move one package only
```

Commit `uv.lock` together with the `pyproject.toml` change. The CI uses `--locked`, so a
forgotten `uv lock` turns the checks red. After an upgrade, run `nox` before you commit: a new
version can bring new lint rules or warnings (pytest runs with `filterwarnings = ["error"]`).

Two things are outside the lock: the `[build-system]` requirement (`setuptools`), which
is installed in an isolated build environment, and the Python version itself.

To see the documentation while you edit it:

```bash
uv run --group docs-live sphinx-autobuild docs/source docs/build/html
```

## Nox sessions

Every session installs its own environment from `uv.lock` (`uv sync --locked`) and only the
groups it needs.

| Session      |      Python      | Groups                          |                          What it runs                          |
|:-------------|:----------------:|:--------------------------------|:--------------------------------------------------------------:|
| `lint`       |       3.13       | `dev-lint`                      |               ruff check and ruff format --check               |
| `types`      |       3.13       | `dev-types`, `dev-test`         |        mypy (strict) on `pyml_datasets`, `scripts`, `tests`    |
| `docstrings` |       3.13       | `dev-docstring`, `dev-test`     |  interrogate (100% coverage) and the doctests of the package   |
| `legal`      |       3.13       | `dev`                           |        `scripts.check_legal` and `scripts.generate --check`    |
| `tests`      | 3.12, 3.13, 3.14 | `dev-test`                      |                             pytest                             |
| `tests-min`  |       3.12       | `dev-test`                      |  pytest with the oldest supported NumPy installed on top       |
| `docs`       |       3.13       | `docs`                          |        sphinx-lint, doc8, rstcheck, `sphinx-build -W`          |
| `linkcheck`  |       3.13       | `docs-build`                    |        Sphinx linkcheck, validity of every link in the docs    |
| `package`    |       3.13       | `dev-package`                   | builds the wheel, checks its contents, imports an installed copy |

`nox` without arguments runs every session except `linkcheck`, which needs the network and is
slow.

```bash
uv run --locked --only-group nox nox -l                    # list all sessions
uv run --locked --only-group nox nox -s lint               # run one session
uv run --locked --only-group nox nox -s tests-3.13         # one session on one Python version
uv run --locked --only-group nox nox -s tests -- -k penguins   # arguments after -- go to pytest
uv run --locked --only-group nox nox -R                    # reuse the existing environments
```

If `nox` is already available in your shell (for example after `uv sync --group nox`), you
can drop the `uv run --locked --only-group nox` prefix and type `nox -s lint`.

## Continuous integration

Every workflow installs uv (`astral-sh/setup-uv`, with the cache keyed on `uv.lock`) and calls
Nox, so a failure in the CI is reproduced locally with the same command:
`uv run --locked --only-group nox nox -s <session>`.

| Workflow        | Runs on                     | Nox sessions                                            |
|:----------------|:----------------------------|:--------------------------------------------------------|
| `quality.yml`   | push, pull request          | `lint`, `types`, `docstrings`, `legal`, `package`       |
| `tests.yml`     | push, pull request          | `tests` on 3.12, 3.13, 3.14 (and 3.13 on Windows), `tests-min` |
| `docs.yml`      | push, pull request          | `docs`                                                  |
| `linkcheck.yml` | weekly schedule, manual run | `linkcheck`                                             |

"Push" means a push to `main` or `dev`, and a pull request means one that targets `main`.

## Conventions

### Code

- Public names are importable from `pyml_datasets`: `load_<name>`, `load_dataset`,
  `get_info`, `list_datasets`, `Dataset`, `DatasetInfo`. The import block and `__all__` are
  generated, do not edit the parts between the `<generated:...>` markers.
- Everything is checked by mypy in strict mode, ruff (line length 100) and interrogate
  (100% docstring coverage, private members and scripts included).
- Data files are read with `allow_pickle=False`. Never store an object array.
- A recipe either downloads only from `https` addresses and pins the SHA-256 of the file,
  or reads a UCI dataset with `ucimlrepo` and checks its shape, dtypes and target values.
  A recipe does not import pandas.

### Docstrings

- NumPy style. The docstring explains the behavior and does not repeat the code.
- Examples are doctests. They run in the `docstrings` session, so they must stay correct.

### Tests

- `tests/` is organised by concern, not by file: `test_loader` (the reader), `test_registry`,
  `test_contract` (rules for every dataset), `test_facts` (compare with `tests/expected`),
  `test_integrity` (manifest, stored provenance), `test_missing_values`, `test_legal`,
  `test_info` and `test_scripts`. Tests that must hold for every dataset use the `name`
  fixture and run once per dataset, so a new dataset is tested without writing a test.
- `tests/expected/<name>.py` holds facts taken from the **documentation of the source**
  (shape, class counts, published means), never copied from the file under test.
- A warning is a failure (`filterwarnings = ["error"]`). Fix its cause, or filter that one
  warning in `pyproject.toml` with a comment that says why.

### Dependencies

- A development tool goes into a group of `[dependency-groups]`, never into
  `[project] dependencies`, which is what the users of the package install.
- Every change of `pyproject.toml` dependencies is followed by `uv lock`, and `uv.lock` is
  committed in the same commit.
- A new Nox session installs only the groups it needs with `_sync(session, "--group", ...)`.

### Commits and versions

- Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
- Work happens on `dev`. `main` receives a pull request from `dev`, and it is merged only when
  all checks pass.
- `__version__` in `pyml_datasets/__init__.py` is the single source of truth. Adding a dataset
  is a MINOR bump, removing one or changing the data format is a breaking change.
- Every release gets an entry in `docs/source/changelog.rst`.

## Dataset admission policy

This is the most important section. A dataset is bundled **only if** its source explicitly
states one of:

- **CC0 1.0** (`CC0-1.0`), or
- **CC BY 4.0** (`CC-BY-4.0`).

Not accepted, however famous the dataset is:

- no license stated, or a license that cannot be found,
- non-commercial (NC), share-alike (SA), no-derivatives (ND), GPL-style licenses,
- "free for educational/research use" and similar statements: they are not licenses,
- an unclear origin: a copy on a forum, a competition, a book CD, a blog,
- a dataset that is a copy of a bigger one whose license is unknown.

Rules for a dataset that is accepted:

1. **Read the license at the original source** (not a mirror, not a library that bundles it),
   and write down where in `legal/evidence/<name>.md`: the license, the address of the page,
   the date, who checked it and an archived copy of the page (Wayback Machine). The
   maintainer re-reads it in a browser and writes the date in `Maintainer check`.
2. **Credit and changes.** CC BY requires credit and a statement of changes. `creators`,
   `citation` and `changes` in `INFO` are that statement, and they end up in the notice, the
   docs and the data file. Cite the way the source asks, and list *every* change, also the
   boring ones (dtype, label shift, dropped column, categorical coding).
3. **Do not hide where the bytes came from.** `obtained_from` names the exact file or the
   library the recipe reads. If it is a copy in a library (for example scikit-learn), say so;
   the license is still the one of the original source.
4. **Do not change the data to fit.** Missing values stay as `NaN`, repeated rows stay.
   Values that the source does not document stay as they are, describe them in `notes`.
5. **Check for extra terms.** Some CC0/CC BY data packages add a request on top (a data use
   policy, a citation request). Put it in `notes`.

If a license changes, or somebody tells me it is wrong, the dataset is removed from the next
version immediately and the history is cleaned if asked. Contact: juraevsherzod9943@gmail.com.

## Adding a dataset

Example: adding `seeds`. You can do every step with the tools; you edit only the lines
marked `TODO`. The commands run in the project environment, so `uv run` comes before them
(the `dev` group has everything they need).

**1. Decide it is allowed.** Read the [policy](#dataset-admission-policy). If the license
page is not clear, stop here.

**2. Scaffold.**

```bash
uv run python -m scripts.new_dataset seeds --license CC-BY-4.0 --task classification
```

This creates five files and refuses to overwrite anything:

| File                                | What goes into it                                         |
|:------------------------------------|:----------------------------------------------------------|
| `pyml_datasets/datasets/seeds.py`   | `INFO` (provenance, license) and `load_seeds()`           |
| `scripts/recipes/seeds.py`          | `build()`: how to get the arrays, returns `Built`         |
| `tests/expected/seeds.py`           | Facts from the source: shape, class counts, means         |
| `docs/source/datasets/seeds.rst`    | Prose for students: features, target, example             |
| `legal/evidence/seeds.md`           | Where and when the license was read                       |

**3. Fill in `INFO`.** Every field is validated when the module is imported: the license
must be allowed, URLs must be `https`, the DOI must look like a DOI, creators and changes
must not be empty. Set `has_missing=True` if the data has `NaN`, and `categorical={...}` for
categorical features (feature name -> names of the categories, in code order).

**4. Write the recipe.** `build()` returns a `Built` with `X`, `y`, `feature_names`, and
optionally `target_names` and `extras`. A recipe gets the arrays in one of two ways. For a
file on the internet use `scripts.recipes._sources.download(url, sha256)`; it accepts only
`https` and checks the digest. For a UCI dataset use `ucimlrepo` (`fetch_ucirepo(id=...)`,
see `scripts/recipes/credit_card_default.py`): check the shape, the dtypes, the target
values and the variable descriptions, and save `ucimlrepo_version` in `extras`. Do not
import pandas in a recipe, use the methods of the frames that `ucimlrepo` returns. Missing
values become `NaN`, categories become integer codes. Values that the source does not
document stay as they are and are described in `notes`. Check the shape and the values you
expect, so a silent change at the source is noticed. A recipe knows nothing about licenses.

**5. Build the data file and generate.**

```bash
uv run python -m scripts.build_datasets seeds
uv run python -m scripts.generate
```

The first command combines the recipe and `INFO`, validates the arrays and saves
`pyml_datasets/data/seeds.npz`. The second updates the registry (`ENTRIES`), the exports,
`NOTICE.md`, the README table, the toctree of the datasets index, the other documentation
includes and `MANIFEST.json`. Never edit those by hand; `generate --check` fails if you do.
Running `generate` again changes nothing when nothing changed.

**6. Fill in the facts and the evidence.** Write `tests/expected/seeds.py` from the source
documentation. A fact that is not on the page of the source (for example class counts) is
checked against the original file, and where it comes from is noted in a comment. Then write
the documentation page (`generate` adds it to the toctree) and `legal/evidence/seeds.md`,
and finish the evidence: open the license page in a browser, save it to the Wayback Machine,
put the link in `Archive` and your name and the date in `Maintainer check`. `check_legal`
warns until you do.

**7. Check everything.**

```bash
uv run python -m scripts.check_legal    # fails on TODO, missing evidence, license mismatch
uv run --locked --only-group nox nox    # lint, types, docstrings, legal, tests, docs, package
```

You do not write tests for a normal dataset: the contract, integrity, missing-value and
legal tests run for it automatically. Add a test only for something special about it.

### Extending in other directions

| I want to...                           | Where                                                                  |
|:---------------------------------------|:-----------------------------------------------------------------------|
| allow another license                  | Do not, without a long think. `LICENSE_IDS` in `pyml_datasets/_types.py`, add `LICENSES/<id>.txt`, `pyproject.toml` license expression, `_LICENSE_NAMES` in `scripts/_render.py`, `new_dataset.py` and the policy above |
| add a field that every dataset has     | `DatasetInfo` in `_types.py`, then `scripts/_render.py` to show it, then regenerate and rebuild (the `meta` array changes) |
| change the file format                 | Bump `_FORMAT_VERSION` in `_loader.py` and `FORMAT_VERSION` in `scripts/_npz.py`, rebuild everything, write the change in the changelog |
| add a new kind of task (e.g. clustering) | `TASKS` in `_types.py`, the dtype rules in `scripts/_npz.py`, the checks in `validate`, the loader doc |
| add a new generated file               | A function in `scripts/_render.py`, and one line in `expected_files()` of `scripts/generate.py` |
| add a legal rule                       | `scripts/check_legal.py` and a test in `tests/test_legal.py`           |
| add a development tool                 | A group in `[dependency-groups]`, `uv lock`, then `_sync(session, "--group", ...)` in `noxfile.py` |
| rebuild a data file                    | `uv run python -m scripts.build_datasets NAME --overwrite`, then `generate`; compare the new manifest digest with the old one |

## Removing a dataset

Delete its module, recipe, data file, expected facts, documentation page and evidence file,
run `uv run python -m scripts.generate`, add a "Removed" entry to the changelog and bump the
version. If the reason is legal, also purge the files from the git history
(`git filter-repo --invert-paths --path pyml_datasets/data/NAME.npz ...`) and replace the
affected tags and releases.

## Releasing

1. Run `nox` on `dev`, and make sure the CI is green. Read the warnings of
   `uv run python -m scripts.check_legal`. Check that `uv lock --check` passes.
2. Bump `__version__` in `pyml_datasets/__init__.py` and add the entry to
   `docs/source/changelog.rst`.
3. Open a pull request from `dev` to `main` and merge it when the CI is green.
4. Create the tag `vX.Y.Z` on `main` and a GitHub release titled `vX.Y.Z`.
5. Check that the Read the Docs build is green.
