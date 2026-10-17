Iris
====

Measurements of 150 iris flowers from three species, 50 flowers each. It is one of the
earliest datasets used to evaluate classification methods and a common first test for a new
classifier. One class is linearly separable from the other two, which are not linearly
separable from each other.

Overview
--------

.. include:: /_generated/iris_overview.inc

Features
--------

``sepal length (cm)``, ``sepal width (cm)``, ``petal length (cm)`` and ``petal width (cm)``.

Target
------

``y`` holds the species of each flower as an integer label. The classes are perfectly
balanced, with 50 samples each.

.. include:: /_generated/iris_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_iris
   >>> data = load_iris()
   >>> data.X.shape, data.y.shape
   ((150, 4), (150,))
   >>> data.target_names
   ('setosa', 'versicolor', 'virginica')
   >>> np.bincount(data.y)
   array([50, 50, 50])
