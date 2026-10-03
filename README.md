<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/branding/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/branding/logo.svg">
    <img alt="pyml-datasets" src="assets/branding/logo.svg" width="420">
  </picture>
</p>

[![Tests](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/tests.yml/badge.svg)](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/tests.yml)
[![Docs](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/docs.yml/badge.svg)](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/docs.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-yellow.svg)](LICENSE)
[![Data: per dataset](https://img.shields.io/badge/data-per%20dataset-lightgrey.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/Ruff-enabled-brightgreen)](https://docs.astral.sh/ruff/)
[![mypy: strict](https://img.shields.io/badge/mypy-strict-blue.svg)](https://mypy.readthedocs.io/)
[![Interrogate](https://img.shields.io/badge/Interrogate-100%25-brightgreen)](https://interrogate.readthedocs.io/)

Classic tabular datasets for machine learning, stored as NumPy `.npz`
files and loaded with a single function call.

## Quick example

```python
from pyml_datasets import load_wine
X, y = load_wine()
print(X.shape, y.shape)  # (178, 13) (178,)
```

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
│   └── _loader.py
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
authors and keep the terms of their original sources:

| Dataset                                          |                                               License                                               |
|:-------------------------------------------------|:---------------------------------------------------------------------------------------------------:|
| Iris, Wine, Breast Cancer Wisconsin (Diagnostic) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), from the UCI Machine Learning Repository |
| Diabetes, Linnerud, California Housing           |                                  Not stated by the original source                                  |

Citations and attribution requirements are on the dataset pages of the documentation.
   