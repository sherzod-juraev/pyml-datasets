Digits
======

Small greyscale images of handwritten digits, 8 by 8 pixels each, prepared from the
NIST handwritten digit forms. Only the 1797 samples of the test part of the original UCI
release are included. It is a small, fast dataset for trying out multiclass classifiers.

Overview
--------

.. include:: /_generated/digits_overview.inc

Features
--------

64 features named ``pixel_<row>_<column>``. Every value is the count of active pixels in a
4 by 4 block of the original image, an integer from 0 to 16, stored as ``float64``.

Target
------

``y`` is the digit shown in the image, an integer from 0 to 9. The ten classes have between
174 and 183 samples.

.. include:: /_generated/digits_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_digits
   >>> data = load_digits()
   >>> data.X.shape
   (1797, 64)
   >>> int(np.bincount(data.y).sum())
   1797
