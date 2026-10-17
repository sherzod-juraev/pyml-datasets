Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits>`__
* Obtained from: scikit-learn (sklearn.datasets.load_digits), which redistributes a copy of the test set of the UCI dataset. The scikit-learn version is recorded in the file.
* Creators: E. Alpaydin, C. Kaynak
* DOI: https://doi.org/10.24432/C50P49

Please cite the dataset as:

   Alpaydin, E. & Kaynak, C. (1998). Optical Recognition of Handwritten Digits [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C50P49

See also:

* C. Kaynak (1995) Methods of Combining Multiple Classifiers and Their Applications to Handwritten Digit Recognition, MSc Thesis, Institute of Graduate Studies in Science and Engineering, Bogazici University.
* E. Alpaydin, C. Kaynak (1998) Cascading Classifiers, Kybernetika.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-17. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Only the test set of the UCI dataset is included: 1797 of its 5620 samples, as distributed by scikit-learn. The training set (3823 samples) is not included.
* Converted to the NumPy NPZ format. Pixels are stored as float64 and the digit as int64 labels.
* Feature and class names follow scikit-learn.
