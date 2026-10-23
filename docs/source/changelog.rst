Changelog
=========

0.4.0
-----

Added
~~~~~

- Dataset ``bank_marketing`` (CC BY 4.0).

Changed
~~~~~~~

- The legal check is stricter. A dataset needs an archived copy of its license page and the
  confirmation of the maintainer in its evidence file. Before, a missing archive or a pending
  confirmation was only a warning, now it fails the check and the CI.
- The generated ``pyml_datasets/datasets/__init__.py`` keeps the form that ``ruff format``
  produces, so ``generate --check`` and the linter agree for any number of datasets.

0.3.1
-----

Fixed
~~~~~

- Dataset ``penguins``: the creators are now the authors of the cited package, as in the
  citation and the DOI. The source link and the recipe now use the tag ``v0.1.0`` of the
  package repository instead of the ``main`` branch. The data did not change.

Changed
~~~~~~~

- The license evidence of every dataset now contains a Wayback Machine copy of the license
  page and the confirmation of the maintainer.

0.3.0
-----

Added
~~~~~

- Dataset ``credit_card_default`` (Default of Credit Card Clients, CC BY 4.0): 30000 clients
  in Taiwan, 23 integer features and a binary target. The values are stored as released,
  including the codes that the source does not document, see the page of the dataset.

Changed
~~~~~~~

- The toctree of the datasets index is generated.

0.2.0
-----

A restructuring release with one **breaking** change in the contents.

Breaking changes
~~~~~~~~~~~~~~~~

- **Removed** ``load_diabetes``, ``load_linnerud`` and ``load_california_housing``. The
  redistribution terms of their sources could not be confirmed, and only datasets with an
  explicit CC0 1.0 or CC BY 4.0 license are bundled now. The data files and their
  documentation pages are removed.
- **Data format 2.** Files carry ``format_version`` and ``meta`` and cannot be read by 0.1.0.
- ``Dataset`` has a new required field ``info``.

Added
~~~~~

- ``DatasetInfo``, ``get_info``, ``list_datasets`` and ``load_dataset``: the license,
  source, DOI, creators, citation and changes of every dataset, available without reading the
  data.
- Missing values (``NaN``) and categorical features, with ``Dataset.has_missing`` and
  ``Dataset.categorical_features``.
- Datasets ``digits`` (CC BY 4.0) and ``penguins`` (CC0 1.0).
- ``NOTICE.md`` and ``LICENSES/CC0-1.0.txt`` in the package, a license expression in the
  package metadata, evidence files in ``legal/evidence/``.
- ``scripts.generate``, ``scripts.check_legal`` and ``scripts.new_dataset``, and a ``legal``
  Nox session and CI job.

Changed
~~~~~~~

- Loaders are one module per dataset in ``pyml_datasets/datasets/``.
- Provenance is written once and the documentation, ``NOTICE.md``, the README table and the
  manifest are generated from it.
- Tests are organised by concern and compare every file with independent facts.
- Citation years of Wine (1992) and Breast Cancer (1993) follow the UCI pages.
- Iris, Wine, Breast Cancer and Digits are described as obtained from scikit-learn's copies
  of the UCI data.

0.1.0
-----

First release.
