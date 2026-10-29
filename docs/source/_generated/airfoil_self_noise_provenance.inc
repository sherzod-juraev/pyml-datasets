Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/291/airfoil+self+noise>`__
* Obtained from: UCI Machine Learning Repository, dataset 291, downloaded with the ucimlrepo package: all 1503 examples with 5 inputs. The ucimlrepo version is recorded in the file.
* Creators: Thomas Brooks, D. Pope, Michael Marcolini
* DOI: https://doi.org/10.24432/C5VW2C

Please cite the dataset as:

   Brooks, T., Pope, D., & Marcolini, M. (1989). Airfoil Self-Noise [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5VW2C.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-10-29. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. Features and the target are stored as float64.
* The columns are named after their descriptions in the variables table of the source, written in lower case with underscores: attack-angle is stored as angle_of_attack, chord-length as chord_length, free-stream-velocity as free_stream_velocity, suction-side-displacement-thickness as suction_side_displacement_thickness, and the target scaled-sound-pressure as scaled_sound_pressure_level. frequency keeps its name. The features are stored in the order of the variables table.

.. note::

   The NASA data set comprises different size NACA 0012 airfoils at various wind tunnel speeds and angles of attack. The span of the airfoil and the observer position were the same in all of the experiments.

.. note::

   Units: the frequency is in Hz, the angle of attack in degrees, the chord length in meters, the free-stream velocity in meters per second, the suction side displacement thickness in meters and the scaled sound pressure level in decibels.

.. note::

   In the data file of the source the frequency takes whole numbers from 200 to 20000 (21 different values), the angle of attack takes 27 different values from 0 to 22.2, the chord length takes 6 different values from 0.0254 to 0.3048 and the free-stream velocity takes 4 different values: 31.7, 39.6, 55.5 and 71.3.

.. note::

   The variables table of UCI lists the angle of attack as binary, but the data file has 27 different values for it, as written above. It is stored as the number the source gives.
