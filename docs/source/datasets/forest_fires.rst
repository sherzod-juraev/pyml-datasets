Forest Fires
============

Forest fires in the northeast region of Portugal, with the burned area to be predicted from
meteorological and other data. The source calls it a difficult **regression** task, and it
is a good dataset for practising with a **skewed target** (about half of the fires have the
area zero) and with **categorical features**.

Overview
--------

.. include:: /_generated/forest_fires_overview.inc

Features
--------

Two features are categorical and stored as integer codes: ``month`` (from jan to dec) and
``day`` (the day of the week, from mon to sun). The names of the categories, in the order of
the codes, are in ``data.info.categorical``, and ``data.categorical_features`` gives the
columns. The other ten features are numbers, stored as ``float64``:

- ``X`` and ``Y``, the coordinates of the place of the fire on the map of the Montesinho park.
  They are whole numbers from 1 to 9 and from 2 to 9.
- ``FFMC``, ``DMC``, ``DC`` and ``ISI``, four indices of the Fire Weather Index (FWI) system.
- ``temp`` (temperature in degrees Celsius), ``RH`` (relative humidity in percent), ``wind``
  (wind speed in km/h) and ``rain`` (outside rain in mm/m2).

The features are stored in the order of the variables table of the source. The dataset has no
missing values. In the data file of the source most of the fires are in August (184) and in
September (172), and ``rain`` is zero for most of them.

The variables table of UCI lists ``DMC``, ``rain`` and ``area`` as integers, although the
ranges that it gives for them have decimals. All values are stored as real numbers.

Target
------

``y`` is the burned area of the forest in hectares, stored as ``float64``. In the data file of
the source it goes from 0 to 1090.84, its mean is 12.85, and 247 of the 517 fires have the
area 0. The source says that this variable is very skewed towards 0.0 and that it may make
sense to model it with the logarithm transform. The paper of the source, Cortez and Morais
(2007), transformed it with ln(x+1) and converted the predictions back. The values here are
stored as released, so applying a transform is up to the user.

.. include:: /_generated/forest_fires_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_forest_fires
   >>> data = load_forest_fires()
   >>> data.X.shape, data.y.shape
   ((517, 12), (517,))
   >>> data.has_missing
   False
   >>> data.categorical_features
   (2, 3)
   >>> data.info.categorical["day"][4]
   'fri'
   >>> round(float(data.y.max()), 2)
   1090.84
   >>> int((data.y == 0).sum())
   247
