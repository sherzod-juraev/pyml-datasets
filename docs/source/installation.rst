Installation
============

Requirements
------------

* Python 3.12, 3.13 or 3.14
* NumPy 1.26 or newer (installed automatically)

The command line also needs rich and rich-argparse, see `Command line`_ below.

.. note::

   pyml-datasets is a personal project and is not published on PyPI, so it is installed
   directly from GitHub.

Install from GitHub
-------------------

.. tab-set::

   .. tab-item:: pip

      Install the latest version of the ``main`` branch:

      .. code-block:: console

         $ pip install git+https://github.com/sherzod-juraev/pyml-datasets.git

      To install a fixed release, add its tag after ``@``, replacing ``vX.Y.Z`` with a tag
      from the `Releases <https://github.com/sherzod-juraev/pyml-datasets/releases>`_ page.
      Pinning a tag keeps your results reproducible, because the data no longer changes under
      you.

      .. code-block:: console

         $ pip install git+https://github.com/sherzod-juraev/pyml-datasets.git@vX.Y.Z

   .. tab-item:: uv

      With `uv <https://docs.astral.sh/uv/>`_, add pyml-datasets to your own project. This
      also records it in your ``pyproject.toml``:

      .. code-block:: console

         $ uv add git+https://github.com/sherzod-juraev/pyml-datasets.git

      To use a fixed release, pass its tag with ``--tag``, replacing ``vX.Y.Z`` with a tag
      from the `Releases <https://github.com/sherzod-juraev/pyml-datasets/releases>`_ page.
      Pinning a tag keeps your results reproducible, because the data no longer changes under
      you.

      .. code-block:: console

         $ uv add git+https://github.com/sherzod-juraev/pyml-datasets.git --tag vX.Y.Z

      To install into the active virtual environment only, without a project, use
      ``uv pip install`` with the same address, and ``@vX.Y.Z`` after it for a release:

      .. code-block:: console

         $ uv pip install git+https://github.com/sherzod-juraev/pyml-datasets.git

Command line
------------

The ``pyml-datasets`` command (see :doc:`cli`) needs rich and rich-argparse. They belong to the
optional ``cli`` extra and are not installed by the commands above. Ask for the extra to
install them too:

.. tab-set::

   .. tab-item:: pip

      .. code-block:: console

         $ pip install "pyml-datasets[cli] @ git+https://github.com/sherzod-juraev/pyml-datasets.git"

   .. tab-item:: uv

      .. code-block:: console

         $ uv add "pyml-datasets[cli] @ git+https://github.com/sherzod-juraev/pyml-datasets.git"

Without the extra the command prints which package is missing and ends with exit code 3.

Check the installation
----------------------

.. tab-set::

   .. tab-item:: pip

      .. code-block:: console

         $ python -c "import pyml_datasets; print(pyml_datasets.__version__)"

   .. tab-item:: uv

      .. code-block:: console

         $ uv run python -c "import pyml_datasets; print(pyml_datasets.__version__)"

This prints the version of the installed release.
