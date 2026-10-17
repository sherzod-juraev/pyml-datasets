Missing values
==============

Many real tabular datasets have missing values, and for 0.1.0 the lack of them was a reason
to leave out well-known datasets. The format now allows them under rules:

* A missing value in ``X`` is ``NaN``. ``DatasetInfo.has_missing`` must say so, and the
  build script and a test refuse a file where the flag and the data disagree.
* Targets are never missing, a sample without a label is not part of the dataset.
* Categorical features are integer codes stored as ``float64``, so a missing category can be
  ``NaN`` too. The names of the categories are in ``DatasetInfo.categorical``.
* Infinite values are never allowed.

The package does not impute, encode or drop anything. Rows with missing values stay in the
data, because choosing what to do with them is part of what a student learns, and because
removing rows would be a change to the data that the license page would have to mention.
