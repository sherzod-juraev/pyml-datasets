Changelog
=========

0.8.0
-----

Added
~~~~~

- Dataset ``energy_efficiency`` (UCI Energy Efficiency, CC BY 4.0): heating load and cooling
  load of 768 simulated buildings, predicted from eight building parameters. It is the first
  dataset with two targets: ``y`` has the shape ``(768, 2)`` and the names of its columns are
  in ``Dataset.target_names``.

0.7.0
-----

Added
~~~~~

- Dataset ``abalone`` (UCI Abalone, CC BY 4.0): physical measurements of 4177 abalones, one
  categorical feature (the sex) and the number of rings of the shell as a regression target.
  The source scaled the continuous values by dividing by 200, see the page of the dataset.

0.6.0
-----

Added
~~~~~

- Dataset ``concrete_strength`` (Concrete Compressive Strength, CC BY 4.0): compressive
  strength in MPa of 1030 concrete samples, eight numeric features (seven ingredients and the
  age) and a regression target. There are no missing values.

Changed
~~~~~~~

- The expected facts of the tests can state a larger tolerance for the published means of a
  dataset.

0.5.0
-----

Added
~~~~~

- Dataset ``auto_mpg`` (Auto MPG, CC BY 4.0): city-cycle fuel consumption in miles per gallon
  of 398 cars, 7 numeric features and a regression target. 6 values of ``horsepower`` are
  missing and stored as ``NaN``. The identifier ``car_name`` is not stored, and ``origin`` has
  no category names because the source does not give them.

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
