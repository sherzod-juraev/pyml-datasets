:`og:description`: |home_description|

pyml-datasets
=============

Classic tabular datasets for `pyml <https://github.com/sherzod-juraev/pyml>`_,
stored as NumPy ``.npz`` files and loaded with a single function call. Only datasets
with an explicit **CC0 1.0** or **CC BY 4.0** license are bundled, and each one keeps its
original license, citation and a list of the changes made to it.

This is a personal project of a student, made for pyml. It is not looking for contributors,
see the `README <https://github.com/sherzod-juraev/pyml-datasets#readme>`_.

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

   .. grid-item-card:: Quick start
      :link: quick_start
      :link-type: doc

      Load a dataset, inspect it and train a pyml model in a few lines.

   .. grid-item-card:: Datasets
      :link: datasets/index
      :link-type: doc

      What each dataset contains, where it comes from and how to cite it.

   .. grid-item-card:: License and citation
      :link: license
      :link-type: doc

      Which license applies to the code and to each dataset.

   .. grid-item-card:: API reference
      :link: api
      :link-type: doc

      The ``Dataset`` class and the ``load_*`` functions.

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
