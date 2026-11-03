German Credit
=============

Credit applicants described by 20 attributes, to be classified as good or bad credit risks. It
is the classic small dataset for **cost-sensitive classification**: the source gives a cost
matrix in which a wrong "good" costs five times more than a wrong "bad". It also has
**categorical features** and **unbalanced classes**.

Overview
--------

.. include:: /_generated/german_credit_overview.inc

Features
--------

Thirteen features are categorical and stored as integer codes: ``checking_status``,
``credit_history``, ``purpose``, ``savings``, ``employment_since``, ``personal_status_sex``,
``other_debtors``, ``property``, ``other_installment_plans``, ``housing``, ``job``,
``telephone`` and ``foreign_worker``. The names of the categories, in the order of the codes,
are in ``data.info.categorical``, and ``data.categorical_features`` gives the columns. Each
name starts with the code of the source (for example ``A11``). The codes are labels, not
quantities.

The other seven features are whole numbers: ``duration`` (months), ``credit_amount``,
``installment_rate`` (percentage of the disposable income), ``residence_since``, ``age``
(years), ``existing_credits`` (number of credits at this bank) and ``people_liable`` (number
of people the applicant has to provide maintenance for). The dataset has no missing values.

The source lists the category ``A47`` of ``purpose`` and the category ``A95`` of
``personal_status_sex``, but neither occurs in the 1000 samples.

.. warning::

   ``personal_status_sex`` mixes the sex and the marital status of the applicant, and ``age``
   and ``foreign_worker`` describe the applicant as a person. Use these attributes with care:
   a model that decides about real people on such grounds can be unfair.

Target
------

``y`` is 0 for a good credit risk (700 applicants) and 1 for a bad one (300). The source codes
the classes 1 and 2, in the same order. The classes are unbalanced, so accuracy alone is a poor
measure of a model.

Cost matrix
~~~~~~~~~~~

The source requires a cost matrix. Its rows are the actual class and its columns the predicted
class. A bad customer classified as good costs 5, a good customer classified as bad costs 1,
and a correct decision costs 0. With the classes of this file the matrix is
``[[0, 1], [5, 0]]``. The package does not store it, so a user has to apply it.

.. include:: /_generated/german_credit_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_german_credit
   >>> data = load_german_credit()
   >>> data.X.shape
   (1000, 20)
   >>> data.has_missing
   False
   >>> data.categorical_features
   (0, 2, 3, 5, 6, 8, 9, 11, 13, 14, 16, 18, 19)
   >>> data.info.categorical["foreign_worker"]
   ('A201: yes', 'A202: no')
   >>> data.target_names
   ('good', 'bad')
   >>> np.bincount(data.y)
   array([700, 300])
   >>> cost = np.array([[0, 1], [5, 0]])
   >>> int(cost[1, 0])  # a bad customer classified as good
   5
