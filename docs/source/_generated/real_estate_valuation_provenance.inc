Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/477/real+estate+valuation+data+set>`__
* Obtained from: UCI Machine Learning Repository, dataset 477, downloaded with the ucimlrepo package: all 414 examples with 6 inputs and the target. The ucimlrepo version is recorded in the file.
* Creators: I-Cheng Yeh
* DOI: https://doi.org/10.24432/C5J30W

Please cite the dataset as:

   Yeh, I. (2018). Real Estate Valuation [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5J30W

See also:

* Yeh, I., & Hsu, T.-K. (2018). Building real estate valuation models with comparative approach through case-based reasoning. Applied Soft Computing.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-11-09. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. The features and the target are stored as float64.
* The identifier column No, the numbers 1 to 414, is not stored, because it is not a feature.
* The column names are written in lowercase with underscores, and the prefixes X1 to X6 and Y are dropped, for example X3 distance to the nearest MRT station becomes distance_to_nearest_mrt_station.

.. note::

   The source says that the data set was randomly split into a training part (2/3 of the samples) and a testing part (1/3), but its file has no column that tells which sample belongs to which part. All 414 samples are stored and the split is not provided.

.. note::

   The transaction date is a number: 2013.250 is March 2013 and 2013.500 is June 2013, as the source describes. Only 12 different dates occur, from 2012.667 to 2013.583. ucimlrepo gives the dates rounded to three decimals, while the xlsx file of the UCI page has seven (the first sale: 2012.9166667), so the stored dates differ from that file by 0.0004 at most.

.. note::

   The target is the house price of unit area in 10000 New Taiwan Dollar per Ping, where a Ping is a local unit of area, 1 Ping = 3.3 square meters, as the source gives.
