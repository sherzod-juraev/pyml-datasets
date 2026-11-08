Adult
=====

Census records of people from the 1994 Census database. Each sample is a person, and the task
is to predict whether the yearly income is above 50000 dollars. It is a good dataset for
practising with **categorical features**, **missing values** and **unbalanced classes**.

Overview
--------

.. include:: /_generated/adult_overview.inc

Features
--------

Eight features are categorical and stored as integer codes: ``workclass``, ``education``,
``marital_status``, ``occupation``, ``relationship``, ``race``, ``sex`` and
``native_country``. The names of the categories, in the order of the codes, are in
``data.info.categorical``, and ``data.categorical_features`` gives the columns. The categories
of ``education`` are in the order of the education level, so its code is ``education_num - 1``.
The other six features are whole numbers: ``age``, ``fnlwgt``, ``education_num`` (the
education level from 1, Preschool, to 16, Doctorate), ``capital_gain``, ``capital_loss`` and
``hours_per_week``. ``fnlwgt`` is the final weight of the record in the census sample. The
documentation of the source explains that people with similar demographic characteristics
should have similar weights, and that this holds only within one state.

``workclass``, ``occupation`` and ``native_country`` have missing entries, marked with ``?``
in the source: 6465 values in 3620 rows. They are stored as ``NaN``, so ``data.has_missing``
is ``True``. Fill or drop them before fitting a model that cannot handle ``NaN``.

The source comes in two files, a training part and a test part. The dataset holds both: the
first 32561 rows are the training part and the last 16281 rows are the test part.

Target
------

``y`` is 0 if the yearly income is at most 50K (37155 people) and 1 if it is above 50K
(11687). The classes are unbalanced, so accuracy alone is a poor measure of a model.

.. include:: /_generated/adult_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_adult
   >>> data = load_adult()
   >>> data.X.shape
   (48842, 14)
   >>> data.has_missing
   True
   >>> int(np.isnan(data.X).sum())
   6465
   >>> data.categorical_features
   (1, 3, 5, 6, 7, 8, 9, 13)
   >>> data.info.categorical["sex"]
   ('Female', 'Male')
   >>> data.target_names
   ('<=50K', '>50K')
   >>> np.bincount(data.y)
   array([37155, 11687])
