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
     - Description text of the dataset, taken from the source. Required.
   * - ``target_names``
     - Class or target names. Optional, absent for datasets without them.
   * - ``sklearn_version``
     - Version of scikit-learn that produced the file. Informational, the loader ignores it.

If a required key is missing, the loader raises a ``ValueError`` that names the dataset and
the missing keys. If the file itself is missing from the installed package, it raises a
``FileNotFoundError``.

Rebuilding the files
--------------------

The files are generated from scikit-learn by ``scripts/build_datasets.py`` in the repository.
The script needs the ``dev`` extra (scikit-learn) and, for California Housing, an internet
connection on the first run, because scikit-learn downloads that dataset.

.. code-block:: console

   $ python scripts/build_datasets.py
   $ python scripts/build_datasets.py iris wine --overwrite

Existing files are skipped unless ``--overwrite`` is given. ``.npz`` files are not
byte-for-byte reproducible, so every rebuild would add a new binary blob to the git history.
Before saving a file the script checks that ``X`` is a finite 2D matrix and that ``y`` and
``feature_names`` match its shape.

Adding a dataset
----------------

1. Check the license of the dataset and note its source and citation.
2. Add a recipe to ``_SPECS`` in ``scripts/build_datasets.py`` and build the file.
3. Add a ``load_<name>`` function to ``pyml_datasets/_loader.py`` and export it from
   ``pyml_datasets/__init__.py``.
4. Add the dataset to the expectations table in ``tests/test_datasets.py``.
5. Add a page under ``docs/source/datasets/`` and a row in the license table.

A dataset that does not come from scikit-learn needs its own recipe that returns an object
with ``data``, ``target``, ``feature_names`` and ``DESCR`` attributes, because the build
script converts that object into the arrays above.
