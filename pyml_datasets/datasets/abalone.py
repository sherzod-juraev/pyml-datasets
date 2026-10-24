"""Abalone: physical measurements of 4177 abalones and the number of rings of their shell."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="abalone",
    title="Abalone",
    task="regression",
    summary=(
        "Physical measurements of 4177 abalones and the number of rings of their shell, "
        "which tells the age of the animal: the number of rings plus 1.5 gives the age in "
        "years. Seven features are measurements (length, diameter, height and four weights) "
        "and one is the sex (male, female or infant). The number of rings can be predicted "
        "as a continuous value or as a classification problem."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/1/abalone",
    doi="10.24432/C55C7W",
    creators=("Warwick Nash", "Tracy Sellers", "Simon Talbot", "Andrew Cawthorn", "Wes Ford"),
    citation=(
        "Nash, W., Sellers, T., Talbot, S., Cawthorn, A., & Ford, W. (1994). Abalone "
        "[Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55C7W"
    ),
    obtained_from=(
        "UCI Machine Learning Repository, dataset 1, downloaded with the ucimlrepo package: "
        "all 4177 examples with 8 inputs. The ucimlrepo version is recorded in the file."
    ),
    changes=(
        "Converted to the NumPy NPZ format. Features and the target are stored as float64.",
        "The column Sex is stored as integer codes, in the order of the category names listed "
        "for it. The names of the columns are written in lower case, for example Whole_weight "
        "is stored as whole_weight. The target is the number of rings.",
        "The continuous values are stored as the source gives them, with the scaling that the "
        "notes describe.",
    ),
    verified_on="2026-10-24",
    references=(
        "Nash, W. J., Sellers, T. L., Talbot, S. R., Cawthorn, A. J., & Ford, W. B. (1994). "
        "The Population Biology of Abalone (Haliotis species) in Tasmania. I. Blacklip "
        "Abalone (H. rubra) from the North Coast and Islands of Bass Strait. Sea Fisheries "
        "Division, Technical Report No. 48 (ISSN 1034-3288).",
        "Waugh, S. (1995). Extending and benchmarking Cascade-Correlation. PhD thesis, "
        "Computer Science Department, University of Tasmania.",
    ),
    categorical={"sex": ("F", "I", "M")},
    notes=(
        "The source says that examples with missing values were removed from the original "
        "data, most of them because the number of rings was missing, and that the ranges of "
        "the continuous values were scaled for use with an artificial neural network by "
        "dividing by 200. Keep this in mind when you use the units mm and grams that the "
        "variable table of UCI lists.",
        "The data comes from a study that was not made for machine learning, by the Marine "
        "Resources Division of the Department of Primary Industry and Fisheries, Tasmania. "
        "The dataset was donated to UCI by Sam Waugh of the University of Tasmania.",
        "The sex is M, F or I (infant).",
        "The number of rings plus 1.5 gives the age of the abalone in years.",
    ),
)


def load_abalone() -> Dataset:
    """Load the Abalone dataset (regression, 4177 samples, 8 features).

    The dataset has one categorical feature, ``sex``, stored as integer codes.

    Returns
    -------
    Dataset
        Dataset with the sex and the physical measurements of an abalone as features and the
        number of rings of its shell as target. ``Dataset.info`` holds the license, the
        source, the citation and the names of the categories.

    Examples
    --------
    >>> from pyml_datasets import load_abalone
    >>> X, y = load_abalone()
    >>> X.shape, y.shape
    ((4177, 8), (4177,))
    """
    return load_npz(INFO)
