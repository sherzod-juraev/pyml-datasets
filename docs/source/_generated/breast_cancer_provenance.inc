Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic>`__
* Obtained from: scikit-learn (sklearn.datasets.load_breast_cancer), which redistributes a copy of the data. The scikit-learn version is recorded in the file.
* Creators: William Wolberg, Olvi Mangasarian, Nick Street, W. Street
* DOI: https://doi.org/10.24432/C5DW2B

Please cite the dataset as:

   Wolberg, W., Mangasarian, O., Street, N., & Street, W. (1993). Breast Cancer Wisconsin (Diagnostic) [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5DW2B

See also:

* W. N. Street, W. H. Wolberg and O. L. Mangasarian. Nuclear feature extraction for breast tumor diagnosis. IS&T/SPIE 1993 International Symposium on Electronic Imaging: Science and Technology, volume 1905, pages 861-870, San Jose, CA, 1993.
* O. L. Mangasarian, W. N. Street and W. H. Wolberg. Breast cancer diagnosis and prognosis via linear programming. Operations Research, 43(4), pages 570-577, July-August 1995.
* W. H. Wolberg, W. N. Street, and O. L. Mangasarian. Machine learning techniques to diagnose breast cancer from fine-needle aspirates. Cancer Letters 77 (1994) 163-171.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-17. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Values are stored as float64 and the diagnosis as int64 labels (0 = malignant, 1 = benign).
* The diagnosis is a number instead of the letters used in the UCI file, and the sample identifier column is not included.
* Feature and class names follow scikit-learn.

.. note::

   This dataset is for learning about machine learning methods. It is not a medical tool and must not be used to diagnose anything.
