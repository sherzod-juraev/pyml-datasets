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
   Prints the facts about one dataset in sections. The header has the title, the task and
   the license. *Overview* has the number of samples and features, the class or target
   names, whether values are missing and the size of the data file. *Provenance* has the
   source, the license with the date it was checked, the DOI and the creators, and the
   addresses are links in terminals that support links. *Features* lists every feature name,
   numeric and categorical ones apart, and *Citation* has the text to cite.

   ``--full``
      Also print the changes made to the data and the notes. Without it a line below the
      report counts them. The notes can hold a warning, for example about a cost matrix or
      about features that describe people, so read them before you use a dataset.

The examples below are not copied: they are the output of the commands, produced when this
documentation is built.

.. command-output:: pyml-datasets list
   :prompt:

The regression datasets, the one with the most samples first:

.. command-output:: pyml-datasets list --task regression --sort samples --reverse
   :prompt:

.. command-output:: pyml-datasets show iris
   :prompt:

A dataset with notes, and the changes and the notes in full:

.. command-output:: pyml-datasets show german_credit
   :prompt:

.. command-output:: pyml-datasets show iris --full
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
