Source and citation
-------------------

* Source: `UCI Machine Learning Repository <https://archive.ics.uci.edu/dataset/73/mushroom>`__
* Obtained from: UCI Machine Learning Repository, dataset 73, downloaded with the ucimlrepo package: all 8124 examples with 22 inputs and the target. The ucimlrepo version is recorded in the file.
* Creators: Jeff Schlimmer (donor), G. H. Lincoff (The Audubon Society Field Guide to North American Mushrooms, 1981)
* DOI: https://doi.org/10.24432/C5959T

Please cite the dataset as:

   Mushroom [Dataset]. (1981). UCI Machine Learning Repository. https://doi.org/10.24432/C5959T.

See also:

* Lincoff, G. H. (Pres.) (1981). The Audubon Society Field Guide to North American Mushrooms. New York: Alfred A. Knopf.
* Schlimmer, J. S. (1987). Concept Acquisition Through Representational Adjustment (Technical Report 87-19). Doctoral dissertation, Department of Information and Computer Science, University of California, Irvine.

License
-------

`CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`__, as stated by the source. The license was checked at the source on 2026-11-10. See :doc:`/license`.

Changes made
~~~~~~~~~~~~

* Converted to the NumPy NPZ format. The features are stored as float64 and the target as int64 labels.
* Categorical features are stored as integer codes. The categories are the one-letter codes of the source that occur in the data, in alphabetical order, and the code of a category is its position in the list of the feature. The target is 0 for e (edible) and 1 for p (poisonous).
* Entries of stalk_root that the source marks as missing (the text ?) are stored as NaN.
* The hyphens in the column names are replaced with underscores, for example cap-shape becomes cap_shape.

.. note::

   The samples are descriptions of hypothetical mushrooms that correspond to 23 species (pages 500 to 525 of the Guide). The Guide says that each species is definitely edible, definitely poisonous, or of unknown edibility and not recommended, and the source combined the last class with the poisonous one. So the class poisonous also holds mushrooms whose edibility is unknown.

.. note::

   A model trained on this dataset must not be used to decide whether a real mushroom is safe to eat. The Guide itself states that there is no simple rule for determining the edibility of a mushroom.

.. note::

   The UCI page and ucimlrepo list no creators. The creators above are the donor and the origin of the records, as the file agaricus-lepiota.names of the source gives them.

.. note::

   The meaning of the one-letter codes is in the file agaricus-lepiota.names of the source and in the documentation page of this dataset.

.. note::

   stalk_root has 2480 missing entries, the text ? in the source, which are NaN. The source documentation says that all 2480 missing entries are in this feature, so fill or drop them before fitting a model that cannot handle NaN.

.. note::

   veil_type has the same value, p (partial), in all 8124 samples, so it carries no information. It is kept as it is in the source.

.. note::

   The source documentation lists codes that never occur in the data, so they are not categories here: gill_attachment (d, n), gill_spacing (d), stalk_root (u, z), veil_type (u) and ring_type (c, s, z).

.. note::

   The classes are nearly balanced: 4208 samples, 51.8 percent, are edible and 3916, 48.2 percent, are poisonous, as the source documentation states.
