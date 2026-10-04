Installation
============

Requirements
------------

|python-badge|

.. |python-badge| image:: https://img.shields.io/badge/python-3.12+-blue.svg
   :target: https://www.python.org/

.. note::

   ``pyml-datasets`` is **not published to PyPI**.
   The distribution is installed as ``pyml-datasets`` and imported as
   ``pyml_datasets``.

Install
-------

.. tab-set::

   .. tab-item:: From GitHub (pip)

      Install the latest release directly from GitHub without cloning:

      .. code-block:: console

         $ pip install git+https://github.com/sherzod-juraev/pyml-datasets.git

   .. tab-item:: From source (editable)

      For development, clone the repository and install it in editable
      mode with the ``dev`` extra. This also installs scikit-learn, which
      is only needed to rebuild the data files (see :doc:`data_format`):

      .. code-block:: console

         $ git clone https://github.com/sherzod-juraev/pyml-datasets.git
         $ cd pyml-datasets
         $ pip install -e ".[dev]"
