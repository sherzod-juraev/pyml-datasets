:`og:description`: |home_description|

pyml-datasets
=============

Classic tabular datasets for `pyml <https://github.com/sherzod-juraev/pyml>`_,
stored as NumPy ``.npz`` files and loaded with a single function call. Only datasets
with an explicit **CC0 1.0** or **CC BY 4.0** license are bundled, and each one keeps its
original license, citation and a list of the changes made to it.

This is a personal project of a student, made for pyml. It is not looking for contributors,
see the `README <https://github.com/sherzod-juraev/pyml-datasets>`_.

The package depends only on NumPy. The tools used to download and convert the
original data, for example scikit-learn and ucimlrepo, are needed only to
rebuild the data files, never to use them.

Each dataset is described in the :doc:`datasets/index` section, with its
source, citation, and license. A file is read from disk only when its
``load_*`` function is called, so importing the package stays cheap.

Originally built to support the `pyml <https://github.com/sherzod-juraev/pyml>`_
project, but it is a standalone package with no dependency on pyml.

.. grid:: 1 1 2 2
   :gutter: 3
   :class-container: sd-mb-4

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Quick start
      ^^^^^^^^^^^
      Load a dataset, inspect it and train a pyml model in a few lines.

      +++
      .. button-ref:: quick_start
         :ref-type: doc
         :color: primary
         :expand:

         Get started

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Datasets
      ^^^^^^^^
      What each dataset contains, where it comes from and how to cite it.

      +++
      .. button-ref:: datasets/index
         :ref-type: doc
         :color: primary
         :expand:

         Browse the datasets

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      License and citation
      ^^^^^^^^^^^^^^^^^^^^
      Which license applies to the code and to each dataset.

      +++
      .. button-ref:: license
         :ref-type: doc
         :color: primary
         :expand:

         Read the license

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      API reference
      ^^^^^^^^^^^^^
      The ``Dataset`` class and the ``load_*`` functions.

      +++
      .. button-ref:: api
         :ref-type: doc
         :color: primary
         :expand:

         Browse the API

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   quick_start
   datasets/index
   data_format
   api
   license
   design/index
   changelog
