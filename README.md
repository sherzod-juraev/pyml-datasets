<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/branding/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/branding/logo.svg">
    <img alt="pyml-datasets" src="assets/branding/logo.svg" width="420">
  </picture>
</p>

[![Release](https://img.shields.io/github/v/release/sherzod-juraev/pyml-datasets)](https://github.com/sherzod-juraev/pyml-datasets/releases)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![Code: MIT](https://img.shields.io/badge/code-MIT-yellow.svg)](LICENSE)
[![Data: per dataset](https://img.shields.io/badge/data-per%20dataset-lightgrey.svg)](#license)
[![Tests](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/tests.yml/badge.svg)](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/tests.yml)
[![Quality](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/quality.yml/badge.svg)](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/quality.yml)
[![Docs](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/docs.yml/badge.svg)](https://github.com/sherzod-juraev/pyml-datasets/actions/workflows/docs.yml)
[![Documentation](https://readthedocs.org/projects/pyml-datasets/badge/?version=latest)](https://pyml-datasets.readthedocs.io/en/latest/)
[![Ruff](https://img.shields.io/badge/Ruff-enabled-brightgreen)](https://docs.astral.sh/ruff/)
[![mypy: strict](https://img.shields.io/badge/mypy-strict-blue.svg)](https://mypy.readthedocs.io/)
[![Interrogate](https://img.shields.io/badge/Interrogate-100%25-brightgreen)](https://interrogate.readthedocs.io/)
[![Nox](https://img.shields.io/badge/nox-sessions-blue)](https://nox.thea.codes/)

Classic tabular datasets for machine learning, stored as NumPy `.npz` files and loaded with a
single function call. No downloads at runtime, no network, no pandas: just NumPy arrays.

- **Documentation**: https://pyml-datasets.readthedocs.io
- **Source code**: https://github.com/sherzod-juraev/pyml-datasets
- **Main library**: [pyml](https://github.com/sherzod-juraev/pyml), a from-scratch machine
  learning library that uses these datasets in its examples

## Quick example

Every loader returns a `Dataset` with the features `X` and the targets `y`:

```python
from pyml_datasets import load_wine

X, y = load_wine()
print(X.shape, y.shape)  # (178, 13) (178,)
```

The same object also works without unpacking:

```python
from pyml_datasets import load_iris

data = load_iris()
print(data.X.shape, data.y.shape)  # (150, 4) (150,)
```

Together with [pyml](https://github.com/sherzod-juraev/pyml):

```python
from pyml.model_selection import train_test_split
from pyml.neighbors import KNNClassifier
from pyml_datasets import load_iris

X, y = load_iris()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = KNNClassifier(n_neighbors=5)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))  # accuracy on the test set
```

> [!NOTE]
> Importing `pyml_datasets` does not read any data. A dataset file is read from disk only when
> its `load_*` function is called, so the import stays fast and you only load the datasets you
> use.

## Installation

pyml-datasets is a personal project and is not published on PyPI. It requires Python 3.12 or
newer (NumPy is the only dependency) and is installed directly from GitHub:

```bash
pip install git+https://github.com/sherzod-juraev/pyml-datasets.git
```

To install a fixed release, add its tag after `@`, replacing `vX.Y.Z` with a tag from the
[Releases](https://github.com/sherzod-juraev/pyml-datasets/releases) page:

```bash
pip install git+https://github.com/sherzod-juraev/pyml-datasets.git@vX.Y.Z
```

## What's inside

| Function                  |            Task             |                    Source                    |
|:--------------------------|:---------------------------:|:--------------------------------------------:|
| `load_iris`               |       Classification        |                 scikit-learn                 |
| `load_wine`               |       Classification        |                 scikit-learn                 |
| `load_breast_cancer`      |       Classification        |                 scikit-learn                 |
| `load_diabetes`           |         Regression          |                 scikit-learn                 |
| `load_california_housing` |         Regression          |                 scikit-learn                 |
| `load_linnerud`           |  Multi-output regression    |                 scikit-learn                 |
| `load_wine_quality`       | Regression / classification |           UCI Machine Learning Repository    |

The license, the source and the citation of every dataset are listed in the
[documentation](https://pyml-datasets.readthedocs.io/en/latest/datasets/index.html#datasets).

## Documentation

- [Datasets](https://pyml-datasets.readthedocs.io/en/latest/datasets/index.html#datasets)
- [License](https://pyml-datasets.readthedocs.io/en/latest/license.html)
- [pyml documentation](https://pyml-edu.readthedocs.io)

## Development

The development setup, the Nox sessions and the project conventions are described in
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

The code is released under the [MIT license](LICENSE). The datasets were created by other
authors and keep the terms of their original sources, so the license differs from dataset to
dataset and some sources do not state one. The license, source and citation of every dataset
are listed in the documentation: [Datasets — pyml-datasets](https://pyml-datasets.readthedocs.io/en/latest/datasets/index.html#datasets)
and [License](https://pyml-datasets.readthedocs.io/en/latest/license.html).
