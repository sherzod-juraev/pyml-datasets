Breast Cancer Wisconsin (Diagnostic)
====================================

Features computed from digitized images of fine needle aspirates (FNA) of breast masses. They
describe the characteristics of the cell nuclei present in each image. The task is to predict
whether a mass is malignant or benign.

Overview
--------

.. include:: /_generated/breast_cancer_overview.inc

Features
--------

30 real-valued features: the mean, the standard error and the worst value of ten
measurements of the cell nuclei, such as radius, texture, perimeter and area. The patient
identifier of the original file is not included.

Target
------

``y`` is 0 for malignant and 1 for benign. There are 212 malignant and 357 benign samples.

.. include:: /_generated/breast_cancer_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_breast_cancer
   >>> data = load_breast_cancer()
   >>> data.X.shape
   (569, 30)
   >>> data.target_names
   ('malignant', 'benign')
   >>> np.bincount(data.y)
   array([212, 357])
