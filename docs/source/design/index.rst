Design Notes
============

Notes on the decisions behind pyml-datasets: why the provenance of a dataset is written in
one place, how the legal rules are enforced, and how missing values are stored.

.. grid:: 1 2 2 2
   :gutter: 3
   :class-container: sd-mb-4

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Single source of truth
      ^^^^^^^^^^^^^^^^^^^^^^
      Why ``DatasetInfo`` is the only place where a fact about a dataset is written.

      +++
      .. button-ref:: single_source
         :ref-type: doc
         :color: primary
         :expand:

         Read the note

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      The legal gate
      ^^^^^^^^^^^^^^
      Which licenses are accepted, and what fails when evidence is missing.

      +++
      .. button-ref:: legal_gate
         :ref-type: doc
         :color: primary
         :expand:

         Read the note

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Missing values
      ^^^^^^^^^^^^^^
      Why ``NaN`` and integer codes, and what the package does not do.

      +++
      .. button-ref:: missing_values
         :ref-type: doc
         :color: primary
         :expand:

         Read the note

.. toctree::
   :maxdepth: 1
   :hidden:

   single_source
   legal_gate
   missing_values
