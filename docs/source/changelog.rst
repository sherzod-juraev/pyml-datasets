Changelog
=========

0.22.0
------

Added
~~~~~

- ``pyml-datasets list`` and ``pyml-datasets show`` take ``--format {text,md,json}``.
  ``text`` is the output as before. ``md`` is Markdown: a table for ``list``, and sections in
  the style of ``NOTICE.md`` for ``show``. ``json`` is for programs: ``list`` gives an array
  of objects and ``show`` gives one object with every fact, whether ``--full`` is given or
  not. The default limit of ``list`` does not cut the JSON, only ``--limit`` does.
- ``--output PATH`` (``-o``) writes the result to a file instead of the terminal, and
  ``--force`` overwrites a file that exists. A file is always written in UTF-8, without a
  byte order mark and with ``\n`` at the end of every line, whatever the console, the locale
  and the platform are, and a character is never replaced. A text file has no colors and no
  links and is wrapped at 100 characters, not at the width of the terminal. Without
  ``--format`` the extension ``.md``, ``.txt`` or ``.json`` chooses the format. The path is
  taken from the current directory, ``~`` is expanded, and its directory must exist. ``-o -``
  is the terminal. ``python -m scripts list`` and ``show`` take the same options.

Changed
~~~~~~~

- ``--format json`` on the terminal writes every character outside ASCII as an escape
  (``\u0131``), so a console with another code page, such as cp1252 on Windows, still gets
  valid JSON. A JSON file keeps the characters, in UTF-8.

0.21.0
------

Added
~~~~~

- Options of ``pyml-datasets list`` that filter and page the rows. ``--name PATTERN`` keeps
  the datasets whose name matches a pattern, like ``ILIKE`` in SQL: ``*`` (or ``%``) stands
  for any characters and ``?`` for one, so ``--name "wine*"`` starts with ``wine`` and
  ``--name "*quality"`` ends with ``quality``. Capital letters do not matter, and a pattern
  without wildcards has to match the whole name; when a wider pattern would find more
  datasets, a line below the table suggests it. ``--missing`` and ``--no-missing`` keep
  the datasets that have, or do not have, missing values. ``--limit N`` shows at most N rows,
  ``--offset N`` skips the first N rows and ``--all`` shows every row. ``python -m scripts
  list`` takes the same options.

Changed
~~~~~~~

- ``pyml-datasets list`` shows at most 25 rows unless ``--limit`` or ``--all`` is given. When
  the table is cut, a line below it says which rows are shown and how many there are, for
  example ``Showing 1-25 of 31.``. The package has fewer than 25 datasets now, so nothing is
  cut yet. The line below the table says ``1 dataset``, not ``1 datasets``. The output is
  meant for people and is not a stable interface.

0.20.0
------

Added
~~~~~

- ``pyml-datasets show NAME --full`` also prints the changes made to the data and the notes.
  ``python -m scripts show`` takes the same option.

Changed
~~~~~~~

- ``pyml-datasets show`` prints sections: the header with the task and the license, then
  *Overview*, *Provenance*, *Features* and *Citation*. Every feature name is listed, the
  numeric and the categorical ones apart, where the lists were cut after ten names. The
  addresses are links in terminals that support links. The changes made to the data and the
  notes moved to ``--full``, and a line below the report says how many there are. The
  output is meant for people and is not a stable interface.

Fixed
~~~~~

- ``pyml-datasets`` no longer fails when the output cannot encode a character, for example
  when it goes through a pipe on Windows, which uses cp1252: ``show combined_cycle_power_plant``
  failed on the letter ``ı`` in the name of a creator. Such a character is now printed as
  ``?``.

0.19.0
------

Added
~~~~~

- Options of ``pyml-datasets list``: ``--task`` shows only the datasets of one task,
  ``--sort`` orders the rows by name, number of samples or number of features, and
  ``--reverse`` reverses the order. Datasets with an equal value stay in the order of their
  names. The line below the table counts the datasets that are shown. ``python -m scripts
  list`` takes the same options.

Changed
~~~~~~~

- The columns ``Task`` and ``License`` of the table are centered. The output is meant for
  people and is not a stable interface.

0.18.0
------

Changed
~~~~~~~

