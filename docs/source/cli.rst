Command line
============

The package installs a command, ``pyml-datasets``, that prints the facts about the bundled
datasets, so you can look up a license or a citation without writing any Python. The same
command runs as ``python -m pyml_datasets``.

.. note::

   The output is meant to be read by people and its layout can change in any release. A
   program should use :func:`~pyml_datasets.list_datasets`, :func:`~pyml_datasets.get_info`
   and :func:`~pyml_datasets.load_dataset` and not parse it.

Commands
--------

``pyml-datasets list``
   Prints a table of the datasets with their task, license, number of samples and number of
   features. The line below the table counts the datasets that are shown, by task. Three
   options choose the rows and their order:

   ``--task {classification,regression}``
      Show only the datasets of this task.

   ``--sort {name,samples,features}``
      The column to order the rows by. The default is ``name``.

   ``--reverse``
      Reverse the order, for example to see the largest dataset first. Datasets with an equal
      value stay in the order of their names.

``pyml-datasets show NAME``
   Prints the facts about one dataset: the summary, the license, the source, the DOI, the
   creators, the shape, the size of the data file, the feature and class names, the citation
   and the changes made to the data. Lists of more than ten names are shortened, the
   ``feature_names`` attribute of the loaded :class:`~pyml_datasets.Dataset` has them all.

The examples below are not copied: they are the output of the commands, produced when this
documentation is built.

.. command-output:: pyml-datasets list
   :prompt:

The regression datasets, the one with the most samples first:

.. command-output:: pyml-datasets list --task regression --sort samples --reverse
   :prompt:

.. command-output:: pyml-datasets show iris
   :prompt:

.. command-output:: pyml-datasets --help
   :prompt:

Both commands only read what is bundled with the package, nothing is downloaded or written.

Colors
------

The output is colored when it goes to a terminal. It is plain text when it is redirected to
a file or a pipe, so it can be saved or searched without escape codes. The ``NO_COLOR``
environment variable switches the colors off and ``FORCE_COLOR`` switches them on, also when
the output is not a terminal.

Exit codes
----------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Meaning
   * - 0
     - The command succeeded.
   * - 1
     - A data file is missing from the package or cannot be read.
   * - 2
     - The dataset name is unknown, or the command line is wrong. Errors are printed to the
       standard error stream.

Dependencies
------------

The command uses `rich <https://github.com/Textualize/rich>`_ and
`rich-argparse <https://github.com/hamdanal/rich-argparse>`_, which are installed together
with the package. They are imported only when the command runs, so ``import pyml_datasets``
does not load them.
