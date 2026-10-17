Changelog
=========

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
