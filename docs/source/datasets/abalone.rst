Abalone
=======

Physical measurements of 4177 abalones, with the number of rings of the shell as target.
Counting the rings under a microscope is slow, so the easier measurements are used to predict
them, and the number of rings plus 1.5 gives the age of the abalone in years. The source offers
the target as a continuous value or as a classification problem. The dataset is a good place to
practise **regression with a categorical feature**.

Overview
--------

.. include:: /_generated/abalone_overview.inc

Features
--------

The features are stored in this order: ``sex``, ``length``, ``diameter``, ``height``,
``whole_weight``, ``shucked_weight``, ``viscera_weight`` and ``shell_weight``.

``sex`` is categorical and stored as integer codes: ``F`` is 0, ``I`` (infant) is 1 and ``M``
is 2. The names are in ``data.info.categorical`` and ``data.categorical_features`` gives the
column. The other seven features are continuous.

The variable table of UCI gives mm as the unit of ``length``, ``diameter`` and ``height`` and
grams as the unit of the weights. The source also says that the ranges of the continuous values
were scaled for use with an artificial neural network by dividing by 200. The values are stored
as the source gives them. Examples with missing values were removed from the original data, so
nothing is missing.

Target
------

``y`` is the number of rings, stored as ``float64`` with whole-number values from 1 to 29. The
most common value is 9 rings (689 abalones). For classification, convert it with
``data.y.astype(int)``.

.. include:: /_generated/abalone_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_abalone
   >>> data = load_abalone()
   >>> data.X.shape, data.y.shape
   ((4177, 8), (4177,))
   >>> data.has_missing
   False
   >>> data.categorical_features
   (0,)
   >>> data.info.categorical["sex"]
   ('F', 'I', 'M')
   >>> float(data.y.min()), float(data.y.max())
   (1.0, 29.0)
   >>> round(float(data.y.mean()), 3)
   9.934
   >>> int(np.bincount(data.y.astype(int))[9])
   689
