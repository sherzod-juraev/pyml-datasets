Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data>`__
* Obtained from: UCI Machine Learning Repository, dataset 144, downloaded with the ucimlrepo package: the original categorical/symbolic form of the data (the file german.data), all 1000 examples with 20 attributes. The numeric version of the source (german.data-numeric) is not used. The ucimlrepo version is recorded in the file.
* Creators: Hans Hofmann
* DOI: https://doi.org/10.24432/C5NC77

Please cite the dataset as:

   Hofmann, H. (1994). Statlog (German Credit Data) [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5NC77

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-11-03. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Numeric features are stored as float64 and the target as int64 labels.
* Categorical features are stored as integer codes, in the order of the category names listed for each feature. Every category name starts with the code of the source (for example A11), followed by the meaning that the source gives to the code.
* The attributes, which the source calls Attribute1 to Attribute20, have descriptive names taken from the data description of the source, in the order of the source.
* The target is 0 for a good and 1 for a bad credit risk. The source codes them as 1 and 2, in the same order.

.. note::

   The source requires a cost matrix. Its rows are the actual class and its columns the predicted class, and a correct decision costs 0. Classifying a bad customer as good costs 5 and classifying a good customer as bad costs 1. With the classes of this file (0 good, 1 bad) the matrix is [[0, 1], [5, 0]]. The matrix is not stored in the file, so a user has to apply it.

.. note::

   The classes are not balanced: 700 good and 300 bad credit risks.

.. note::

   The integer codes of a categorical feature are labels, not quantities. Some features are ordered (for example savings), but the codes are not distances, and unordered features such as purpose have no order at all.

.. note::

   The source lists the category A47 of purpose and the category A95 of personal_status_sex, but neither occurs in the 1000 samples. They stay in the lists of categories, so the codes keep the order of the source.

.. note::

   personal_status_sex mixes the sex and the marital status of the applicant, and age and foreign_worker describe the applicant as a person. Use these attributes with care: a model that decides about real people on such grounds can be unfair.
