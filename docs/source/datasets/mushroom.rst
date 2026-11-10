Mushroom
========

Descriptions of mushrooms from a field guide, to be classified as edible or poisonous. All 22
features are **categorical**, so the dataset is a good one for practising with categories,
with one feature that has **missing values**, and with classes that are nearly **balanced**.
The classic use is decision trees and rule learning, because a few of the features already
separate the classes almost perfectly.

Overview
--------

.. include:: /_generated/mushroom_overview.inc

Features
--------

All 22 features are categorical and stored as integer codes. The categories are the
one-letter codes of the source that occur in the data, in alphabetical order, so the code of
a letter is its position in ``data.info.categorical[feature]``. ``data.categorical_features``
gives the columns, which here are all of them. The table lists the letters of every feature
in the order of the codes, with the meaning that the documentation of the source gives them.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feature
     - Codes, in the order of the integer codes 0, 1, 2, ...
   * - ``cap_shape``
     - b = bell, c = conical, f = flat, k = knobbed, s = sunken, x = convex
   * - ``cap_surface``
     - f = fibrous, g = grooves, s = smooth, y = scaly
   * - ``cap_color``
     - b = buff, c = cinnamon, e = red, g = gray, n = brown, p = pink, r = green, u = purple,
       w = white, y = yellow
   * - ``bruises``
     - f = no, t = bruises
   * - ``odor``
     - a = almond, c = creosote, f = foul, l = anise, m = musty, n = none, p = pungent, s =
       spicy, y = fishy
   * - ``gill_attachment``
     - a = attached, f = free
   * - ``gill_spacing``
     - c = close, w = crowded
   * - ``gill_size``
     - b = broad, n = narrow
   * - ``gill_color``
     - b = buff, e = red, g = gray, h = chocolate, k = black, n = brown, o = orange, p =
       pink, r = green, u = purple, w = white, y = yellow
   * - ``stalk_shape``
     - e = enlarging, t = tapering
   * - ``stalk_root``
     - b = bulbous, c = club, e = equal, r = rooted
   * - ``stalk_surface_above_ring``
     - f = fibrous, k = silky, s = smooth, y = scaly
   * - ``stalk_surface_below_ring``
     - f = fibrous, k = silky, s = smooth, y = scaly
   * - ``stalk_color_above_ring``
     - b = buff, c = cinnamon, e = red, g = gray, n = brown, o = orange, p = pink, w = white,
       y = yellow
   * - ``stalk_color_below_ring``
     - b = buff, c = cinnamon, e = red, g = gray, n = brown, o = orange, p = pink, w = white,
       y = yellow
   * - ``veil_type``
     - p = partial
   * - ``veil_color``
     - n = brown, o = orange, w = white, y = yellow
   * - ``ring_number``
     - n = none, o = one, t = two
   * - ``ring_type``
     - e = evanescent, f = flaring, l = large, n = none, p = pendant
   * - ``spore_print_color``
     - b = buff, h = chocolate, k = black, n = brown, o = orange, r = green, u = purple, w =
       white, y = yellow
   * - ``population``
     - a = abundant, c = clustered, n = numerous, s = scattered, v = several, y = solitary
   * - ``habitat``
     - d = woods, g = grasses, l = leaves, m = meadows, p = paths, u = urban, w = waste

``stalk_root`` has missing entries, marked with ``?`` in the source: 2480 values in the 8124
rows, which is the only feature with missing values. They are stored as ``NaN``, so
``data.has_missing`` is ``True``. Fill or drop them before fitting a model that cannot handle
``NaN``.

``veil_type`` has the value ``p`` (partial) in every sample, so it carries no information.
It is kept as it is in the source.

The documentation of the source lists codes that never occur in the data. They are not
categories here and get no integer code:

``gill_attachment``: d (descending), n (notched); ``gill_spacing``: d (distant);
``stalk_root``: u (cup), z (rhizomorphs); ``veil_type``: u (universal); ``ring_type``: c
(cobwebby), s (sheathing), z (zone)

Target
------

``y`` is 0 if the mushroom is edible (4208 samples, 51.8 percent) and 1 if it is poisonous
(3916, 48.2 percent). The source describes hypothetical samples that correspond to 23 species
of the Agaricus and Lepiota family, and it combined the species of unknown edibility with the
poisonous class, so the class poisonous also holds mushrooms whose edibility is unknown.

A model trained on this dataset must not be used to decide whether a real mushroom is safe to
eat. The field guide itself states that there is no simple rule for determining the edibility
of a mushroom.

.. include:: /_generated/mushroom_provenance.inc

Example
-------

.. doctest::

   >>> import numpy as np
   >>> from pyml_datasets import load_mushroom
   >>> data = load_mushroom()
   >>> data.X.shape
   (8124, 22)
   >>> data.has_missing
   True
   >>> int(np.isnan(data.X).sum())
   2480
   >>> data.categorical_features == tuple(range(22))
   True
   >>> data.info.categorical["odor"]
   ('a', 'c', 'f', 'l', 'm', 'n', 'p', 's', 'y')
   >>> data.target_names
   ('edible', 'poisonous')
   >>> np.bincount(data.y)
   array([4208, 3916])
