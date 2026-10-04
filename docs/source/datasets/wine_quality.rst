Wine Quality
============

Physicochemical measurements of 6497 red and white vinho verde wines from the north of
Portugal, together with the quality of each wine as a score given by wine tasters. Red and
white wines are stored together and the colour of the wine is not part of the data. The
scores are ordered and unbalanced, so the dataset suits regression as well as ordinal or
multiclass classification.

Overview
--------

.. list-table::
   :widths: 25 75

   * - Loader
     - ``load_wine_quality()``
   * - Task
     - Regression, also usable for classification
   * - Samples
     - 6497 (1599 red and 4898 white wines)
   * - Features
     - 11, all real-valued
   * - Target
     - ``quality``, a score between 0 and 10 (the observed scores are 3 to 9)

Features
--------

``fixed_acidity``, ``volatile_acidity``, ``citric_acid``, ``residual_sugar``, ``chlorides``,
``free_sulfur_dioxide``, ``total_sulfur_dioxide``, ``density``, ``pH``, ``sulphates`` and
``alcohol``. The values are in the units of the original UCI release.

Target
------

``y`` holds the quality score of each wine as a ``float64`` with whole-number values. For
classification, convert it with ``data.y.astype(int)``. Most of the wines, about three
quarters, have a score of 5 or 6, and only 5 wines have the highest score, 9.

The data is stored as released by UCI, so repeated rows are kept.

Source and citation
-------------------

The data comes from the UCI Machine Learning Repository and was created by Paulo Cortez and
colleagues at the University of Minho. It was converted to the NumPy NPZ format with the
features stored as ``float64``, the values are otherwise unchanged.

* Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine
  preferences by data mining from physicochemical properties. *Decision Support Systems*,
  47(4), 547-553.
* Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Wine Quality
  [Dataset]. UCI Machine Learning Repository.
  https://archive.ics.uci.edu/dataset/186/wine+quality

License
-------

CC BY 4.0, as stated by the UCI Machine Learning Repository. See :doc:`../license`.

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_wine_quality
   >>> data = load_wine_quality()
   >>> data.X.shape, data.y.shape
   ((6497, 11), (6497,))
   >>> data.feature_names[:3]
   ('fixed_acidity', 'volatile_acidity', 'citric_acid')
   >>> data.target_names
   ('quality',)
   >>> np.bincount(data.y.astype(int))[3:].tolist()
   [30, 216, 2138, 2836, 1079, 193, 5]
