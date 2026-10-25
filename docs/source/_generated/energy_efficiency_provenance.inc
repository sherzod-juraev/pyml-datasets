Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/242/energy+efficiency>`__
* Obtained from: UCI Machine Learning Repository, dataset 242, downloaded with the ucimlrepo package: all 768 examples with 8 inputs and 2 targets. The ucimlrepo version is recorded in the file.
* Creators: Athanasios Tsanas, Angeliki Xifara
* DOI: https://doi.org/10.24432/C51307

Please cite the dataset as:

   Tsanas, A. & Xifara, A. (2012). Energy Efficiency [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C51307.

See also:

* Tsanas, A., Xifara, A. (2012). Accurate quantitative estimation of energy performance of residential buildings using statistical machine learning tools. Energy and Buildings, vol. 49.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-25. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Features and targets are stored as float64.
* The two targets are stored together: y has the shape (768, 2), the first column is the heating load (Y1 of the source) and the second column is the cooling load (Y2).
* The columns X1 to X8 are named after their descriptions in the variables table of the source, written in lower case with underscores, for example Glazing Area Distribution (X8) is stored as glazing_area_distribution. The features are stored in the order X1 to X8.

.. note::

   The buildings are 12 different building shapes simulated in Ecotect. They differ in the glazing area, the distribution of the glazing area and the orientation, among other parameters, and 768 building shapes were obtained by simulating various settings of these characteristics.

.. note::

   The source says the aim is to predict each of the two responses from the eight features, and that the data can also be used as a multi-class classification problem if the response is rounded to the nearest integer. This library stores it as a regression dataset.

.. note::

   orientation and glazing_area_distribution are integers in the source. The source does not say what their numbers stand for, so they are stored as its numbers without category names.

.. note::

   The source does not state the units of the columns, so none are given here.
