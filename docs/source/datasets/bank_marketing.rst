Bank Marketing
==============

Data from the phone-call marketing campaigns of a Portuguese bank. Each sample is a client,
and the task is to predict whether the client subscribed a term deposit. It is a good dataset
for practising with **categorical features** and with **unbalanced classes**.

Overview
--------

.. include:: /_generated/bank_marketing_overview.inc

Features
--------

Nine features are categorical and stored as integer codes: ``job``, ``marital``,
``education``, ``default``, ``housing``, ``loan``, ``contact``, ``month`` and ``poutcome``.
The names of the categories, in the order of the codes, are in ``data.info.categorical``, and
``data.categorical_features`` gives the columns. The other seven features are whole numbers:
``age``, ``balance`` (average yearly balance in euros), ``day`` (day of the month of the last
contact), ``duration`` (seconds), ``campaign``, ``pdays`` and ``previous``.

The features describe three things: the client (``age`` to ``loan``), the last contact of the
current campaign (``contact`` to ``duration``) and the earlier campaigns (``campaign`` to
``poutcome``).

Some entries of ``job``, ``education``, ``contact`` and ``poutcome`` are unknown in the source.
They are stored as the category ``unknown``, so the dataset has no ``NaN`` values. ``pdays`` is
-1 for clients who were not contacted in an earlier campaign, and the value is kept as it is.

.. warning::

   ``duration`` is known only after the call, and the call ends with the answer of the
   client. The source advises to use it for benchmarks only and to drop it for a realistic
   predictive model.

Target
------

``y`` is 0 if the client did not subscribe a term deposit (39922 clients) and 1 if the client
did (5289). The classes are unbalanced, so accuracy alone is a poor measure of a model.

.. include:: /_generated/bank_marketing_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_bank_marketing
   >>> data = load_bank_marketing()
   >>> data.X.shape
   (45211, 16)
   >>> data.has_missing
   False
   >>> data.categorical_features
   (1, 2, 3, 4, 6, 7, 8, 10, 15)
   >>> data.info.categorical["education"]
   ('primary', 'secondary', 'tertiary', 'unknown')
   >>> data.target_names
   ('no', 'yes')
   >>> np.bincount(data.y)
   array([39922,  5289])
