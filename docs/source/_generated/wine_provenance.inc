Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/109/wine>`__
* Obtained from: scikit-learn (sklearn.datasets.load_wine), which redistributes a copy of the data. The scikit-learn version is recorded in the file.
* Creators: Stefan Aeberhard, M. Forina
* DOI: https://doi.org/10.24432/C5PC7J

Please cite the dataset as:

   Aeberhard, S. & Forina, M. (1992). Wine [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5PC7J

See also:

* Forina, M. et al. PARVUS: an extendable package of programs for data exploration, classification and correlation. Institute of Pharmaceutical and Food Analysis and Technologies, Genoa, Italy.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-17. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Values are stored as float64 and the cultivar as int64 labels.
* The cultivar labels are 0, 1 and 2 (the UCI file numbers them 1, 2 and 3).
* Feature and class names follow scikit-learn.
