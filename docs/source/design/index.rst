Design Notes
============

Notes on the decisions behind pyml-datasets: why the provenance of a dataset is written in
one place, how the legal rules are enforced, and how missing values are stored.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: Single source of truth
      :link: single_source
      :link-type: doc
      :shadow: sm

      Why ``DatasetInfo`` is the only place where a fact about a dataset is written.

   .. grid-item-card:: The legal gate
      :link: legal_gate
      :link-type: doc
      :shadow: sm

      Which licenses are accepted, and what fails when evidence is missing.

   .. grid-item-card:: Missing values
      :link: missing_values
      :link-type: doc
      :shadow: sm

      Why ``NaN`` and integer codes, and what the package does not do.

.. toctree::
   :maxdepth: 1
   :hidden:

   single_source
   legal_gate
   missing_values
