Superconductivity
=================

Data on superconductors, to predict the critical temperature of a superconductor from 81
numeric features. It is a large **regression** dataset: 21263 samples and 81 features, all of
them numbers, without missing values. The features are statistics of properties of the
superconductor, so the columns are strongly related to each other.

Overview
--------

.. include:: /_generated/superconductivity_overview.inc

Features
--------

All 81 features are numbers, stored as ``float64``, and none of them is categorical. The UCI
page gives no description of the features, so this page only tells how their names are built.

- ``number_of_elements`` is the first column. It holds whole numbers from 1 to 9.
- The other 80 columns are ten statistics of each of eight properties, written as
  ``<statistic>_<property>``, for example ``mean_atomic_mass`` or ``wtd_std_Valence``. The
  columns of one property follow each other.

The ten statistics, in the order of the columns of a property, are ``mean``, ``wtd_mean``,
``gmean``, ``wtd_gmean``, ``entropy``, ``wtd_entropy``, ``range``, ``wtd_range``, ``std`` and
``wtd_std``. The eight properties, in the order of the columns, are ``atomic_mass``, ``fie``,
``atomic_radius``, ``Density``, ``ElectronAffinity``, ``FusionHeat``,
``ThermalConductivity`` and ``Valence``. The names are kept as they are in the source, so
some of them have capital letters.

Two more columns, ``range_atomic_radius`` and ``range_Valence``, hold whole numbers only.
The dataset has no missing values.

Repeated rows
-------------

66 rows of the source file repeat another row in all columns. They are kept, so the dataset
has all 21263 rows of the source. The file ``unique_m.csv`` of the source, which has the
chemical formula of every row, has no repeated row, so these rows appear to be different
compounds that have the same values. When you split the data into a training and a test part,
equal rows can end up in both parts and make the test result look better than it is.

Target
------

``y`` is the critical temperature, the column ``critical_temp`` of the source. It goes from
0.00021 to 185 and its mean is 34.4212.

The source has a second file, ``unique_m.csv``, with the chemical formula of every
superconductor broken up into the number of atoms of every element. It is not part of this
dataset.

.. include:: /_generated/superconductivity_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_superconductivity
   >>> data = load_superconductivity()
   >>> data.X.shape, data.y.shape
   ((21263, 81), (21263,))
   >>> data.has_missing
   False
   >>> data.feature_names[:2]
   ('number_of_elements', 'mean_atomic_mass')
   >>> data.target_names
   ('critical_temp',)
   >>> float(data.y.max())
   185.0
