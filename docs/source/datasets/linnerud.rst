Linnerud
========

Physical exercise data for 20 middle-aged men at a fitness club: three exercise measurements
and three physiological measurements. It is a **multi-output** regression dataset, so ``y``
has one column per physiological variable.

Overview
--------

.. list-table::
   :widths: 25 75

   * - Loader
     - ``load_linnerud()``
   * - Task
     - Multi-output regression
   * - Samples
     - 20
   * - Features
     - 3 exercise measurements
   * - Targets
     - 3 physiological measurements

Features
--------

``Chins``, ``Situps`` and ``Jumps``: how many chin-ups, sit-ups and jumps each person
performed.

Targets
-------

``y`` has shape ``(20, 3)``. Its columns follow ``target_names``: ``Weight``, ``Waist`` and
``Pulse``.

.. note::

   Models that only support a one-dimensional ``y`` need one column at a time, for example
   ``data.y[:, 0]`` for ``Weight``.

Source and citation
-------------------

* Tenenhaus, M. (1998). *La regression PLS: theorie et pratique*. Paris: Editions Technip.

The data is distributed through scikit-learn, which is where this package took it from.

License
-------

The original source does not state a license for this dataset, so no license is claimed for
it here. It is included for educational use with attribution to its authors. Please check the
original source before using it for any other purpose. See :doc:`../license`.

Example
-------

.. doctest::

   >>> from pyml_datasets import load_linnerud
   >>> data = load_linnerud()
   >>> data.X.shape, data.y.shape
   ((20, 3), (20, 3))
   >>> data.feature_names
   ('Chins', 'Situps', 'Jumps')
   >>> data.target_names
   ('Weight', 'Waist', 'Pulse')
   >>> data.X[:2]
   array([[  5., 162.,  60.],
          [  2., 110.,  60.]])
