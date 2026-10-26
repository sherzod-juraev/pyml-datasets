Combined Cycle Power Plant
==========================

Net hourly electrical energy output of a combined cycle power plant, to be predicted from four
hourly average ambient variables. The 9568 data points were collected over 6 years
(2006-2011), while the plant was set to work with full load. It is a clean **regression**
dataset: all features are numbers, nothing is missing, and it is the largest regression
dataset of the package.

Overview
--------

.. include:: /_generated/combined_cycle_power_plant_overview.inc

Features
--------

The features are stored in this order, which is the order of the variables table of the
source: ``temperature`` (AT, in degrees Celsius), ``exhaust_vacuum`` (V, in cm Hg),
``ambient_pressure`` (AP, in millibar) and ``relative_humidity`` (RH, in percent). All of
them are stored as ``float64``. They are hourly averages of ambient variables, taken from
sensors around the plant that record them every second, and the source gives them without
normalization. According to the source the exhaust vacuum is collected from and has an effect
on the steam turbine, and the other three variables affect the performance of the gas
turbine.

The relative humidity goes above 100 percent in the source, up to 100.16, and is stored as it
is.

Target
------

``y`` is the net hourly electrical energy output in MW, stored as ``float64``. The source
documents the range 420.26 to 495.76.

Order of the rows
-----------------

To allow 5x2 fold statistical tests, the source provides the data shuffled five times, one
shuffling in each of the five sheets of its file. The rows of this dataset are in the order
of the table that UCI serves through ``ucimlrepo``, whose first row is the first row of the
first sheet.

.. include:: /_generated/combined_cycle_power_plant_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_combined_cycle_power_plant
   >>> data = load_combined_cycle_power_plant()
   >>> data.X.shape, data.y.shape
   ((9568, 4), (9568,))
   >>> data.feature_names
   ('temperature', 'exhaust_vacuum', 'ambient_pressure', 'relative_humidity')
   >>> data.has_missing
   False
   >>> round(float(data.y.min()), 2), round(float(data.y.max()), 2)
   (420.26, 495.76)
