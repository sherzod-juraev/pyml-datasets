Breast Cancer Wisconsin (Diagnostic)
====================================

Features computed from digitized images of fine needle aspirates (FNA) of breast masses. They
describe the characteristics of the cell nuclei present in each image. The task is to predict
whether a mass is malignant or benign.

Overview
--------

.. list-table::
   :widths: 25 75

   * - Loader
     - ``load_breast_cancer()``
   * - Task
     - Binary classification
   * - Samples
     - 569
   * - Features
     - 30, all real-valued
   * - Targets
     - 2 classes: ``malignant`` (0), ``benign`` (1)

Features
--------

Ten properties of the cell nuclei are measured in each image: radius, texture, perimeter,
area, smoothness, compactness, concavity, concave points, symmetry and fractal dimension.
For each property the dataset stores three values, which gives 30 features:

* the mean, named like ``mean radius``
* the standard error, named like ``radius error``
* the "worst" (largest) value, named like ``worst radius``

Target
------

``y`` holds the diagnosis as an integer label. Note that ``0`` means malignant and ``1`` means
benign. There are 212 malignant and 357 benign samples, so the classes are imbalanced.

Source and citation
-------------------

The dataset was created by William Wolberg, Olvi Mangasarian and Nick Street at the University
of Wisconsin and is distributed by the UCI Machine Learning Repository.

* Wolberg, W., Mangasarian, O., Street, N., & Street, W. (1995). Breast Cancer Wisconsin
  (Diagnostic) [Dataset]. UCI Machine Learning Repository.
  https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-diagnostic

License
-------

CC BY 4.0, as stated by the UCI Machine Learning Repository. See :doc:`../license`.

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_breast_cancer
   >>> data = load_breast_cancer()
   >>> data.X.shape, data.y.shape
   ((569, 30), (569,))
   >>> data.feature_names[:3]
   ('mean radius', 'mean texture', 'mean perimeter')
   >>> data.target_names
   ('malignant', 'benign')
   >>> np.bincount(data.y)
   array([212, 357])
