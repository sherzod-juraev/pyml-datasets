Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/186/wine+quality>`__
* Obtained from: UCI Machine Learning Repository, dataset 186, downloaded with the ucimlrepo package. The ucimlrepo version is recorded in the file.
* Creators: Paulo Cortez, A. Cerdeira, F. Almeida, T. Matos, J. Reis
* DOI: https://doi.org/10.24432/C56S3T

Please cite the dataset as:

   Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Wine Quality [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56S3T

See also:

* Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. Decision Support Systems, 47(4), 547-553.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-17. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Features and the quality score are stored as float64.
* The red wines (1599) and the white wines (4898) are stored together. As in the UCI release, the colour of the wine is not a feature.
