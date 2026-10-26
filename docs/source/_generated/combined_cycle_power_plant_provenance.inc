Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/294/combined+cycle+power+plant>`__
* Obtained from: UCI Machine Learning Repository, dataset 294, downloaded with the ucimlrepo package: all 9568 examples with 4 inputs. The ucimlrepo version is recorded in the file.
* Creators: Pınar Tüfekci, Heysem Kaya
* DOI: https://doi.org/10.24432/C5002N

Please cite the dataset as:

   Tfekci, P. & Kaya, H. (2014). Combined Cycle Power Plant [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5002N.

See also:

* Tüfekci, P. (2014). Prediction of full load electrical power output of a base load operated combined cycle power plant using machine learning methods. International Journal of Electrical Power & Energy Systems, Volume 60, September 2014, Pages 126-140. https://doi.org/10.1016/j.ijepes.2014.02.027
* Kaya, H., Tüfekci, P., Gürgen, S. F. (2012). Local and Global Learning Methods for Predicting Power of a Combined Gas & Steam Turbine. Proceedings of the International Conference on Emerging Trends in Computer and Electronics Engineering ICETCEE 2012, pp. 13-18, Dubai.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-26. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Features and the target are stored as float64.
* The columns are named after their descriptions in the variables table of the source, written in lower case with underscores: AT is stored as temperature, V as exhaust_vacuum, AP as ambient_pressure, RH as relative_humidity and the target PE as net_hourly_electrical_energy_output. The features are stored in the order AT, V, AP, RH.

.. note::

   The features are hourly averages of ambient variables. The averages are taken from various sensors located around the plant that record the variables every second. The source gives the variables without normalization.

.. note::

   Units: the temperature is in degrees Celsius, the exhaust vacuum in cm Hg, the ambient pressure in millibar, the relative humidity in percent and the net hourly electrical energy output in MW. The source documents the ranges 1.81 to 37.11 for the temperature, 25.36 to 81.56 for the exhaust vacuum, 992.89 to 1033.30 for the ambient pressure, 25.56 to 100.16 for the relative humidity and 420.26 to 495.76 for the output. The relative humidity goes above 100 percent in the source and is stored as it is.

.. note::

   According to the source the exhaust vacuum is collected from and has an effect on the steam turbine, and the other three variables affect the performance of the gas turbine.

.. note::

   To allow 5x2 fold statistical tests, the source provides the data shuffled five times. This dataset holds the rows in the order of the table that UCI serves through ucimlrepo.

.. note::

   UCI prints the citation, and the name of the first creator on its page, without the letters of the name Tüfekci that are not in the English alphabet. The citation is given here as UCI prints it, the name of the creator as it is written in the papers of the source.
