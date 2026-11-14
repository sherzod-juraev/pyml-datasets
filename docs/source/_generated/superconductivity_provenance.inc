Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/464/superconductivty+data>`__
* Obtained from: UCI Machine Learning Repository, dataset 464, downloaded with the ucimlrepo package: all 21263 examples with 81 inputs and the target. The ucimlrepo version is recorded in the file.
* Creators: Kam Hamidieh
* DOI: https://doi.org/10.24432/C53P47

Please cite the dataset as:

   Hamidieh, K. (2018). Superconductivty Data [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C53P47.

See also:

* Hamidieh, K. (2018). A data-driven statistical model for predicting the critical temperature of a superconductor. Computational Materials Science.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-11-14. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. The features and the target are stored as float64.
* The data comes from the file train.csv of the source, which ucimlrepo gives. The file unique_m.csv, which has the chemical formula of every row, is not stored.
* The names of the features and of the target are the column names of the source.

.. note::

   The 81 features are number_of_elements and ten statistics (mean, wtd_mean, gmean, wtd_gmean, entropy, wtd_entropy, range, wtd_range, std and wtd_std) of eight properties (atomic_mass, fie, atomic_radius, Density, ElectronAffinity, FusionHeat, ThermalConductivity and Valence). The UCI page gives no description of the features, so only their names are documented here.

.. note::

   The source file train.csv has 66 rows that repeat another row in all 82 columns. The file unique_m.csv of the source, with the chemical formula of every row, has no repeated row, so these rows appear to be different compounds that have the same values. All 21263 rows are kept. Keep this in mind when you split the data: equal rows in the training and in the test part make the test result look better.

.. note::

   number_of_elements, range_atomic_radius and range_Valence hold whole numbers only. There are no missing values.

.. note::

   The target critical_temp goes from 0.00021 to 185 in the source file.

.. note::

   According to the UCI page the original data comes from http://supercon.nims.go.jp/index_en.html, which it calls public. The license above is the one that the UCI page states for this dataset.

.. note::

   The UCI page spells the name of the dataset Superconductivty. The name here is corrected, while the URL of the source and the citation keep the spelling of UCI.
