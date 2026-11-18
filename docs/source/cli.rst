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
   features. The line below the table counts the datasets that are shown, by task. The
   options choose the rows and their order. The datasets are filtered first, then ordered,
   and the table shows the page that ``--offset`` and ``--limit`` choose.

   ``--task {classification,regression}``
      Show only the datasets of this task.

   ``--name PATTERN``
      Show only the datasets whose name matches the pattern, like ``ILIKE`` in SQL. ``*`` (or
      ``%``, as in SQL) stands for any characters, ``?`` for one character and ``[abc]`` for
      one of the listed characters, so ``"wine*"`` starts with ``wine``, ``"*quality"`` ends
      with ``quality`` and ``"*ine*"`` contains ``ine``. Capital letters do not matter. A
      pattern without these characters has to match the whole name, as ``ILIKE 'wine'`` does,
      and when a wider pattern would find more datasets, a line below the table suggests it.
      ``_`` is an ordinary character, not a wildcard, because the names have it. Put the
      pattern in quotes: a Unix shell can replace an ``*`` that is not quoted with the names
      of files.

   ``--missing`` or ``--no-missing``
      Show only the datasets that have, or do not have, missing values. Without either
      option both kinds are shown.

   ``--sort {name,samples,features}``
      The column to order the rows by. The default is ``name``.

   ``--reverse``
      Reverse the order, for example to see the largest dataset first. Datasets with an equal
      value stay in the order of their names.

   ``--offset N``
      Skip the first ``N`` rows of the ordered list. The default is 0.

   ``--limit N``
      Show at most ``N`` rows. The default is 25. When the table is cut, a line below it says
      which rows are shown, for example ``Showing 1-25 of 31.``, and how to see the rest.

   ``--all``
      Show every row, without a limit. It cannot be used together with ``--limit``.

   When no dataset matches the filters, or ``--offset`` is past the last row, a message says
   so and the exit code is 0 (the JSON is an empty array).

   ``--format {text,md,json}`` and ``--output PATH`` choose the format and the file, see
   `Format and file`_. The default limit does not cut the JSON.

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
      about features that describe people, so read them before you use a dataset. The JSON
      always has the changes and the notes.

   ``--format {text,md,json}`` and ``--output PATH`` choose the format and the file, see
   `Format and file`_.

The examples below are not copied: they are the output of the commands, produced when this
documentation is built.

.. command-output:: pyml-datasets list
   :prompt:

The regression datasets, the one with the most samples first:

.. command-output:: pyml-datasets list --task regression --sort samples --reverse
   :prompt:

The datasets whose name starts with ``wine``, and the ones without missing values, two at a
time (the second page):

.. command-output:: pyml-datasets list --name "wine*"
   :prompt:

.. command-output:: pyml-datasets list --no-missing --limit 2 --offset 2
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

Format and file
---------------

``list`` and ``show`` take the same three options.

``--format {text,md,json}``
   ``text`` is the output for the terminal and the default. ``md`` is Markdown: a table for
   ``list``, and for ``show`` sections in the style of ``NOTICE.md``, with the addresses in
   angle brackets. ``json`` is for programs: ``list`` gives an array of objects (``name``,
   ``task``, ``license``, ``samples``, ``features`` and ``has_missing``) and ``show`` gives
   one object with every field of :class:`~pyml_datasets.DatasetInfo` and also
   ``n_samples``, ``n_features``, ``feature_names``, ``target_names`` and ``size_bytes``.
   The JSON of ``list`` is not cut by the default limit. On the terminal it is plain ASCII, so
   a console with another code page, such as cp1252 on Windows, still gets valid JSON.

``--output PATH``, ``-o PATH``
   Write the result to a file instead of the terminal. Without ``--format`` the extension
   chooses the format: ``.md``, ``.txt`` or ``.json``. Another extension needs ``--format``,
   and a ``--format`` that does not fit the extension is an error.

   A file is always written in UTF-8, without a byte order mark and with ``\n`` at the end of
   every line, whatever the console, the locale and the platform are, so the same command
   gives the same bytes everywhere. A character is never replaced with ``?`` in a file. A text
   file has no colors and no links and is wrapped at 100 characters, not at the width of the
   terminal.

   A name alone is a file in the current directory of the terminal, a relative path is taken
   from there, and a full path is used as it is. ``~`` is expanded. The directory must
   exist, it is not created. After the file is written, its full path is printed to the
   standard error, so the standard output stays clean. ``-o -`` means the terminal.

``--force``
   Overwrite the file of ``--output`` if it exists. Without it an existing file is an
   error, and nothing is written.

.. code-block:: console

   $ pyml-datasets show german_credit --full -o german_credit.md
   $ pyml-datasets list --format json --task classification -o classification.json
   $ pyml-datasets list --format md --name "wine*"

The wrong options (a format that does not fit the extension, a missing directory, a file that
exists) end with exit code 2, and a file that cannot be written with exit code 1.

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
