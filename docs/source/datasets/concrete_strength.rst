Concrete Compressive Strength
=============================

Compressive strength of 1030 concrete samples, to be predicted from the amounts of seven
ingredients of the mixture and the age of the concrete. The source describes the compressive
strength as a highly nonlinear function of age and ingredients. It is a small, clean
**regression** dataset: all features are numbers and nothing is missing.

Overview
--------

.. include:: /_generated/concrete_strength_overview.inc

Features
--------

The features are stored in this order: ``cement``, ``blast_furnace_slag``, ``fly_ash``,
``water``, ``superplasticizer``, ``coarse_aggregate``, ``fine_aggregate`` and ``age``. The
first seven are the amounts of the ingredients in kg in a m3 mixture, and ``age`` is the age
of the concrete in days, from 1 to 365. All of them are stored as ``float64``. The names are
the names of the source written in lower case with underscores.

Target
------

``y`` is the concrete compressive strength in MPa (megapascals), stored as ``float64``.

.. include:: /_generated/concrete_strength_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_concrete_strength
   >>> data = load_concrete_strength()
   >>> data.X.shape, data.y.shape
   ((1030, 8), (1030,))
   >>> data.feature_names[-1]
   'age'
   >>> data.has_missing
   False
   >>> round(float(data.y.min()), 2), round(float(data.y.max()), 2)
   (2.33, 82.6)
