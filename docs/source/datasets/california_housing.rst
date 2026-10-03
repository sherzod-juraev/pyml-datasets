California Housing
==================

Median house prices and neighborhood statistics for 20640 block groups in California, based on
the 1990 U.S. census. Each row describes one block group, the smallest geographical unit for
which the census publishes sample data. It is the largest dataset in the package and a
standard regression benchmark.

Overview
--------

.. list-table::
   :widths: 25 75

   * - Loader
     - ``load_california_housing()``
   * - Task
     - Regression
   * - Samples
     - 20640
   * - Features
     - 8, all numeric
   * - Targets
     - 1 continuous target, named ``MedHouseVal``

Features
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Name
     - Meaning
   * - ``MedInc``
     - Median income in the block group
   * - ``HouseAge``
     - Median house age in the block group
   * - ``AveRooms``
     - Average number of rooms per household
   * - ``AveBedrms``
     - Average number of bedrooms per household
   * - ``Population``
     - Population of the block group
   * - ``AveOccup``
     - Average number of household members
   * - ``Latitude``
     - Latitude of the block group
   * - ``Longitude``
     - Longitude of the block group

Target
------

``y`` is the median house value of the block group, in units of 100,000 US dollars. The
values are capped at about 5.0, which means 500,000 dollars.

Source and citation
-------------------

* Pace, R. K., & Barry, R. (1997). Sparse spatial autoregressions. *Statistics & Probability
  Letters*, 33(3), 291-297.

The data is distributed through scikit-learn, which is where this package took it from.

License
-------

The original source does not state a license for this dataset, so no license is claimed for
it here. It is included for educational use with attribution to its authors. Please check the
original source before using it for any other purpose. See :doc:`../license`.

Example
-------

.. doctest::

   >>> from pyml_datasets import load_california_housing
   >>> data = load_california_housing()
   >>> data.X.shape, data.y.shape
   ((20640, 8), (20640,))
   >>> data.feature_names[:4]
   ('MedInc', 'HouseAge', 'AveRooms', 'AveBedrms')
   >>> data.target_names
   ('MedHouseVal',)
