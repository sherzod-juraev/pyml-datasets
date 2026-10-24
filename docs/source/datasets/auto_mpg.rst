Auto MPG
========

City-cycle fuel consumption in miles per gallon of 398 cars, to be predicted from seven
features of the car. It is a small **regression** dataset with a few **missing values** in
one feature, which makes it a good place to practise imputation.

Overview
--------

.. include:: /_generated/auto_mpg_overview.inc

Features
--------

The features are stored in this order: ``cylinders``, ``displacement``, ``horsepower``,
``weight``, ``acceleration``, ``model_year`` and ``origin``. The source describes
``cylinders``, ``model_year`` and ``origin`` as multi-valued discrete features and the other
four as continuous. All of them are stored as ``float64`` with the numbers of the source.
The UCI page gives no units for the features.

``origin`` has the values 1, 2 and 3. The source does not say what they stand for, so the
feature has no category names and ``data.categorical_features`` is empty.

6 values of ``horsepower`` are missing in the source and are stored as ``NaN``. The name of
the car is an identifier that is unique for each car, so it is not stored.

Target
------

``y`` is ``mpg``, the fuel consumption in miles per gallon, stored as ``float64``. A higher
value means a more economical car. The source removed 8 cars of the StatLib original
because their ``mpg`` was unknown, so the target has no missing values.

.. include:: /_generated/auto_mpg_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_auto_mpg
   >>> data = load_auto_mpg()
   >>> data.X.shape, data.y.shape
   ((398, 7), (398,))
   >>> data.feature_names[2]
   'horsepower'
   >>> data.has_missing, int(np.isnan(data.X).sum())
   (True, 6)
   >>> data.categorical_features
   ()
