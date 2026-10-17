Wine Quality
============

Physicochemical measurements of 6497 red and white vinho verde wines from the north of
Portugal, together with the quality of each wine as a score given by wine tasters. Red and
white wines are stored together and the colour of the wine is not part of the data. The
scores are ordered and unbalanced, so the dataset suits regression as well as ordinal or
multiclass classification.

Overview
--------

.. include:: /_generated/wine_quality_overview.inc

Features
--------

``fixed_acidity``, ``volatile_acidity``, ``citric_acid``, ``residual_sugar``, ``chlorides``,
``free_sulfur_dioxide``, ``total_sulfur_dioxide``, ``density``, ``pH``, ``sulphates`` and
``alcohol``. The values are in the units of the original UCI release.

Target
------

``y`` holds the quality score of each wine as a ``float64`` with whole-number values. For
classification, convert it with ``data.y.astype(int)``. About three quarters of the wines
have a score of 5 or 6, and only 5 wines have the highest score, 9. The data is stored as
released by UCI, so repeated rows are kept.

.. include:: /_generated/wine_quality_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_wine_quality
   >>> data = load_wine_quality()
   >>> data.X.shape
   (6497, 11)
   >>> float(data.y.min()), float(data.y.max())
   (3.0, 9.0)
