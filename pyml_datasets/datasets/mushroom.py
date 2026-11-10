"""Mushroom: 8124 mushroom descriptions, predict whether a mushroom is edible or poisonous."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="mushroom",
    title="Mushroom",
    task="classification",
    summary=(
        "Descriptions of hypothetical samples that correspond to 23 species of gilled "
        "mushrooms in the Agaricus and Lepiota family, taken from The Audubon Society Field "
        "Guide to North American Mushrooms (1981). Each of the 8124 samples is described by "
        "22 categorical features, for example the shape, surface and color of the cap, the "
        "odor, the gills, the stalk, the ring and the habitat. The goal is to predict whether "
        "a mushroom is edible or poisonous."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/73/mushroom",
    doi="10.24432/C5959T",
    creators=(
        "Jeff Schlimmer (donor)",
        "G. H. Lincoff (The Audubon Society Field Guide to North American Mushrooms, 1981)",
    ),
    citation=(
        "Mushroom [Dataset]. (1981). UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5959T."
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 73, downloaded with the ucimlrepo package: "
        "all 8124 examples with 22 inputs and the target. The ucimlrepo version is recorded "
        "in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. The features are stored as float64 and the target "
        "as int64 labels.",
        "Categorical features are stored as integer codes. The categories are the one-letter "
        "codes of the source that occur in the data, in alphabetical order, and the code of a "
        "category is its position in the list of the feature. The target is 0 for e (edible) "
        "and 1 for p (poisonous).",
        "Entries of stalk_root that the source marks as missing (the text ?) are stored as NaN.",
        "The hyphens in the column names are replaced with underscores, for example "
        "cap-shape becomes cap_shape.",
    ),
    verified_on="2026-11-10",
    references=(
        "Lincoff, G. H. (Pres.) (1981). The Audubon Society Field Guide to North American "
        "Mushrooms. New York: Alfred A. Knopf.",
        "Schlimmer, J. S. (1987). Concept Acquisition Through Representational Adjustment "
        "(Technical Report 87-19). Doctoral dissertation, Department of Information and "
        "Computer Science, University of California, Irvine.",
    ),
    categorical={
        "cap_shape": ("b", "c", "f", "k", "s", "x"),
        "cap_surface": ("f", "g", "s", "y"),
        "cap_color": ("b", "c", "e", "g", "n", "p", "r", "u", "w", "y"),
        "bruises": ("f", "t"),
        "odor": ("a", "c", "f", "l", "m", "n", "p", "s", "y"),
        "gill_attachment": ("a", "f"),
        "gill_spacing": ("c", "w"),
        "gill_size": ("b", "n"),
        "gill_color": ("b", "e", "g", "h", "k", "n", "o", "p", "r", "u", "w", "y"),
        "stalk_shape": ("e", "t"),
        "stalk_root": ("b", "c", "e", "r"),
        "stalk_surface_above_ring": ("f", "k", "s", "y"),
        "stalk_surface_below_ring": ("f", "k", "s", "y"),
        "stalk_color_above_ring": ("b", "c", "e", "g", "n", "o", "p", "w", "y"),
        "stalk_color_below_ring": ("b", "c", "e", "g", "n", "o", "p", "w", "y"),
        "veil_type": ("p",),
        "veil_color": ("n", "o", "w", "y"),
        "ring_number": ("n", "o", "t"),
        "ring_type": ("e", "f", "l", "n", "p"),
        "spore_print_color": ("b", "h", "k", "n", "o", "r", "u", "w", "y"),
        "population": ("a", "c", "n", "s", "v", "y"),
        "habitat": ("d", "g", "l", "m", "p", "u", "w"),
    },
    has_missing=True,
    notes=(
        "The samples are descriptions of hypothetical mushrooms that correspond to 23 species "
        "(pages 500 to 525 of the Guide). The Guide says that each species is definitely "
        "edible, definitely poisonous, or of unknown edibility and not recommended, and the "
        "source combined the last class with the poisonous one. So the class poisonous also "
        "holds mushrooms whose edibility is unknown.",
        "A model trained on this dataset must not be used to decide whether a real mushroom is "
        "safe to eat. The Guide itself states that there is no simple rule for determining the "
        "edibility of a mushroom.",
        "The UCI page and ucimlrepo list no creators. The creators above are the donor and the "
        "origin of the records, as the file agaricus-lepiota.names of the source gives them.",
        "The meaning of the one-letter codes is in the file agaricus-lepiota.names of the "
        "source and in the documentation page of this dataset.",
        "stalk_root has 2480 missing entries, the text ? in the source, which are NaN. The "
        "source documentation says that all 2480 missing entries are in this feature, so fill "
        "or drop them before fitting a model that cannot handle NaN.",
        "veil_type has the same value, p (partial), in all 8124 samples, so it carries no "
        "information. It is kept as it is in the source.",
        "The source documentation lists codes that never occur in the data, so they are not "
        "categories here: gill_attachment (d, n), gill_spacing (d), stalk_root (u, z), "
        "veil_type (u) and ring_type (c, s, z).",
        "The classes are nearly balanced: 4208 samples, 51.8 percent, are edible and 3916, "
        "48.2 percent, are poisonous, as the source documentation states.",
    ),
)


def load_mushroom() -> Dataset:
    """Load the Mushroom dataset (classification, 8124 samples, 22 features).

    Returns
    -------
    Dataset
        Dataset with 22 categorical features, stored as integer codes, and two classes:
        the mushroom is edible (0) or poisonous (1). Missing entries of ``stalk_root`` are
        ``NaN``. ``Dataset.info`` holds the license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_mushroom
    >>> X, y = load_mushroom()
    >>> X.shape, y.shape
    ((8124, 22), (8124,))
    """
    return load_npz(INFO)
