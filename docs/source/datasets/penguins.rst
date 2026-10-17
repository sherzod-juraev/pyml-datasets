Palmer Penguins
===============

Body measurements of 344 penguins of three species, observed on three islands of the
Palmer Archipelago in Antarctica between 2007 and 2009. It is a friendly alternative to Iris,
and the first dataset here with **missing values** and **categorical features**, which makes
it a good place to practise imputation and encoding.

Overview
--------

.. include:: /_generated/penguins_overview.inc

Features
--------

``island`` and ``sex`` are categorical and stored as integer codes, the names of the
categories are in ``data.info.categorical``. ``bill_length_mm``, ``bill_depth_mm``,
``flipper_length_mm``, ``body_mass_g`` and ``year`` are numbers. Missing values are ``NaN``.
Use ``data.categorical_features`` to find the categorical columns.

Target
------

``y`` is the species: 0 for Adelie (152 penguins), 1 for Chinstrap (68) and 2 for Gentoo
(124). The target has no missing values.

.. include:: /_generated/penguins_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_penguins
   >>> data = load_penguins()
   >>> data.X.shape
   (344, 7)
   >>> data.has_missing, int(np.isnan(data.X).sum())
   (True, 19)
   >>> data.categorical_features
   (0, 5)
   >>> data.info.categorical["sex"]
   ('female', 'male')
