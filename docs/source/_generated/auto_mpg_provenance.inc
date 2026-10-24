Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/9/auto+mpg>`__
* Obtained from: UCI Machine Learning Repository, dataset 9, downloaded with the ucimlrepo package: all 398 examples of the revised version, in which the source already removed 8 examples of the StatLib original because their mpg was unknown. The ucimlrepo version is recorded in the file.
* Creators: R. Quinlan
* DOI: https://doi.org/10.24432/C5859H

Please cite the dataset as:

   Quinlan, R. (1993). Auto MPG [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5859H

See also:

* Quinlan, R. (1993). Combining Instance-Based and Model-Based Learning. In Proceedings on the Tenth International Conference of Machine Learning, 236-243, University of Massachusetts, Amherst. Morgan Kaufmann.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-24. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Features and the target mpg are stored as float64.
* The 6 missing values of horsepower are stored as NaN.
* The column car_name, which UCI marks as an identifier and describes as a string that is unique for each instance, is not stored, because X holds numbers only. The other columns are stored in the order of the data description of the source.

.. note::

   The source took the data from the StatLib library at Carnegie Mellon University, where it was used in the 1983 American Statistical Association Exposition, and calls it a slightly modified version of that dataset.

.. note::

   6 values of horsepower are missing and stored as NaN. Impute them or drop the rows before fitting a model that cannot handle NaN.

.. note::

   cylinders, model_year and origin are multi-valued discrete features in the source and are stored as its numbers. The source does not say what the numbers of origin stand for, so origin has no category names.

.. note::

   mpg is fuel consumption in miles per gallon, so a higher value means a more economical car.
