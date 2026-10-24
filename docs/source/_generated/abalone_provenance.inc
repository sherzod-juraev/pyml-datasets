Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/1/abalone>`__
* Obtained from: UCI Machine Learning Repository, dataset 1, downloaded with the ucimlrepo package: all 4177 examples with 8 inputs. The ucimlrepo version is recorded in the file.
* Creators: Warwick Nash, Tracy Sellers, Simon Talbot, Andrew Cawthorn, Wes Ford
* DOI: https://doi.org/10.24432/C55C7W

Please cite the dataset as:

   Nash, W., Sellers, T., Talbot, S., Cawthorn, A., & Ford, W. (1994). Abalone [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55C7W

See also:

* Nash, W. J., Sellers, T. L., Talbot, S. R., Cawthorn, A. J., & Ford, W. B. (1994). The Population Biology of Abalone (Haliotis species) in Tasmania. I. Blacklip Abalone (H. rubra) from the North Coast and Islands of Bass Strait. Sea Fisheries Division, Technical Report No. 48 (ISSN 1034-3288).
* Waugh, S. (1995). Extending and benchmarking Cascade-Correlation. PhD thesis, Computer Science Department, University of Tasmania.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-24. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Features and the target are stored as float64.
* The column Sex is stored as integer codes, in the order of the category names listed for it. The names of the columns are written in lower case, for example Whole_weight is stored as whole_weight. The target is the number of rings.
* The continuous values are stored as the source gives them, with the scaling that the notes describe.

.. note::

   The source says that examples with missing values were removed from the original data, most of them because the number of rings was missing, and that the ranges of the continuous values were scaled for use with an artificial neural network by dividing by 200. Keep this in mind when you use the units mm and grams that the variable table of UCI lists.

.. note::

   The data comes from a study that was not made for machine learning, by the Marine Resources Division of the Department of Primary Industry and Fisheries, Tasmania. The dataset was donated to UCI by Sam Waugh of the University of Tasmania.

.. note::

   The sex is M, F or I (infant).

.. note::

   The number of rings plus 1.5 gives the age of the abalone in years.
