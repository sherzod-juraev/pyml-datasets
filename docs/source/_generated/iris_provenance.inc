Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/53/iris>`__
* Obtained from: scikit-learn (sklearn.datasets.load_iris), which redistributes a copy of the data. The scikit-learn version is recorded in the file.
* Creators: R. A. Fisher
* DOI: https://doi.org/10.24432/C56C76

Please cite the dataset as:

   Fisher, R. (1936). Iris [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56C76

See also:

* Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics, 7(2), 179-188.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-17. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Values are stored as float64 and the species as int64 labels (0 = setosa, 1 = versicolor, 2 = virginica).
* Samples 35 and 38 follow Fisher's paper, as corrected in scikit-learn. The UCI page lists these two samples as differing between its file and the paper.
* Feature and class names follow scikit-learn.
