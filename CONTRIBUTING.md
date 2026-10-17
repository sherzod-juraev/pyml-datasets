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
├── .github/workflows/          # CI workflows, each one calls Nox
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
├── pyproject.toml              # Project metadata and tool config
└── README.md                   # Project overview
```

The idea behind the layout: **a dataset is described once**, in `pyml_datasets/datasets/<name>.py`
(its `INFO`). Everything that says where a dataset comes from or under which license it is
distributed is generated from that. See `docs/source/design/single_source.rst`.

## Development setup

### Requirements

- Python 3.12, 3.13 and 3.14. Install all three to run the whole Nox matrix, or run a single
  version, for example `nox -s tests-3.13`.

### Optional extras

| Extra  |                           Purpose                            |
|:-------|:------------------------------------------------------------:|
| `nox`  |                      Nox, to run sessions                    |
| `dev`  | mypy, ruff, pytest, interrogate, scikit-learn, ucimlrepo     |
| `docs` |                Sphinx and documentation tools                |
| `all`  |                      Everything above                        |

scikit-learn and ucimlrepo are needed only to rebuild data files, never to use the package.

## Nox sessions

| Session      |      Python      |                          What it runs                          |
|:-------------|:----------------:|:--------------------------------------------------------------:|
| `lint`       |       3.13       |               ruff check and ruff format --check               |
| `types`      |       3.13       |        mypy (strict) on `pyml_datasets`, `scripts`, `tests`    |
| `docstrings` |       3.13       |  interrogate (100% coverage) and the doctests of the package   |
| `legal`      |       3.13       |        `scripts.check_legal` and `scripts.generate --check`    |
| `tests`      | 3.12, 3.13, 3.14 |                             pytest                             |
| `tests-min`  |       3.12       |            pytest with the oldest supported NumPy              |
| `docs`       |       3.13       |        sphinx-lint, doc8, rstcheck, `sphinx-build -W`          |
| `linkcheck`  |       3.13       |        Sphinx linkcheck, validity of every link in the docs    |
| `package`    |       3.13       | builds the wheel, checks its contents, imports an installed copy |

`nox` without arguments runs every session except `linkcheck`, which needs the network and is
slow.

```bash
nox -l                          # list all sessions
nox -s lint                     # run one session
nox -s tests-3.13               # run one session on one Python version
nox -s tests -- -k penguins     # arguments after -- are passed to pytest
nox -R                          # reuse the existing virtual environments, much faster
```

## Continuous integration

Every workflow calls Nox, so a failure in the CI is reproduced locally with the same command.

| Workflow        | Runs on                     | Nox sessions                                            |
|:----------------|:----------------------------|:--------------------------------------------------------|
| `quality.yml`   | push, pull request          | `lint`, `types`, `docstrings`, `legal`, `package`       |
| `tests.yml`     | push, pull request          | `tests` on 3.12, 3.13, 3.14 (and 3.13 on Windows)       |
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
- A recipe downloads only from `https` addresses and pins the SHA-256 of the file.

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

### Commits and versions

- Commits follow [Conventional Commits](https://www.conventionalcommits.org/).
- Work happens on `dev`. `main` receives a merge only when all checks pass.
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
5. **Check for extra terms.** Some CC0/CC BY data packages add a request on top (a data use
   policy, a citation request). Put it in `notes`.

If a license changes, or somebody tells me it is wrong, the dataset is removed from the next
version immediately and the history is cleaned if asked. Contact: juraevsherzod9943@gmail.com.

## Adding a dataset

Example: adding `seeds`. You can do every step with the tools; you edit only the lines
marked `TODO`.

**1. Decide it is allowed.** Read the [policy](#dataset-admission-policy). If the license
page is not clear, stop here.

**2. Scaffold.**

```bash
python -m scripts.new_dataset seeds --license CC-BY-4.0 --task classification
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
optionally `target_names` and `extras`. Use `scripts.recipes._sources.download(url, sha256)`
for files from the internet; it accepts only `https` and checks the digest. Missing values
become `NaN`, categories become integer codes. Check the shape and the values you expect, so a
silent change at the source is noticed. A recipe knows nothing about licenses.

**5. Build the data file and generate.**

```bash
python -m scripts.build_datasets seeds
python -m scripts.generate
```

The first command combines the recipe and `INFO`, validates the arrays and saves
`pyml_datasets/data/seeds.npz`. The second updates the registry (`ENTRIES`), the exports,
`NOTICE.md`, the README table, the documentation includes and `MANIFEST.json`. Never edit
those by hand; `generate --check` fails if you do.

**6. Fill in the facts and the evidence.** Write `tests/expected/seeds.py` from the source
documentation, then the documentation page and `legal/evidence/seeds.md`.

**7. Check everything.**

```bash
python -m scripts.check_legal     # fails on TODO, missing evidence, license mismatch
nox                               # lint, types, docstrings, legal, tests, docs, package
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
| rebuild a data file                    | `python -m scripts.build_datasets NAME --overwrite`, then `generate`; compare the new manifest digest with the old one |

## Removing a dataset

Delete its module, recipe, data file, expected facts, documentation page and evidence file,
run `python -m scripts.generate`, add a "Removed" entry to the changelog and bump the
version. If the reason is legal, also purge the files from the git history
(`git filter-repo --invert-paths --path pyml_datasets/data/NAME.npz ...`) and replace the
affected tags and releases.

## Releasing

1. Run `nox` on `dev`, and make sure the CI is green. Read the warnings of
   `python -m scripts.check_legal`.
2. Bump `__version__` in `pyml_datasets/__init__.py` and add the entry to
   `docs/source/changelog.rst`.
3. Merge `dev` into `main` and push.
4. Create the tag `vX.Y.Z` on `main` and a GitHub release titled `vX.Y.Z`.
5. Check that the Read the Docs build is green.
