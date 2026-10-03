Diabetes
========

Ten baseline variables measured for 442 diabetes patients, together with a quantitative
measure of disease progression one year after the baseline. It is a small regression dataset
that is often used to demonstrate linear models and regularization.

Overview
--------

.. list-table::
   :widths: 25 75

   * - Loader
     - ``load_diabetes()``
   * - Task
     - Regression
   * - Samples
     - 442
   * - Features
     - 10, all numeric
   * - Targets
     - 1 continuous target, ``target_names`` is ``None``

Features
--------

``age`` (in years), ``sex`` (coded as 1 and 2), ``bmi`` (body mass index), ``bp`` (average
blood pressure) and six blood serum measurements ``s1`` to ``s6``.

.. note::

   The features are the **raw, unscaled** values. scikit-learn's own ``load_diabetes``
   returns mean-centered and scaled features by default; this package does not. If your
   model is sensitive to feature scale, scale ``X`` yourself, for example with pyml's
   ``StandardScaler``.

Target
------

``y`` is a quantitative measure of disease progression one year after the baseline. Its
values range from 25 to 346.

Source and citation
-------------------

The data comes from the study behind the least angle regression paper. The original data
page is https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html.

* Efron, B., Hastie, T., Johnstone, I., & Tibshirani, R. (2004). Least angle regression.
  *Annals of Statistics*, 32(2), 407-499.

License
-------

The original source does not state a license for this dataset, so no license is claimed for
it here. It is included for educational use with attribution to its authors. Please check the
original source before using it for any other purpose. See :doc:`../license`.

Example
-------

.. doctest::

   >>> from pyml_datasets import load_diabetes
   >>> data = load_diabetes()
   >>> data.X.shape, data.y.shape
   ((442, 10), (442,))
   >>> data.feature_names
   ('age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6')
   >>> data.target_names is None
   True
   >>> data.X[:2, :2]
   array([[59.,  2.],
          [48.,  1.]])
