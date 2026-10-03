Wine
====

Results of a chemical analysis of wines grown in the same region of Italy but derived from
three different cultivars. The analysis measured 13 constituents in each wine. The classes
are well separated, which makes it a good dataset for a first test of a new classifier.

Overview
--------

.. list-table::
   :widths: 25 75

   * - Loader
     - ``load_wine()``
   * - Task
     - Classification
   * - Samples
     - 178
   * - Features
     - 13, all continuous
   * - Targets
     - 3 classes: ``class_0`` (0), ``class_1`` (1), ``class_2`` (2)

Features
--------

``alcohol``, ``malic_acid``, ``ash``, ``alcalinity_of_ash``, ``magnesium``,
``total_phenols``, ``flavanoids``, ``nonflavanoid_phenols``, ``proanthocyanins``,
``color_intensity``, ``hue``, ``od280/od315_of_diluted_wines`` and ``proline``.

The features are on very different scales (``proline`` is in the hundreds, ``hue`` is around
one), so scaling them usually helps distance-based and gradient-based models.

Target
------

``y`` holds the cultivar of each wine as an integer label. The classes contain 59, 71 and 48
samples.

Source and citation
-------------------

The data was donated to the UCI Machine Learning Repository by Stefan Aeberhard. It was
originally collected by M. Forina and colleagues at the Institute of Pharmaceutical and Food
Analysis and Technologies in Genoa, Italy.

* Aeberhard, S., & Forina, M. (1991). Wine [Dataset]. UCI Machine Learning Repository.
  https://doi.org/10.24432/C5PC7J

License
-------

CC BY 4.0, as stated by the UCI Machine Learning Repository. See :doc:`../license`.

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_wine
   >>> data = load_wine()
   >>> data.X.shape, data.y.shape
   ((178, 13), (178,))
   >>> data.feature_names[:3]
   ('alcohol', 'malic_acid', 'ash')
   >>> data.target_names
   ('class_0', 'class_1', 'class_2')
   >>> np.bincount(data.y)
   array([59, 71, 48])
