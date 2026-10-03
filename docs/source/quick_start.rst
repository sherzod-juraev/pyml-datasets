Quick start
===========

Loading a dataset
-----------------

Every dataset has a loader named ``load_<name>``. It returns a
:class:`~pyml_datasets.Dataset`:

.. code-block:: pycon

   >>> from pyml_datasets import load_wine
   >>> data = load_wine()
   >>> data.X.shape
   (178, 13)
   >>> data.y.shape
   (178,)

The same call works for the other loaders: ``load_iris``, ``load_breast_cancer``,
``load_diabetes``, ``load_linnerud`` and ``load_california_housing``. See
:doc:`datasets/index` for what each one contains.

The Dataset object
------------------

.. list-table::
   :header-rows: 1
   :widths: 22 33 45

   * - Attribute
     - Type
     - Meaning
   * - ``X``
     - ``float64`` array, shape ``(n_samples, n_features)``
     - Data matrix.
   * - ``y``
     - ``int64`` array for classification, ``float64`` for regression
     - Targets, shape ``(n_samples,)``, or ``(n_samples, n_targets)`` for multi-output
       datasets.
   * - ``feature_names``
     - tuple of ``str``
     - Names of the columns of ``X``.
   * - ``target_names``
     - tuple of ``str`` or ``None``
     - Class names for classification, target names for multi-output regression, ``None``
       if the source has none.
   * - ``description``
     - ``str``
     - Description of the dataset, including its source.

In classification datasets ``y`` holds integer labels ``0, 1, 2, ...`` that follow
the order of ``target_names``.

Unpacking
---------

A ``Dataset`` yields ``X`` and then ``y`` when iterated, so both styles work:

.. code-block:: pycon

   >>> from pyml_datasets import load_iris
   >>> data = load_iris()
   >>> X, y = load_iris()
   >>> X.shape, y.shape
   ((150, 4), (150,))

Nothing is cached: every call reads the file again and returns new arrays, so changing the
arrays of one result never affects another. The ``Dataset`` object itself is immutable, you
cannot reassign its attributes.

Using a dataset with pyml
-------------------------

.. code-block:: python

   from pyml.model_selection import train_test_split
   from pyml.neighbors import KNNClassifier
   from pyml_datasets import load_iris

   X, y = load_iris()
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

   model = KNNClassifier(n_neighbors=5)
   model.fit(X_train, y_train)
   print(model.score(X_test, y_test))

The loaded feature matrix ``X`` and target array ``y`` are plain NumPy
arrays, so they work with any library that accepts NumPy input.
