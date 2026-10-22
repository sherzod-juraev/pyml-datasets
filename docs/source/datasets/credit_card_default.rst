Default of Credit Card Clients
==============================

Payment records of 30000 credit card clients in Taiwan, from April to September 2005. The
data was collected for a study that compared six data mining methods at predicting default
payments. The task is binary classification: will the client default on the payment of the
next month? The classes are unbalanced, about 22 percent of the clients default.

Overview
--------

.. include:: /_generated/credit_card_default_overview.inc

Features
--------

23 integer features. The names are the ones of the UCI variable descriptions, the source
calls them ``X1`` to ``X23``:

* ``LIMIT_BAL``: the amount of the given credit in NT dollars. It includes the individual
  consumer credit and the family (supplementary) credit.
* ``SEX`` (1 = male, 2 = female), ``EDUCATION`` (1 = graduate school, 2 = university,
  3 = high school, 4 = others), ``MARRIAGE`` (1 = married, 2 = single, 3 = others) and
  ``AGE`` in years.
* ``PAY_0``, ``PAY_2``, ``PAY_3``, ``PAY_4``, ``PAY_5`` and ``PAY_6``: the repayment status
  from September back to April 2005. The source documents the scale -1 = pay duly, 1 = payment
  delay of one month, up to 9 = delay of nine months and above. There is no ``PAY_1``,
  ``PAY_0`` is the status of September.
* ``BILL_AMT1`` to ``BILL_AMT6``: the amount of the bill statement in NT dollars, from
  September back to April 2005.
* ``PAY_AMT1`` to ``PAY_AMT6``: the amount of the previous payment in NT dollars, from
  September back to April 2005.

The data is stored exactly as released. Some values are not covered by the documentation of
the source: ``EDUCATION`` also contains 0, 5 and 6, ``MARRIAGE`` also contains 0, and all
``PAY_*`` columns also contain -2 and 0. The categorical columns keep the raw integer codes
of the source (``SEX`` is 1 and 2, not 0 and 1) and are not declared as categorical features.
Nothing was recoded or removed, so decide yourself how to treat these values. The row
identifier column ``ID`` of the source is not included.

The features describe the sex, education, marital status and age of individual clients. A
model trained on them can reproduce unfair differences between groups, keep this in mind
before drawing conclusions about people.

Target
------

``y`` is 0 for a client with no default payment next month and 1 for a client with a
default payment next month, in the order of ``target_names``. 6636 of the 30000 clients
(22.12 percent) have the label 1 and 23364 have the label 0.

.. include:: /_generated/credit_card_default_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_credit_card_default
   >>> data = load_credit_card_default()
   >>> data.X.shape
   (30000, 23)
   >>> data.target_names
   ('No default payment', 'Default payment')
   >>> np.bincount(data.y)
   array([23364,  6636])