- ``import pyml_datasets`` and ``list_datasets`` no longer import the module of every dataset.
  A ``load_<name>`` function, ``get_info`` and ``load_dataset`` import only the module of the
  dataset they are asked for, so the import time does not grow with the number of datasets.
  ``from pyml_datasets import load_iris``, ``from pyml_datasets import *`` and ``dir()`` work
  as before, and type checkers still report a misspelled loader name.
- ``pyml_datasets.datasets`` holds an index of the dataset names and tasks, ``DATASET_TASKS``,
  in place of ``ENTRIES``. Both are internal.

0.17.0
------

Added
~~~~~

- The ``pyml-datasets`` command, also run as ``python -m pyml_datasets``, with two
  sub-commands. ``list`` prints a table of the datasets with their task, license and shape.
  ``show NAME`` prints the facts about one dataset: its license, source, citation and the
  changes made to the data. The output is meant for people and is not a stable interface.

Changed
~~~~~~~

- ``rich`` and ``rich-argparse`` are now dependencies of the package. They are used only by the
  command and are not imported by ``import pyml_datasets``.

0.16.0
------

Added
~~~~~

- Dataset ``superconductivity`` (UCI Superconductivty Data, CC BY 4.0): 21263 superconductors
  described by 81 numeric features, with the critical temperature as the regression target.
  66 rows of the source repeat another row and are kept, so equal rows can end up in both
  parts of a split.

0.15.0
------

Added
~~~~~

- Dataset ``mushroom`` (UCI Mushroom, CC BY 4.0): 8124 descriptions of hypothetical
  mushrooms from a field guide, with 22 categorical features, to be classified as edible or
  poisonous (48.2 percent are poisonous, and that class also holds mushrooms of unknown
  edibility). Entries of ``stalk_root`` that the source marks as missing are stored as
  ``NaN``.

0.14.0
------

Added
~~~~~

- Dataset ``real_estate_valuation`` (UCI Real Estate Valuation, CC BY 4.0): 414 house sales in
  the Sindian District of New Taipei City, Taiwan, described by 6 numeric features (the
  transaction date, the house age, the distance to the nearest MRT station, the number of
  convenience stores and the latitude and longitude), with the house price of unit area as
  the target. The source says that the data was split randomly into a training and a testing
  part, but its file does not tell which sample belongs to which, so the split is not
  provided.

0.13.0
------

Added
~~~~~

- Dataset ``adult`` (UCI Adult, CC BY 4.0): 48842 people from the 1994 Census database,
  described by 14 features, 8 categorical and 6 whole numbers, to be classified by whether the
  yearly income is above 50K (23.93 percent of the people are). Entries of ``workclass``,
  ``occupation`` and ``native_country`` that the source marks as unknown are stored as ``NaN``.
  The training part of the source (32561 rows) comes first and its test part (16281 rows) last.

0.12.0
------

Added
~~~~~

- Dataset ``forest_fires`` (UCI Forest Fires, CC BY 4.0): 517 forest fires in the northeast
  region of Portugal, with the burned area in hectares predicted from the place on the map of
  the Montesinho park, the month, the day of the week, four indices of the Fire Weather Index
  system and four weather observations. The target is very skewed towards zero. It is stored
  as released, without the logarithm transform that the source suggests.

0.11.0
------

Added
~~~~~

- Dataset ``german_credit`` (UCI Statlog German Credit Data, CC BY 4.0): 1000 credit applicants
  described by 20 attributes, 13 categorical and 7 numeric, to be classified as good or bad
  credit risks. The source requires a cost matrix (a bad customer classified as good costs 5,
  a good customer classified as bad costs 1), which is written in the notes and on the page of
  the dataset. The package does not apply it.

0.10.0
------

Added
~~~~~

- Dataset ``airfoil_self_noise`` (UCI Airfoil Self-Noise, CC BY 4.0): scaled sound pressure
  level of NACA 0012 airfoil blade sections, predicted from five inputs (frequency, angle of
  attack, chord length, free-stream velocity and suction side displacement thickness). 1503
  examples from a series of aerodynamic and acoustic tests in an anechoic wind tunnel.

0.9.0
-----

Added
~~~~~

- Dataset ``combined_cycle_power_plant`` (UCI Combined Cycle Power Plant, CC BY 4.0): net hourly
  electrical energy output of a power plant, predicted from four hourly average ambient
  variables (temperature, exhaust vacuum, ambient pressure and relative humidity). 9568 data
  points, the largest regression dataset of the package.

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
