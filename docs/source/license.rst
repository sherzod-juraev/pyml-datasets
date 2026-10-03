License and citation
====================

Code
----

The code of pyml-datasets is released under the MIT license, see the ``LICENSE``
file in the repository and in the installed package metadata.

Data
----

The datasets were created by other people, so each one keeps the terms of its
original source.

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Dataset
     - License
     - Original source
   * - :doc:`datasets/iris`
     - CC BY 4.0
     - `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/53/iris>`__
   * - :doc:`datasets/wine`
     - CC BY 4.0
     - `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/109/wine>`__
   * - :doc:`datasets/breast_cancer`
     - CC BY 4.0
     - `UCI Machine Learning Repository
       <https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-diagnostic>`__
   * - :doc:`datasets/diabetes`
     - Not stated by the source
     - `Efron et al. (2004), data page
       <https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html>`_
   * - :doc:`datasets/linnerud`
     - Not stated by the source
     - Tenenhaus (1998), as distributed by scikit-learn
   * - :doc:`datasets/california_housing`
     - Not stated by the source
     - Pace and Barry (1997), as distributed by scikit-learn

CC BY 4.0 datasets
~~~~~~~~~~~~~~~~~~

Iris, Wine and Breast Cancer Wisconsin (Diagnostic) are distributed by the UCI Machine
Learning Repository under the `Creative Commons Attribution 4.0 International license
<https://creativecommons.org/licenses/by/4.0/>`_. The license text is included in the
package as
`LICENSES/CC-BY-4.0.txt <https://github.com/sherzod-juraev/pyml-datasets/blob/main/LICENSES/CC-BY-4.0.txt>`_.
It requires giving credit to the original authors, so please use the citation on
each dataset page.

Changes made: the files were converted to the NumPy ``.npz`` format. Feature values
were not modified, only stored as ``float64``, and class labels were stored as
``int64``.

Datasets without a stated license
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For Diabetes, Linnerud and California Housing no license could be found at the original
source, so no license is claimed for them here. They are included for educational use
with attribution to their authors. Please check the original source before using them
for any other purpose.

Citation
--------

If you use a dataset in published work, cite its original authors. The references are
listed in the *Source and citation* section of every page in :doc:`datasets/index`.
