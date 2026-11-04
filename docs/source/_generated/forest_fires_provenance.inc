Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/162/forest+fires>`__
* Obtained from: UCI Machine Learning Repository, dataset 162, downloaded with the ucimlrepo package: all 517 examples with 12 inputs and the target area. The ucimlrepo version is recorded in the file.
* Creators: Paulo Cortez, Anbal Morais
* DOI: https://doi.org/10.24432/C5D88D

Please cite the dataset as:

   Cortez, P. & Morais, A. (2007). Forest Fires [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5D88D

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-11-04. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. The features and the target are stored as float64.
* The categorical features month and day are stored as integer codes, in the order of the category names listed for each feature: the months from jan to dec and the days of the week from mon to sun.

.. note::

   The target area is very skewed towards 0.0. The source page says that it may make sense to model it with the logarithm transform, and the paper of the source used ln(x+1). The values are stored as released, without any transform.

.. note::

   X and Y are the coordinates of a grid on the map of the Montesinho park, stored as whole numbers.

.. note::

   The variables table of UCI lists DMC, rain and area as integers, although the ranges that it gives for them have decimals. The values are stored as real numbers.
