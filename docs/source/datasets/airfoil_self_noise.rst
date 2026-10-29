Airfoil Self-Noise
==================

Scaled sound pressure level of NACA 0012 airfoil blade sections, to be predicted from five
inputs: the frequency, the angle of attack, the chord length, the free-stream velocity and the
suction side displacement thickness. The source calls it a NASA data set, obtained from a
series of aerodynamic and acoustic tests of two and three-dimensional airfoil blade sections
conducted in an anechoic wind tunnel. It is a small, clean **regression** dataset: all
features are numbers and nothing is missing.

Overview
--------

.. include:: /_generated/airfoil_self_noise_overview.inc

Features
--------

The features are stored in this order, which is the order of the variables table of the
source: ``frequency`` (in Hz), ``angle_of_attack`` (in degrees), ``chord_length`` (in meters),
``free_stream_velocity`` (in meters per second) and ``suction_side_displacement_thickness``
(in meters). All of them are stored as ``float64``. The names are the descriptions of the
variables table of the source written in lower case with underscores.

In the data file of the source the frequency takes whole numbers from 200 to 20000 (21
different values) and the angle of attack takes 27 different values from 0 to 22.2. The chord
length takes only 6 different values, from 0.0254 to 0.3048, and the free-stream velocity only
4, which are 31.7, 39.6, 55.5 and 71.3. The variables table of UCI lists the angle of attack
as binary, which does not match the data, so it is stored as the number the source gives.

The source says that the data set comprises different size NACA 0012 airfoils at various wind
tunnel speeds and angles of attack, and that the span of the airfoil and the observer
position were the same in all of the experiments.

Target
------

``y`` is the scaled sound pressure level in decibels, stored as ``float64``. In the data file
of the source it goes from 103.38 to 140.987.

.. include:: /_generated/airfoil_self_noise_provenance.inc

Example
-------

.. doctest::

   >>> from pyml_datasets import load_airfoil_self_noise
   >>> data = load_airfoil_self_noise()
   >>> data.X.shape, data.y.shape
   ((1503, 5), (1503,))
   >>> data.feature_names[1]
   'angle_of_attack'
   >>> data.has_missing
   False
   >>> round(float(data.y.min()), 2), round(float(data.y.max()), 2)
   (103.38, 140.99)
