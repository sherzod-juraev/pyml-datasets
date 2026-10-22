Data format
===========

Each dataset is stored in ``pyml_datasets/data/<name>.npz``, a compressed NumPy archive.
The loader reads it with ``allow_pickle=False``, so an archive can never execute code
when it is opened. The current format is version 2.

Contents of a file
------------------

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Key
     - Content
   * - ``X``
     - 2D ``float64`` data matrix. Required. Missing values are ``NaN``.
   * - ``y``
     - Targets: ``int64`` labels ``0 .. n_classes - 1`` for classification, ``float64``
       values for regression. Required, and never ``NaN``.
   * - ``feature_names``
     - One string per column of ``X``. Required.
   * - ``description``
     - Description text with the source, citation, license and changes. Required. It is
       generated from the information of the dataset.
   * - ``format_version``
     - The integer ``2``. Required. A file with another version is refused.
   * - ``meta``
     - The ``DatasetInfo`` of the dataset as JSON. Required, so a file carries its own
       provenance and license.
   * - ``target_names``
     - Class or target names. Optional.
   * - ``build``
     - Informational JSON written by the recipe, for example the version of the library the
       data came from or the SHA-256 digest of the downloaded file. The loader ignores it.

If a required key is missing, the loader raises a ``ValueError`` that names the dataset and
the missing keys. If the file itself is missing from the installed package, it raises a
``FileNotFoundError``.

Missing values and categorical features
---------------------------------------

Missing values are stored as ``NaN`` in ``X``. ``DatasetInfo.has_missing`` says whether a
dataset has any, and the build script refuses a file whose ``NaN`` do not match the flag.
Categorical features are stored as integer codes in ``X`` (still ``float64``, so a missing
category is ``NaN``). The names of the categories are in ``DatasetInfo.categorical``: the code
is the index of the name. ``Dataset.categorical_features`` gives the column indices.
The pyml-datasets package does not impute or encode anything, that is left to you.

Rebuilding the files
--------------------

The files are generated from the original sources by the scripts in ``scripts/``. Each
dataset has a recipe in ``scripts/recipes/`` that fetches the data and returns it as a
``Built`` object, and the provenance in ``pyml_datasets/datasets/<name>.py``. The ``dev``
dependency group, which ``uv sync`` installs, contains the packages the recipes need, and
recipes that download data need an internet connection. Run the commands from the repository
root:

.. code-block:: console

   $ uv run python -m scripts.build_datasets
   $ uv run python -m scripts.build_datasets iris wine --overwrite
   $ uv run python -m scripts.generate

Existing files are skipped unless ``--overwrite`` is given. ``.npz`` files are not
byte-for-byte reproducible, so every rebuild would add a new binary file to the git history.
That is why ``pyml_datasets/data/MANIFEST.json`` stores a digest of the arrays (not of the
file), and why a test compares every file with it. Before saving, the script checks that
``X`` is a finite 2D matrix without unexpected ``NaN``, that ``y`` and ``feature_names``
match it, that class labels are ``0 .. n_classes - 1`` and that categorical codes are valid.

Adding a dataset
----------------

The steps are in ``CONTRIBUTING.md``, section *Adding a dataset*. In short:
``uv run python -m scripts.new_dataset`` creates the files, you fill in the facts, build the
file and run ``uv run python -m scripts.generate``, then the Nox sessions.
