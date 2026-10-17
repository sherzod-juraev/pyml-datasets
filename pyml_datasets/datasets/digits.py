"""Digits: 1797 handwritten digits as 8x8 images, the test set of a UCI dataset."""

from typing import Final

from .._loader import load_npz
from .._types import Dataset, DatasetInfo

INFO: Final = DatasetInfo(
    name="digits",
    title="Optical Recognition of Handwritten Digits",
    task="classification",
    summary=(
        "Images of handwritten digits. Normalized bitmaps of 32x32 pixels were divided into "
        "blocks of 4x4 and the pixels that are on were counted in each block, which gives "
        "8x8 images whose pixels are integers from 0 to 16."
    ),
    license="CC-BY-4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    source="UCI Machine Learning Repository",
    source_url="https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits",
    doi="10.24432/C50P49",
    creators=("E. Alpaydin", "C. Kaynak"),
    citation=(
        "Alpaydin, E. & Kaynak, C. (1998). Optical Recognition of Handwritten Digits "
        "[Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C50P49"
    ),
    obtained_from=(
        "scikit-learn (sklearn.datasets.load_digits), which redistributes a copy of the test "
        "set of the UCI dataset. The scikit-learn version is recorded in the file."
    ),
    changes=(
        "Only the test set of the UCI dataset is included: 1797 of its 5620 samples, as "
        "distributed by scikit-learn. The training set (3823 samples) is not included.",
        "Converted to the NumPy NPZ format. Pixels are stored as float64 and the digit as "
        "int64 labels.",
        "Feature and class names follow scikit-learn.",
    ),
    verified_on="2026-10-17",
    references=(
        "C. Kaynak (1995) Methods of Combining Multiple Classifiers and Their Applications "
        "to Handwritten Digit Recognition, MSc Thesis, Institute of Graduate Studies in "
        "Science and Engineering, Bogazici University.",
        "E. Alpaydin, C. Kaynak (1998) Cascading Classifiers, Kybernetika.",
    ),
)


def load_digits() -> Dataset:
    """Load the handwritten digits dataset (classification, 1797 samples, 64 features).

    Returns
    -------
    Dataset
        Dataset with the 10 digits as classes and the pixels of an 8x8 image as features.
        ``Dataset.info`` holds the license, the source and the citation.

    Examples
    --------
    >>> from pyml_datasets import load_digits
    >>> X, y = load_digits()
    >>> X.shape, y.shape
    ((1797, 64), (1797,))
    """
    return load_npz(INFO)
