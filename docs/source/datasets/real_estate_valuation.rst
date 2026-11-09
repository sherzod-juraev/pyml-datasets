Real Estate Valuation
=====================

Market data of house sales in the Sindian District of New Taipei City, Taiwan, with the house
price of unit area to be predicted from the age and the surroundings of the house. It is a
small **regression** dataset: 414 samples and 6 numeric features without missing values,
including the geographic coordinates of the houses.

Overview
--------

.. include:: /_generated/real_estate_valuation_overview.inc

Features
--------

All six features are numbers, stored as ``float64``, and none of them is categorical:

- ``transaction_date``, the date of the sale as a number: 2013.250 is March 2013 and 2013.500
  is June 2013. Only twelve different dates occur, from 2012.667 to 2013.583.
- ``house_age``, the age of the house in years.
- ``distance_to_nearest_mrt_station``, the distance to the nearest MRT station in meters.
- ``number_of_convenience_stores``, the number of convenience stores in the living circle on
  foot. It is a whole number from 0 to 10.
- ``latitude`` and ``longitude``, the geographic coordinates of the house in degrees.

The dataset has no missing values. The identifier column ``No`` of the source is not stored.

The dates are stored as ``ucimlrepo`` gives them, rounded to three decimals. The xlsx file of
the UCI page has seven decimals (2012.9166667 for the first sale), so the stored dates differ
from it by 0.0004 at most.

Target
------

``y`` is the house price of unit area, in 10000 New Taiwan Dollar per Ping, where a Ping is a
local unit of area, 1 Ping = 3.3 square meters. In the data file of the source it goes from
7.6 to 117.5.

The source says that the data was randomly split into a training part (2/3 of the samples) and
a testing part (1/3), but its file does not tell which sample belongs to which part. The
dataset holds all 414 samples and does not provide the split, so make your own, for example
a random split with a fixed seed.

.. include:: /_generated/real_estate_valuation_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_real_estate_valuation
   >>> data = load_real_estate_valuation()
   >>> data.X.shape, data.y.shape
   ((414, 6), (414,))
   >>> data.has_missing
   False
   >>> data.feature_names[2]
   'distance_to_nearest_mrt_station'
   >>> data.target_names
   ('house_price_of_unit_area',)
