Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients>`__
* Obtained from: UCI dataset 350, read with the ucimlrepo package (version stored in extras['ucimlrepo_version']).
* Creators: I-Cheng Yeh
* DOI: https://doi.org/10.24432/C55S3H

Please cite the dataset as:

   Yeh, I. (2009). Default of Credit Card Clients [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-22. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format.
* The row identifier column ID of the source is not included.
* Column names X1..X23 were replaced with the feature names from the UCI variable descriptions; the values themselves were not modified.
* Features were converted to float64.
* Target Y was kept as integer 0/1 codes, and the class names were set from the Yes/No meaning in the source description.

.. note::

   SEX uses the codes 1 (male) and 2 (female) as documented by the source, so the category codes do not start at 0.

.. note::

   EDUCATION is documented as 1 = graduate school, 2 = university, 3 = high school, 4 = others. The data also contains the undocumented values 0, 5 and 6.

.. note::

   MARRIAGE is documented as 1 = married, 2 = single, 3 = others. The data also contains the undocumented value 0.

.. note::

   The repayment status columns PAY_0, PAY_2, PAY_3, PAY_4, PAY_5 and PAY_6 are documented with the scale -1 = pay duly, 1 to 9 = payment delay in months. The data also contains the undocumented values -2 and 0 in all six columns, and the value 9 does not occur. The value 1 does not occur in PAY_5 and PAY_6. There is no column PAY_1: PAY_0 is the repayment status of September 2005, as in the source.

.. note::

   All raw values are kept as they are in the source; no recoding, cleaning or removal of rows was applied.
