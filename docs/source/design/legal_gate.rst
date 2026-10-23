Legal gate
==========

The project exists to be used safely in teaching and in other projects, so the license of a
dataset is treated like a test: it can fail the build.

* Only ``CC0-1.0`` and ``CC-BY-4.0`` are accepted. The allowed list is a constant in
  ``pyml_datasets/_types.py`` and ``DatasetInfo`` refuses anything else.
* Every license used has its text in ``LICENSES/``, and ``pyproject.toml`` declares the
  license expression of the wheel (``MIT AND CC-BY-4.0 AND CC0-1.0``) together with
  ``NOTICE.md``.
* Every dataset has an evidence file in ``legal/evidence/``: the license, the page that
  states it, the date, who checked it and an archived copy of the page.
* ``python -m scripts.check_legal`` fails on a missing evidence file, a mismatch between the
  evidence and ``INFO``, a DOI that is missing from the citation, a ``TODO`` left in the
  files, an orphan data file and a license expression that does not match the data. It fails
  as well when the evidence is not complete: the ``Archive`` must be a Wayback Machine link
  to the license page of the evidence, and the ``Maintainer check`` must give the name of the
  maintainer and a date. A dataset with a ``pending`` value in either field cannot be merged.
  The check only warns when a license was verified more than a year ago.

Why not allow more licenses? Share-alike and non-commercial licenses would change the
license of the whole package or limit its use, and "free for educational use" statements
are not licenses. If a good dataset is excluded, it is the safer choice.

The check cannot read a license page for you. The evidence files are written by hand, and a
person must re-read the page and open the archived copy, because the Wayback Machine
sometimes saves an empty or blocked page. That is the purpose of the *Maintainer check*
field.
