Single source of truth
======================

Version 0.1.0 wrote the same facts about a dataset in many places: the loader, the tests,
the documentation page, the license table, the README and the data file. They drifted apart,
and one of them (the license) was wrong for three datasets.

Since 0.2.0 each dataset has one module, ``pyml_datasets/datasets/<name>.py``, with a
frozen ``DatasetInfo`` called ``INFO`` and a loader. ``INFO`` holds the license, the source,
the DOI, the creators, the citation, where the data was obtained from, the changes made, the
categorical features and the date the license was checked. Its constructor refuses invalid
values: a license outside the allowed list, a URL that is not https, a malformed DOI, empty
creators or changes.

Everything else is *generated* from ``INFO`` by ``python -m scripts.generate``:

* the registry (``pyml_datasets/datasets/__init__.py``) and the public exports,
* the description stored in the data file, and the ``meta`` array,
* ``NOTICE.md``, the table in the README, and the documentation tables and includes,
* ``MANIFEST.json``, the digests of the arrays.

``python -m scripts.generate --check`` fails when any generated file is out of date, so CI
catches a hand edit. Adding a dataset therefore means writing one module, one recipe and
one page of prose, not editing seven files. A recipe describes *how to get the arrays*; it
knows nothing about licenses.
