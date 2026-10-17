Wine
====

Results of a chemical analysis of wines grown in the same region of Italy but derived from
three different cultivars. The analysis measured 13 constituents in each wine. The classes
are well separated, which makes it a good dataset for a first test of a new classifier.

Overview
--------

.. include:: /_generated/wine_overview.inc

Features
--------

13 chemical measurements such as ``alcohol``, ``malic_acid``, ``ash`` and ``proline``. The
features have very different scales, so the dataset is a good place to try feature scaling.

Target
------

``y`` holds the cultivar as an integer label 0, 1 or 2. The UCI file numbers the cultivars
1 to 3, the labels here are shifted by one. The classes have 59, 71 and 48 samples.

.. include:: /_generated/wine_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_wine
   >>> data = load_wine()
   >>> data.X.shape
   (178, 13)
   >>> np.bincount(data.y)
   array([59, 71, 48])
