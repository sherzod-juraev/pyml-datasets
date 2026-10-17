License and citation
====================

Code
----

The code of pyml-datasets is released under the MIT license, see the ``LICENSE`` file in the
repository and in the installed package metadata.

Data
----

The datasets were created by other people, so each one keeps the license of its original
source. Only two licenses are accepted in this project:

* `CC0 1.0 <https://creativecommons.org/publicdomain/zero/1.0/>`__, a public domain
  dedication. Nothing is required, but citing the creators is good practice.
* `CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__. You may use and share the
  data, also commercially, if you give credit, link the license and say if changes were
  made. The citation on each dataset page and in ``get_info(name).citation`` is the credit,
  and the changes are listed on the same page.

.. include:: /_generated/license_table.inc

The license texts are in the ``LICENSES`` folder of the repository and of the installed
package, together with ``NOTICE.md``, which lists the creators, sources, citations and
changes of every dataset.

How a dataset is admitted
-------------------------

A dataset is bundled only if its source states one of the two licenses above. A dataset
with no license, with a non-commercial or share-alike license, with an "educational use"
statement or with an unclear origin is not bundled, even if it is very well known.
For each dataset the repository keeps a short evidence file (``legal/evidence/<name>.md``)
with the page that states the license and the date it was checked, and the automated check
``python -m scripts.check_legal`` fails if any dataset lacks one. The rules are written in
the contributing guide of the repository.

.. important::

   I am not a lawyer and this is not legal advice. The licenses were read at the source on
   the dates in the evidence files. Licenses can change, so check the source yourself if it
   matters for your use.

Removed datasets
----------------

Version 0.1.0 also contained Diabetes, Linnerud and California Housing. Their sources do not
state a license that allows redistribution, so they were removed in 0.2.0, see the
:doc:`changelog`.

Citation
--------

If you use a dataset in published work, cite its original authors. The references are in the
*Source and citation* section of every page in :doc:`datasets/index`.

Takedown and corrections
------------------------

If you hold the rights to a dataset here and the license, the attribution or the changes
listed are wrong, or you do not want it distributed, write to
juraevsherzod9943@gmail.com. It will be corrected or removed.
