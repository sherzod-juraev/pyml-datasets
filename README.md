<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/branding/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/branding/logo.svg">
    <img alt="pyml-datasets" src="assets/branding/logo.svg" width="420">
  </picture>
</p>

[![Tests](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/tests.yml/badge.svg)](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/tests.yml)
[![Docs](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/docs.yml/badge.svg)](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/docs.yml)
   [![Documentation](https://readthedocs.org/projects/pyml-datasets/badge/?version=latest)](https://pyml-datasets.readthedocs.io/en/latest/)
[![Code: MIT](https://img.shields.io/badge/code-MIT-yellow.svg)](LICENSE)
[![Data: per dataset](https://img.shields.io/badge/data-per%20dataset-lightgrey.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/Ruff-enabled-brightgreen)](https://docs.astral.sh/ruff/)
[![mypy: strict](https://img.shields.io/badge/mypy-strict-blue.svg)](https://mypy.readthedocs.io/)
[![Interrogate](https://img.shields.io/badge/Interrogate-100%25-brightgreen)](https://interrogate.readthedocs.io/)

Classic tabular datasets for machine learning, stored as NumPy `.npz`
files and loaded with a single function call.

📖 [pyml-datasets.readthedocs.io](https://pyml-datasets.readthedocs.io/en/latest/)

## Quick example

```python
from pyml_datasets import load_wine
X, y = load_wine()
print(X.shape, y.shape)  # (178, 13) (178,)
```

> [!NOTE]
> Importing `pyml_datasets` does not read any data. A dataset file is read from disk only when
> its `load_*` function is called, so the import stays fast and you only load the datasets you
> use.

## Installation

```bash
pip install git+https://github.com/sherzod-juraev/pyml-datasets.git
```

## Project Structure

```text
pyml-datasets/
├── .github/
│   └── workflows/
│       ├── docs.yml
│       ├── docs-linkcheck.yml
│       └── tests.yml
│
├── assets/
│
├── docs/
│
├── LICENSES/
│
├── pyml_datasets/
│   ├── data/
│   ├── _loader.py
│   ├── _sklearn.py
│   └── _wine_quality.py
│
├── scripts/
│
├── tests/
│   ├── test_init.py
│   ├── test_loader.py
│   ├── test_sklearn_datasets.py
│   └── test_wine_quality.py
│
├── .gitignore
├── .readthedocs.yaml
├── pyproject.toml
├── README.md
└── LICENSE
```

## Quality tooling

| Tool                        |               Checks                |
|:----------------------------|:-----------------------------------:|
| mypy (strict)               |        Static type checking         |
| interrogate                 |      Docstring coverage (100%)      |
| ruff                        |       Linting and formatting        |
| pytest                      |             Test suite              |
| sphinx-lint, doc8, rstcheck |   Documentation style and syntax    |
| sphinx linkcheck            | Validity of every link in the docs  |


## License

The code is released under the [MIT license](LICENSE). The datasets were created by other
authors and keep the terms of their original sources, so the license differs from dataset to
dataset and some sources do not state one. The license, source and citation of every dataset
are listed in the documentation: [Datasets — pyml-datasets](https://pyml-datasets.readthedocs.io/en/latest/datasets/index.html#datasets)
and [License](https://pyml-datasets.readthedocs.io/en/latest/license.html).
   