Energy Efficiency
=================

Heating load and cooling load of 768 simulated buildings, to be predicted from eight building
parameters. The source simulated 12 different building shapes in Ecotect, and the buildings
differ in the glazing area, the distribution of the glazing area, the orientation and other
parameters. It is a small, clean **regression** dataset with **two targets**: all features
are numbers and nothing is missing.

Overview
--------

.. include:: /_generated/energy_efficiency_overview.inc

Features
--------

The features are stored in this order, which is the order X1 to X8 of the source:
``relative_compactness``, ``surface_area``, ``wall_area``, ``roof_area``,
``overall_height``, ``orientation``, ``glazing_area`` and ``glazing_area_distribution``. All
of them are stored as ``float64``. The names are the descriptions of the variables table of
the source written in lower case with underscores.

``orientation`` and ``glazing_area_distribution`` are integers in the source. In the data
file of the source ``orientation`` takes the values 2, 3, 4 and 5, and
``glazing_area_distribution`` the values 0 to 5. The source does not say what these numbers
stand for, so they are stored as numbers without category names. The source does not state
the units of the columns, so none are given here.

Targets
-------

``y`` has two columns, both stored as ``float64``: the heating load (column 0, Y1 of the
source) and the cooling load (column 1, Y2). The names are in ``Dataset.target_names``. The
source says that the aim is to predict each of the two responses from the eight features, and
that the data can also be treated as a multi-class classification problem if the response is
rounded to the nearest integer. Here it is stored as a regression dataset.

.. include:: /_generated/energy_efficiency_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_energy_efficiency
   >>> data = load_energy_efficiency()
   >>> data.X.shape, data.y.shape
   ((768, 8), (768, 2))
   >>> data.target_names
   ('heating_load', 'cooling_load')
   >>> data.has_missing
   False
   >>> data.y.min(axis=0).round(2).tolist()
   [6.01, 10.9]
