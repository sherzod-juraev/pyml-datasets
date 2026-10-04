Data format
===========

Each dataset is stored in ``pyml_datasets/data/<name>.npz``, a compressed NumPy archive.
The loader reads it with ``allow_pickle=False``, so an archive can never execute code
when it is opened.

Contents of a file
------------------

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Key
     - Content
   * - ``X``
     - 2D ``float64`` data matrix. Required.
   * - ``y``
     - Targets: ``int64`` labels for classification, ``float64`` values for regression.
       Required.
   * - ``feature_names``
     - One string per column of ``X``. Required.
   * - ``description``
     - Description text of the dataset, with its source and citation. Required.
   * - ``target_names``
     - Class or target names. Optional, absent for datasets without them.
   * - Other keys
     - Extra metadata written by the recipe, such as ``sklearn_version``,
       ``ucimlrepo_version`` or ``source``. Informational, the loader ignores them.

If a required key is missing, the loader raises a ``ValueError`` that names the dataset and
the missing keys. If the file itself is missing from the installed package, it raises a
``FileNotFoundError``.

Rebuilding the files
--------------------

The files are generated from the original sources by the scripts in ``scripts/``. Each
dataset has a recipe in ``scripts/recipes/`` that fetches the data and returns it as a
``Built`` object. The ``dev`` extra installs the packages the recipes need, and recipes that
download data need an internet connection. Run the commands from the repository root:

.. code-block:: console

   $ python -m scripts.build_datasets
   $ python -m scripts.build_datasets iris wine --overwrite

Existing files are skipped unless ``--overwrite`` is given. ``.npz`` files are not
byte-for-byte reproducible, so every rebuild would add a new binary blob to the git history.
Before saving a file the script checks that ``X`` is a finite 2D matrix and that ``y`` and
``feature_names`` match its shape.

Adding a dataset
----------------

1. Check the license of the dataset and note its source and citation.
2. Add a recipe in ``scripts/recipes/`` with a ``build()`` function that returns a ``Built``
   object, as ``wine_quality.py`` does, make it available to the build script and build
   the file. A recipe that downloads data should check the shape and the values it receives,
   so a silent change on the source side is noticed instead of being saved.
3. Add a module ``pyml_datasets/_<name>.py`` with a ``load_<name>`` function that calls
   ``_load_npz``, and export it from ``pyml_datasets/__init__.py``.
4. Add a test file ``tests/test_<name>.py`` that checks the integrity of the file, and add the
   loader to the list in ``tests/test_init.py``.
5. Add a page under ``docs/source/datasets/``, a row in the datasets index and a row in the
   license table.

A dataset that comes from scikit-learn is added to the existing ``_sklearn.py`` modules and
to ``tests/test_sklearn_datasets.py`` instead of getting new files.

A ``Built`` object holds the data matrix, the targets, the feature names, the optional target
names, the description, the task (``"classification"`` or ``"regression"``, which decides the
dtype of ``y``) and optional extra metadata. The build script converts it into the arrays
described above.
