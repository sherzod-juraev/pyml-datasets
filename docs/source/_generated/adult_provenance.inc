Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/2/adult>`__
* Obtained from: UCI Machine Learning Repository, dataset 2, downloaded with the ucimlrepo package: all 48842 examples with 14 inputs, the training part of the source (adult.data, 32561 rows) followed by its test part (adult.test, 16281 rows). The ucimlrepo version is recorded in the file.
* Creators: Barry Becker, Ronny Kohavi
* DOI: https://doi.org/10.24432/C5XW20

Please cite the dataset as:

   Becker, B. & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20

See also:

* Kohavi, R. (1996). Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid. Proceedings of the Second International Conference on Knowledge Discovery and Data Mining.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-11-08. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Numeric features are stored as float64 and the target as int64 labels.
* Categorical features are stored as integer codes, in the order of the category names listed for each feature. The categories are in alphabetical order, except those of education, which are in the order of the education level, so its code is education_num minus one. The target is 0 for <=50K and 1 for >50K.
* The training part and the test part of the source are stored together, the training part first. The test part writes the target with a trailing dot (<=50K. and >50K.). The dot is dropped, so both parts use the same two classes.
* Entries of workclass, occupation and native_country that the source marks as missing are stored as NaN. UCI delivers some of them as the text ? and some as empty cells, both become NaN.
* The hyphens in the column names are replaced with underscores, for example marital-status becomes marital_status.

.. note::

   Missing entries, the text ? in the source, occur in workclass, occupation and native_country: 6465 values in 3620 rows, which leaves 45222 complete rows, the number that the source documentation gives. The missing entries are NaN, so fill or drop them before fitting a model that cannot handle NaN.

.. note::

   The first 32561 rows are the training part of the source and the last 16281 rows are its test part, so slicing the rows gives back the split of the source.

.. note::

   The classes are not balanced: 11687 of the 48842 people, 23.93 percent, are in the class above 50K, as the source documentation states.

.. note::

   education_num is the education level as a number. It holds the same information as education, because every education has exactly one education_num in the source.

.. note::

   Rows that repeat an earlier row are kept as they are in the source.

.. note::

   race and sex are features of the dataset, and the UCI variables table marks them as demographic variables. A model that uses them can reproduce social bias, so check its fairness before it is used for decisions about people.
