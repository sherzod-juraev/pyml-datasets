Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/222/bank+marketing>`__
* Obtained from: UCI Machine Learning Repository, dataset 222, downloaded with the ucimlrepo package: all 45211 examples with 16 inputs (the bank-full version). The ucimlrepo version is recorded in the file.
* Creators: S. Moro, P. Rita, P. Cortez
* DOI: https://doi.org/10.24432/C5K306

Please cite the dataset as:

   Moro, S., Rita, P., & Cortez, P. (2014). Bank Marketing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5K306

See also:

* Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the success of bank telemarketing. Decision Support Systems, 62, 22-31.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-23. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Numeric features are stored as float64 and the target as int64 labels.
* Categorical features are stored as integer codes, in the order of the category names listed for each feature. The target is 0 for no and 1 for yes.
* Entries of job, education, contact and poutcome that the UCI release marks as missing are stored as the category unknown, which the data description of the source lists for these features. No NaN values are stored.
* The column that UCI calls day_of_week is named day, because the source describes it as the day of the month of the last contact.

.. note::

   The duration of the last call is only known after the call, and the call ends with the answer. The source advises to use duration for benchmarks only and to drop it for a realistic predictive model.

.. note::

   pdays is -1 for clients who were not contacted in a previous campaign. The value is kept as it is in the source.

.. note::

   The classes are not balanced: far fewer clients subscribed than not.
