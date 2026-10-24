Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength>`__
* Obtained from: UCI Machine Learning Repository, dataset 165, downloaded with the ucimlrepo package: all 1030 examples with 8 inputs. The ucimlrepo version is recorded in the file.
* Creators: I-Cheng Yeh
* DOI: https://doi.org/10.24432/C5PK67

Please cite the dataset as:

   Yeh, I. (1998). Concrete Compressive Strength [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5PK67

See also:

* Yeh, I. (1998). Modeling of strength of high-performance concrete using artificial neural networks. Cement and Concrete Research, Vol. 28, No. 12.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-24. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Features and the target are stored as float64.
* The names of the columns are written in lower case with underscores, for example Blast Furnace Slag is stored as blast_furnace_slag. The features are stored in the order of the data description of the source, the target is the concrete compressive strength.

.. note::

   The seven ingredients are given in kg in a m3 mixture, the age in days (1 to 365) and the compressive strength in MPa.

.. note::

   The source describes the compressive strength of concrete as a highly nonlinear function of age and ingredients.

.. note::

   The data file that UCI offers for download (Concrete_Data.xls) has more decimals than the table that ucimlrepo returns and that is stored here: the amounts of the ingredients differ by at most 0.05 and the strength by less than 0.005.
