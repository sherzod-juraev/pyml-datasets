Iris
====

Measurements of 150 iris flowers from three species, 50 flowers each. It is one of the
earliest datasets used to evaluate classification methods and a common first test for a new
classifier. One class is linearly separable from the other two, which are not linearly
separable from each other.

Overview
--------

.. list-table::
   :widths: 25 75

   * - Loader
     - ``load_iris()``
   * - Task
     - Classification
   * - Samples
     - 150
   * - Features
     - 4, all real-valued
   * - Targets
     - 3 classes: ``setosa`` (0), ``versicolor`` (1), ``virginica`` (2)

Features
--------

``sepal length (cm)``, ``sepal width (cm)``, ``petal length (cm)`` and ``petal width (cm)``.

Target
------

``y`` holds the species of each flower as an integer label. The classes are perfectly
balanced, with 50 samples each.

Source and citation
-------------------

The data comes from R. A. Fisher's 1936 paper and is distributed by the UCI Machine Learning
Repository.

* Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems.
  *Annals of Eugenics*, 7(2), 179-188.
* Fisher, R. A. (1936). Iris [Dataset]. UCI Machine Learning Repository.
  https://archive.ics.uci.edu/dataset/53/iris

License
-------

CC BY 4.0, as stated by the UCI Machine Learning Repository. See :doc:`../license`.

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_iris
   >>> data = load_iris()
   >>> data.X.shape, data.y.shape
   ((150, 4), (150,))
   >>> data.feature_names
   ('sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)')
   >>> data.target_names
   ('setosa', 'versicolor', 'virginica')
   >>> np.bincount(data.y)
   array([50, 50, 50])
